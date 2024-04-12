from django.contrib import admin
from menu.models import Menu

# Register your models here.


class RootMenu(admin.SimpleListFilter):
    title = "Меню"
    parameter_name = 'filter'

    def lookups(self, request, model_admin):
        return [('menu', 'Менюшки'),
                ('items', 'Всё содержимое')
                ]

    def queryset(self, request, queryset):
        if self.value() == 'menu':
            return queryset.filter(parent__isnull=True)
        elif self.value() == 'items':
            return queryset.filter(parent__isnull=False)
        else:
            return queryset


@admin.register(Menu)
class Menu(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'url')
    list_filter = (RootMenu, )
    fieldsets = (
        (None, {
            'fields': (('parent',), 'title', 'url')
        }),
    )
