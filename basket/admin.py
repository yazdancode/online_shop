from django.contrib import admin
from basket.models import Basket, BasketLine


class BasketInLine(admin.TabularInline):
    model = BasketLine


class BasketAdmin(admin.ModelAdmin):
    list_display = ["user", "created_time"]
    inlines = (BasketInLine,)


admin.site.register(Basket, BasketAdmin)
