from django.contrib import admin

from .models import Good, Price, TradeAdmin, Transaction

admin.site.register(Transaction)
admin.site.register(Good)
admin.site.register(Price)
admin.site.register(TradeAdmin)
