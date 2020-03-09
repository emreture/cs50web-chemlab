from django.contrib import admin
from django.forms import TextInput
from .models import *
# Register your models here.


admin.site.register(TestMethod)
admin.site.register(Product)
admin.site.register(Sample)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ["get_sample_number", "get_result"]
    list_filter = ["sample__receipt_date", "sample__product", "sample__number"]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': "10"})}
    }

    def get_sample_number(self, obj):
        return obj.sample.number
    get_sample_number.short_description = "Sample number"
    get_sample_number.admin_order_field = "sample"

    def get_result(self, obj):
        return f"{obj.test_method.name}, {obj.result} {obj.test_method.unit}"
    get_result.short_description = "Test Result"
    get_result.admin_order_field = "test_method"

    class Meta:
        model = Result
