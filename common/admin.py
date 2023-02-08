from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Organisation, Group, Replacement, ReplacementStatus, ReplacementEmployee



class RaplacementEmployeeInLine(TabularInline):
    fields = ('employee', 'status',)
    model = ReplacementEmployee


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director',)


@admin.register(Group)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'min_active',)

@admin.register(ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'sort', 'is_active',
    )\


@admin.register(Replacement)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group', 'date', 'break_start', 'break_end', 'break_max_duration'
    )

    inlines = (
        RaplacementEmployeeInLine,
    )
