from django.contrib import admin
from lottery.models import User, Prize, PrizeClass
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        import_id_fields = ('serial_number', 'name', 'group',)
        fields = ('serial_number', 'name', 'group', 'weights')


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ('serial_number', 'name', 'group', 'weights')
    search_fields = ('serial_number', 'name', 'group', 'weights')


class PrizeAdmin(admin.ModelAdmin):
    filter_horizontal = ('prohibited_users', 'win_users')
    list_display = ('name', 'prize_class', 'number', )
    search_fields = ('name', 'prize_class',  'number',)


class PrizeClassAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


admin.site.register(User, UserAdmin)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(PrizeClass, PrizeClassAdmin)