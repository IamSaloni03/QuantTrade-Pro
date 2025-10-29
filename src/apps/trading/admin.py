from django.contrib import admin

# Register your models here.

from .models import Asset, Portfolio, Trade

admin.site.register(Asset)
admin.site.register(Portfolio)
admin.site.register(Trade)

