from django.shortcuts import render
from django.shortcuts import render, HttpResponse
import json
from lottery.models import User, PrizeClass, Prize
from collections import defaultdict
from lottery.utils import obj_redis, lottery_method
import random


def index(req):
    # 首页初始化
    prize_classes = []
    for prize_class in PrizeClass.objects.all():
        prize_classes.append({'id': prize_class.id, 'name': prize_class.name})
    return render(req, 'index.html', {
        'prize_classes': prize_classes
    })


def get_all_users(req):
    # 取得所有参与抽奖的用户
    users = []
    for user in User.objects.all():
        users.append({'id': user.id, 'name': user.name, 'serial_number': user.serial_number, 'group': user.group})
    return HttpResponse(json.dumps({"success": True, "users": users}), content_type="application/json")


def get_prize_by_class(req):
    # 取得具体奖项下的所有奖品
    prize_class_id = req.POST.get('prize_class_id', False)
    if prize_class_id:
        try:
            prize_list = Prize.objects.filter(prize_class__id=int(prize_class_id)).all()
        except:
            prize_list = None

        if prize_list:
            prizes = []
            for prize in prize_list:
                prizes.append({'id': prize.id, 'name': prize.name, 'img': prize.img.url,
                               'number': prize.number, 'prize_class': prize.prize_class.name})
            return HttpResponse(json.dumps({"success": True, "prizes": prizes}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"success": False, "prizes": []}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"success": False, "prizes": []}), content_type="application/json")


def get_all_prizes(req):
    # 取得所有奖品
    prizes = defaultdict(list)
    for prize in Prize.objects.values('prize_class__name', 'name', 'img', 'number').order_by('prize_class', 'name'):
        prizes[prize['prize_class__name']].append({'name': prize['name'], 'img': '/media/' + prize['img'], 'number': prize['number']})
    return render(req, 'show_prizes.html', {
        'prizes': dict(prizes)
    })


def lottery(req):
    # 进行抽奖
    all_user_ids = set(User.objects.values_list('id', flat=True).distinct())  # 参与抽奖用户ID
    prize_class_id = req.POST.get('prize_class_id', False)
    prize_id = req.POST.get('prize_id', False)
    if prize_class_id and prize_id:
        try:
            prize = Prize.objects.get(pk=int(prize_id))
        except:
            prize = None
        if prize:
            winners = []  # 中奖结果
            all_winner_ids = obj_redis.get_all('all_winner_ids')  # 所有已中奖人(ID)
            winner_ids = obj_redis.get_all(prize.id)  # 当前奖项已中奖用户(ID)
            win_number = prize.number  # 可中奖人数
            if not all_winner_ids:
                all_winner_ids = set()
            if not winner_ids:
                winner_ids = set()
            # 记录已中奖用户
            for winner_id in winner_ids:
                try:
                    user = User.objects.get(pk=int(winner_id))
                except:
                    user = None
                winners.append({'id': user.id, 'name': user.name, 'group': user.group})
                all_user_ids.remove(user.id)  # 排除当前奖项已中奖用户
            if len(winner_ids) >= win_number:
                # 当前奖项已进行抽奖且已抽取所有可中奖用户
                return HttpResponse(json.dumps({"success": False, "winners": winners,
                                                "messages": '当前奖项已抽奖完毕, 详细请查看中奖名单'}),
                                    content_type="application/json")
            else:
                win_number = win_number - len(winners)  # 可中奖人数=最大可中奖人数-此奖项已中奖人数
                print(win_number)
                # 排除用户
                prohibited_user_ids = [user.id for user in prize.prohibited_users.all()]  # 需要排除的用户
                for prohibited_user_id in prohibited_user_ids:
                    all_user_ids.remove(prohibited_user_id)
                # 添加中奖用户
                for winner_user in prize.win_users.all():
                    if len(winner_ids) >= win_number:
                        break  # 大于可中奖人数, 停止添加中奖用户
                    all_winner_ids.add(winner_user.id)
                    winner_ids.add(winner_user.id)
                    winners.append({'id': winner_user.id, 'name': winner_user.name, 'group': winner_user.group})
                    all_user_ids.remove(winner_user.id)
                    obj_redis.put('all_winner_ids', winner_user.id)
                    obj_redis.put(prize.id, winner_user.id)
                if prize.is_exclude:
                    all_user_ids = list(filter(lambda x: x not in all_winner_ids, all_user_ids))  # 排除所有已中奖用户
                print(prohibited_user_ids)
                print(all_winner_ids)
                print(winners)
                print(all_user_ids)

                win_number = win_number - len(winners)  # 剩余可中奖人数=最大可中奖人数 - 此奖项已中奖人数
                print(win_number)

                # 抽奖
                for _ in range(win_number):
                    winner_id = lottery_method(all_user_ids)
                    try:
                        user = User.objects.get(pk=int(winner_id))
                    except:
                        user = None
                    if user:
                        winners.append({'id': user.id, 'name': user.name, 'group': user.group})
                        all_winner_ids.add(user.id)
                        winner_ids.add(user.id)
                        all_user_ids.remove(user.id)
                        obj_redis.put('all_winner_ids', user.id)
                        obj_redis.put(prize.id, user.id)
                print("中奖结果:")
                print(winners)
                print(len(winners))

                return HttpResponse(json.dumps({"success": True, "winners": winners, "messages": '抽奖成功!恭喜中奖'}), content_type="application/json")

        else:
            return HttpResponse(json.dumps({"success": False, "winners": [], "messages": '当前奖品不存在!'}),
                                content_type="application/json")
    else:
        return HttpResponse(json.dumps({"success": False, "winners": [],  "messages": '请发送正确参数!'}), content_type="application/json")


def get_winner_users(req):
    # 查看中奖名单
    prizes = defaultdict(list)
    for prize in Prize.objects.values('prize_class__name', 'name', 'img', 'number', 'id').order_by('prize_class', 'name'):
        prize_winner_user_ids = obj_redis.get_all(prize['id'])
        winner_users = []
        for prize_winner_user_id in prize_winner_user_ids:
            try:
                user = User.objects.get(pk=int(prize_winner_user_id))
            except:
                user = None
            if user:
                winner_users.append({'name': user.name, 'group':user.group, 'id':user.id})
        prizes[prize['prize_class__name']].append(
            {'id': prize['id'], 'name': prize['name'], 'img': '/media/' + prize['img'],
             'number': prize['number'], 'users': winner_users})

    return render(req, 'show_winner_users.html', {
        'winner_users': dict(prizes)
    })


def reset_all(req):
    obj_redis.flushdb()
    return HttpResponse(json.dumps({"success": True, "messages": '重置所有获奖结果!'}),
                        content_type="application/json")