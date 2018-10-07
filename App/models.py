from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

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

# ------------------------------------------------------------------
# TableName   : Validate
# Description : 문자인증 테이블
# ------------------------------------------------------------------
class Validate(models.Model):
    number = models.CharField(max_length=64, verbose_name="전화번호")
    code = models.IntegerField(verbose_name="확인코드")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일자")

    def __str__(self):
        return str(self.number)+" 문자 인증"

# ------------------------------------------------------------------
# TableName   : UserProfile
# Description : 유저 프로필 테이블
# ------------------------------------------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="유저")
    customer_uid = models.UUIDField(default=uuid4, editable=False)
    birth = models.CharField(max_length=8, verbose_name="생년월일")
    phone = models.CharField(max_length=32, verbose_name="전화번호")
    billing = models.BooleanField(default=False, verbose_name="빌링등록여부")

    def __str__(self):
        return str(self.user) + " 프로필"

# ------------------------------------------------------------------
# TableName   : Site
# Description : 사이트 테이블
# ------------------------------------------------------------------
class Site(models.Model):
    class Meta:
        unique_together = ("user", "url")

    STATUS_CHOICES = (
        ('ready', '미결제'),
        ('paid', '결제완료'),
        ('cancelled', '결제취소'),
        ('failed', '결제실패'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="유저")
    name = models.CharField(max_length=32, verbose_name="사이트명")
    url = models.CharField(max_length=255, verbose_name="사이트URL")
    merchant_uid = models.UUIDField(default=uuid4, editable=False)
    imp_uid = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="ready", verbose_name="상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="주문일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일자")

    def __str__(self):
        return str(self.user) + " : " + str(self.name)