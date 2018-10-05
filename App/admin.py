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