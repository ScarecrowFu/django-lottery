from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class User(models.Model):
    # 参与抽奖的用户
    serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="编号", help_text='可空')
    name = models.CharField(max_length=255, verbose_name="姓名")
    group = models.CharField(max_length=255, null=True, blank=True, verbose_name="部门")
    weights = models.IntegerField(default=0, verbose_name="权重", help_text="权重为0-100, 权重越高, 中奖机会越高")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "参与用户"
        verbose_name_plural = "参与用户"


class PrizeClass(models.Model):
    # 奖项
    name = models.CharField(max_length=255, verbose_name="类型名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "奖项"
        verbose_name_plural = "奖项"


class Prize(models.Model):
    # 奖品
    prize_class = models.ForeignKey(PrizeClass, related_name='prize_class', null=True, verbose_name="所属奖项", on_delete=models.SET_NULL)
    img = models.ImageField(default='prize/default.png', blank=True, null=True,  upload_to="prize", verbose_name='图片')
    name = models.CharField(max_length=255, verbose_name="奖品名称")
    number = models.IntegerField(default=1, verbose_name="中奖人数")
    prohibited_users = models.ManyToManyField(User, verbose_name="排除用户", blank=True, related_name='prohibited_users',
                                              help_text="排除用户, 该用户将不参与此奖品的抽奖")
    win_users = models.ManyToManyField(User, verbose_name="必中用户", blank=True, related_name='win_users',
                                       help_text="必中用户. 该用户将必然中得此奖品, 排除用户与必中用户同时存在时, 该用户为必中用户")
    is_exclude = models.BooleanField(default=True, verbose_name="是否排除已中奖用户", help_text="默认排除已中奖用户")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "奖品"
        verbose_name_plural = "奖品"
