from django.db import models
from public.models import CommonInfo


# Create your models here.

class Env(CommonInfo):
    eid = models.IntegerField(unique=True, verbose_name="环境序号")

    class Meta:
        db_table = 'env'
