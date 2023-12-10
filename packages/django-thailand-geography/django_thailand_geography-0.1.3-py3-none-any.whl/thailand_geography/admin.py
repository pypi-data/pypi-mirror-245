from django.contrib import admin

from .models import Province, District, Subdistrict


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_en', 'name_th')
    search_fields = ('name_en', 'name_th')


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'name_en', 'name_th')
    search_fields = ('name_en', 'name_th', 'province__name_en', 'province__name_th')
    list_select_related = ('province',)


class SubdistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'district', 'name_en', 'name_th')
    search_fields = (
        'name_en', 'name_th', 'province__name_en', 'province__name_th', 'district__name_en', 'district__name_th',
    )
    list_select_related = ('district__province',)

    def province(self, obj):
        return obj.get_province()


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Subdistrict, SubdistrictAdmin)
