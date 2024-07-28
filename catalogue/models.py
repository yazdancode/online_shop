from django.db import models
from django.core.exceptions import ValidationError


class IsActiveManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        return super().get_queryset(*args, **kwargs).select_related("category", "brand")

    def actives(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).filter(is_active=True)

    def deactives(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).exclude(is_active=True)


class IsActiveCategoryManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        return super().get_queryset(*args, **kwargs).filter(category__is_active=True)


class ProductType(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"
        ordering = ["title"]

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    INTEGER = 1
    STRING = 2
    FLOAT = 3

    ATTRIBUTE_TYPES_FIELDS = (
        (INTEGER, "Integer"),
        (STRING, "String"),
        (FLOAT, "Float"),
    )

    title = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute_type = models.PositiveSmallIntegerField(
        default=INTEGER, choices=ATTRIBUTE_TYPES_FIELDS
    )

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sub_brands",
    )

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    upc = models.BigIntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, related_name="category_products", on_delete=models.CASCADE
    )
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE)

    default_manager = models.Manager()
    objects = IsActiveManager()
    is_active_category_manager = IsActiveCategoryManager()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["title"]

    def __str__(self):
        return self.title

    @property
    def stock(self):
        return self.partners.all().order_by("price").first()


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attribute_values"
    )
    value = models.CharField(max_length=48)
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.PROTECT, related_name="values"
    )

    class Meta:
        verbose_name = "Product Attribute Value"
        verbose_name_plural = "Product Attribute Values"
        ordering = ["product", "attribute"]

    def clean(self):
        if self.attribute.attribute_type == ProductAttribute.INTEGER:
            if not self.value.isdigit():
                raise ValidationError("Value must be an integer.")
        elif self.attribute.attribute_type == ProductAttribute.FLOAT:
            try:
                float(self.value)
            except ValueError:
                raise ValidationError("Value must be a float.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} ({self.attribute}): {self.value}"
