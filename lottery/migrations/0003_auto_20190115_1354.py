# Generated by Django 2.1.5 on 2019-01-15 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottery', '0002_prize_is_exclude'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='guest',
            field=models.BooleanField(default=False, help_text='嘉宾不参与`其他`奖项的抽奖', verbose_name='是否为嘉宾'),
        ),
        migrations.AlterField(
            model_name='prize',
            name='win_users',
            field=models.ManyToManyField(blank=True, help_text='必中用户. 该用户将必然中得此奖品, 排除用户与必中用户同时存在时, 该用户为必中用户', related_name='win_users', to='lottery.User', verbose_name='必中用户'),
        ),
        migrations.AlterField(
            model_name='user',
            name='weights',
            field=models.IntegerField(default=0, help_text='权重为0-100, 权重越高, 中奖机会越高', verbose_name='权重'),
        ),
    ]
