from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf.urls import url, include
from mainapp.models import ProductCategory, Products
from django.http import HttpResponseRedirect
from django.conf.urls import url
# from monitor.models import LoginMonitor
# from monitor.import_custom import ImportCustom
#
#
# @admin.register(LoginMonitor)
# class LoginMonitorAdmin(admin.ModelAdmin):
#     change_list_template = "admin/monitor_change_list.html"
#
#     def get_urls(self):
#         urls = super(LoginMonitorAdmin, self).get_urls()
#         custom_urls = [url('^import/$', self.process_import, name='process_import'), ]
#         return custom_urls + urls
#
#     def process_import_btmp(self, request):
#         import_custom = ImportCustom()
#         count = import_custom.import_data()
#         self.message_user(request, f"создано {count} новых записей")
#         return HttpResponseRedirect("../")


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_description', 'is_visible')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('is_visible',)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category', 'is_visible')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'category')
    list_filter = ('category', 'is_visible')
    list_editable = ('price', 'quantity', 'category', 'is_visible')

    # def get_urls(self):
    #     urls = super(MenuOrderAdmin, self).get_urls()

    # def button(self, obj):
    #     return mark_safe(f'<a class="button" >Кнопка</a>')


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Products, ProductsAdmin)

