from django.contrib import admin
from store.models import Store

# Register your models here.

class StoreAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'created_at']

    class Meta:
        model = Store


admin.site.register(Store, StoreAdmin)

