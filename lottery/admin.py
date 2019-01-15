from django.contrib import admin
from lottery.models import User, Prize, PrizeClass
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        import_id_fields = ('serial_number', 'name', 'group',)
        fields = ('serial_number', 'name', 'group', 'weights')


class UserAdmin(ImportExportModelAdmin):
    # your normal stuff
    def get_export_formats(self):
        """
        Returns available export formats.
        """
        formats = (
            base_formats.CSV,
            base_formats.XLS,
        )
        return [f for f in formats if f().can_export()]

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        formats = (
            base_formats.CSV,
            base_formats.XLS,
        )
        return [f for f in formats if f().can_import()]

    resource_class = UserResource
    list_display = ('name', 'group', 'weights', 'serial_number')
    search_fields = ('serial_number', 'name', 'group', 'weights')


class PrizeAdmin(admin.ModelAdmin):
    filter_horizontal = ('prohibited_users', 'win_users')
    list_display = ('name', 'prize_class', 'number', 'is_exclude')
    search_fields = ('name', 'prize_class',  'number',)


class PrizeClassAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


admin.site.register(User, UserAdmin)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(PrizeClass, PrizeClassAdmin)