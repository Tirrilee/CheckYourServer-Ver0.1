from django.db import models

# Create your models here.
# ------------------------------------------------------------------
# TableName   : Nation
# Description : 국가 테이블
# ------------------------------------------------------------------
class Nation(models.Model):
    name = models.CharField(max_length=64, verbose_name="국가명")
    flag = models.CharField(max_length=255, verbose_name="국기")
    callcode = models.CharField(max_length=8, verbose_name="국가번호")

    def __str__(self):
        return str(self.name)