from django.contrib import admin

from main.models import Payment, Collect


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'event',
        'amount',
    )

class CollectAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'reason',
        'description',
        'total',
        'start',
        'end',
    )

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Collect, CollectAdmin)
