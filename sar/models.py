from django.db import models
from django.utils import timezone
# Create your models here.


class BaseModel(models.Model):
    class_name = models.CharField(max_length=16, default='design')  # 试验类型
    build_user = models.CharField(max_length=128, default='admin')  # 用户名
    build_time = models.DateTimeField(auto_now_add=True)  # 建立时间
    title = models.CharField(max_length=256, default='随机区组试验')  # 试验名称
class RandomBlockCompletelyDesign(BaseModel):
    block_name = models.CharField(max_length=256)#block名称
    drug_name = models.CharField(max_length=256)#drug名称
    block = models.IntegerField(default=0)#block数量
    drug = models.IntegerField(default=0)#drug数量
class DataProcess(BaseModel):
    path = models.CharField(max_length=256, default='admin')
class DataVision(BaseModel):
    pass
