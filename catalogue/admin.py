from django.contrib import admin
from django.contrib.admin import register
from catalogue.models import Category, Brand, Product, ProductType, ProductAttribute


class ProductAttributeInline(admin.TabularInline):
    """
    Inline class to manage product attributes within the product type admin.
    """

    model = ProductAttribute
    extra = 1


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    """

    list_display = ("upc", "product_type", "is_active", "title", "category", "brand")
    list_display_links = ("title",)
    list_filter = ["is_active"]
    list_editable = ["is_active"]
    search_fields = ["upc", "title", "category__name", "brand__name"]
    actions = ["active_all"]

    def active_all(self, request, queryset):
        """
        Custom admin action to activate all selected products.
        """
        queryset.update(is_active=True)
        self.message_user(
            request, f"{queryset.count()} products were successfully activated."
        )

    active_all.short_description = "Activate selected products"

    def get_list_display(self, request):
        """
        Customize the list display dynamically if needed.
        """
        return self.list_display

    def has_delete_permission(self, request, obj=None):
        """
        Disable delete permission for Product model.
        """
        return False

    # def has_view_permission(self, request, obj=None):
    #     """
    #     Disable view permission for Product model.
    #     """
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     """
    #     Disable change permission for Product model.
    #     """
    #     return False


@register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductType model.
    """

    list_display = ["title", "description"]
    inlines = [ProductAttributeInline]


@register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductAttribute model.
    """

    list_display = ["title", "product_type", "attribute_type"]


admin.site.register(Category)
admin.site.register(Brand)
