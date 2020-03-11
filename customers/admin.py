from django.contrib import admin
from .models import Customer

# Register your models here.


# admin.site.register(Customer)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "get_users"]
    list_filter = ["users"]

    def get_users(self, obj):
        return list(obj.users.all())
    get_users.short_description = "Users"

    class Meta:
        model = Customer
