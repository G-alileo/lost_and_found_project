from django.contrib import admin

from .models import Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    inlines = []




class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 0
    fields = ("name", "created_by", "created_at")
    readonly_fields = ("created_at",)


CategoryAdmin.inlines = [SubCategoryInline]



@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "created_by", "created_at")
    search_fields = ("name", "category__name")
    list_filter = ("created_at", "category")


