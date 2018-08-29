from django.contrib import admin
from .models import OAuthyb
# Register your models here.

@admin.register(OAuthyb)
class OauthybAdmin(admin.ModelAdmin):
    list_display = ('user', 'yb_id')