from django.contrib import admin
from django.contrib.admin import TabularInline
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from .models import Organisation, Group, Replacement, \
    ReplacementStatus, ReplacementEmployee, BreakStatus, Break



class RaplacementEmployeeInLine(TabularInline):
    fields = ('employee', 'status',)
    model = ReplacementEmployee


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director',)
    search_fields = ('name',)
    filter_horizontal = ('employees',)
    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'min_active', 'replacement_count',)
    search_fields = ('name__startswith',)
    autocomplete_fields = ('organisation',)

    list_select_related = ('organisation',)

    readonly_fields = (
        'created_at', 'created_by', 'updated_at', 'updated_by',
    )

    def replacement_count(self, obj):
        return obj.replacement_count

    replacement_count.short_description = 'Кол-во смен'

    def get_queryset(self, request):
        queryset = Group.objects.annotate(
            replacement_count=Count('replacements__id')
        )
        return queryset


@admin.register(ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'sort', 'is_active',
    )


@admin.register(BreakStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'sort', 'is_active',
    )


@admin.register(Replacement)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group', 'date', 'break_start', 'break_end', 'break_max_duration'
    )

    inlines = (
        RaplacementEmployeeInLine,
    )


@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'replacement_link', 'break_start', 'break_end', 'status',
    )
    list_filter = ('status',)
    empty_value_display = 'Unknown'
    radio_fields = {'status': admin.VERTICAL}
    list_select_related = ('replacement', 'employee', )

    def replacement_link(self, obj):
        '''Определяем ссылку для перехода на смену а не на обеденный перерыв
        common_replacement_change - означает приложение_модель_изменение'''
        link = reverse(
            'admin:common_replacement_change', args=[obj.replacement.id]
        )
        return format_html('<a href="{}">{}</a>', link, obj.replacement)

