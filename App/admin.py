from django.contrib import admin
from .models import *
# Register your models here.
# ------------------------------------------------------------------
# TableName   : Nation
# Description : 국가 테이블
# ------------------------------------------------------------------
@admin.register(Nation)
class NationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Nation._meta.fields]

# ------------------------------------------------------------------
# TableName   : Validate
# Description : 문자인증 테이블
# ------------------------------------------------------------------
@admin.register(Validate)
class ValidateAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Validate._meta.fields]

# ------------------------------------------------------------------
# TableName   : UserProfile
# Description : 유저 프로필 테이블
# ------------------------------------------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UserProfile._meta.fields]

# ------------------------------------------------------------------
# TableName   : Site
# Description : 사이트 테이블
# ------------------------------------------------------------------
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Site._meta.fields]

# ------------------------------------------------------------------
# TableName   : CheckLog
# Description : 사이트 체크 로그 테이블
# ------------------------------------------------------------------
@admin.register(CheckLog)
class CheckLogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CheckLog._meta.fields]


# ------------------------------------------------------------------
# TableName   : Order
# Description : 주문 정보 테이블
# ------------------------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Order._meta.fields]


