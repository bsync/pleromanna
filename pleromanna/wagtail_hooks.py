from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Series, SubSeries


class SeriesAdmin(ModelAdmin):
    model = Series
    menu_label = 'Series'  # ditch this to use verbose_name_plural from model
    menu_icon = 'list-ul'  # change as required
    menu_order = 500  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add to the Settings sub-menu
    exclude_from_explorer = True  # or True to exclude from Wagtail's explorer
    list_display = ('title', 'start_date', 'stop_date')
    list_filter = ('title',)
    search_fields = ('title',)


class SubSeriesAdmin(ModelAdmin):
    model = SubSeries
    menu_label = 'SubSeries'
    menu_icon = 'list-ul'  # change as required
    menu_order = 500  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add to the Settings sub-menu
    exclude_from_explorer = True  # or True to exclude from Wagtail's explorer
    list_display = ('title', 'start_date', 'stop_date')
    list_filter = ('title',)
    search_fields = ('title',)


#modeladmin_register(SeriesAdmin)
#modeladmin_register(SubSeriesAdmin)
