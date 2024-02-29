from django.contrib import admin, messages
from .models import  Product, Category, ProductDetail, TagProduct

# Register your models here.
class AdditionalInformationFilter(admin.SimpleListFilter):
    title = 'Additional Information'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('exist', 'exist'),
            ('does_not_exist', 'does not exist')
        ]

    def queryset(self, request, queryset=None):
        if self.value() == 'exist':
            return queryset.filter(detail__isnull=False)
        elif self.value() == 'does_not_exist':
            return queryset.filter(detail__isnull=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    #prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_display = ('id', 'title', 'slug', 'category', 'in_stock', 'date_added', 'is_published', 'brief_info')
    list_display_links = ('id', 'title')
    ordering = ('-date_added',)
    list_editable = ('in_stock',)
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'category__name']
    list_filter = ['category__name', 'is_published', AdditionalInformationFilter]

    @admin.display(description='Total price')
    def brief_info(self, product: Product):
        return f"{product.price * product.in_stock}$"

    @admin.display(description='Publish')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Product.Status.PUBLISHED)
        self.message_user(request, f"{count} entries have been published")

    @admin.display(description='Remove from publication')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Product.Status.DRAFT)
        self.message_user(request, f"{count} entries have been removed from publication", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ('name',)

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'detailed_description')
    list_display_links = ('id', 'detailed_description')
    ordering = ('id',)

@admin.register(TagProduct)
class TagProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tag',)}
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    ordering = ('tag',)
