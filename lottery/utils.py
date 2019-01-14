import redis
import random
from lottery.models import User

class OPRedis(object):
    """
    Redis连接池
    """
    def __init__(self):
        if not hasattr(OPRedis, 'pool'):
            OPRedis.getRedisCoon()  # 创建redis连接
        self.coon = redis.Redis(connection_pool=OPRedis.pool)

    @staticmethod
    def getRedisCoon():
        OPRedis.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

    """
    string类型 {'key':'value'} redis操作
    """
    def setredis(self, key, value, time=None):
        # 非空即真非0即真
        if time:
            res = self.coon.setex(key, value, time)
        else:
            res = self.coon.set(key, value)
        return res

    def getRedis(self, key):
        res = self.coon.get(key).decode()
        return res

    def delRedis(self, key):
        res = self.coon.delete(key)
        return res

    def flushdb(self):
        res = self.coon.flushall()
        return res

    """
    hash类型，{'name':{'key':'value'}} redis操作
    """
    def setHashRedis(self, name, key, value):
        res = self.coon.hset(name, key, value)
        return res

    def getHashRedis(self, name, key=None):
        # 判断key是否我为空，不为空，获取指定name内的某个key的value; 为空则获取name对应的所有value
        if key:
            res = self.coon.hget(name, key)
        else:
            res = self.coon.hgetall(name)
        return res

    def delHashRedis(self, name, key=None):
        if key:
            res = self.coon.hdel(name, key)
        else:
            res = self.coon.delete(name)
        return res

    def qsize(self, key):
        return self.coon.llen(key)  # 返回队列里面list内元素的数量

    def put(self, key, item):
        self.coon.sadd(key, item)  # 添加新元素到队列最右方

    def get_all(self, key):
        items = self.coon.smembers(key)
        return set([int(item) for item in items])

    def get(self, key):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.coon.spop(key)
        return item


obj_redis = OPRedis()


def lottery_method(all_user_ids):
    random.shuffle(all_user_ids)  # 打乱数组顺序
    # 生成抽奖用户
    all_users_with_weights = {}
    for user_id in all_user_ids:
        try:
            user = User.objects.get(pk=int(user_id))
        except:
            user = None
        if user:
            all_users_with_weights[user.id] = user.weights
    # 加权随机
    total = sum(all_users_with_weights.values())  # 权重之和
    rad = random.randint(0, total)  # 在0与权重和之前获取一个随机数
    curr_sum = 0
    result = ''
    for key in all_users_with_weights.keys():
        curr_sum += all_users_with_weights[key]  # 在遍历中，累加当前权重值
        if rad <= curr_sum:  # 当随机数<=当前权重和时，返回权重key
            result = key
            break
    return result