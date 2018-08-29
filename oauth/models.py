from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OAuthyb(models.Model):
    """yb and User Bind"""
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)   # 关联用户信息表
    yb_id = models.CharField(max_length=64)   # yb_id
