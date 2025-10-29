from django.contrib import admin

# Register your models here.

from .models import MarketData, NewsFeed

admin.site.register(MarketData)
admin.site.register(NewsFeed)

