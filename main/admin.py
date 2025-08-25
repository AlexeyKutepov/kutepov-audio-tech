from django import forms
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from main.models import Feedback, Subscriber, Post, ProductInfo, ProductImage, ContactLink
from ckeditor_uploader.widgets import CKEditorUploadingWidget



@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    """
    Сообщение из формы обратной связи
    """
    list_display = ('email', 'message', 'datetime', )
    list_filter = ('email', 'datetime', )


@admin.register(Subscriber)
class Subscriber(admin.ModelAdmin):
    list_display = ('email', 'is_subscribed', 'datetime',)
    list_filter = ('email', )


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)

class ProductInfoAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    short_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Краткое описание для карточки товара"
    )

    class Meta:
        model = ProductInfo
        fields = '__all__'
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'update_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Преобразуем строки дат в объекты datetime с учетом временной зоны
        for field in ['datetime', 'update_date']:
            if field in cleaned_data and isinstance(cleaned_data[field], str):
                try:
                    cleaned_data[field] = timezone.datetime.fromisoformat(cleaned_data[field])
                except (ValueError, TypeError):
                    cleaned_data[field] = timezone.now()
        return cleaned_data
    

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview', 'order')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" width="100" height="100" style="object-fit: contain;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Превью"


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    form = ProductInfoAdminForm
    inlines = [ProductImageInline]
    list_display = ('display_image', 'name', 'category', 'price', 'old_price', 'available', 'is_published', 'created_at')
    list_display_links = ('display_image', 'name')
    list_filter = ('category', 'available', 'is_published', 'datetime')
    search_fields = ('name', 'short_text', 'description')
    readonly_fields = ('display_image_preview', 'created_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'url', 'category', 'image', 'display_image_preview')
        }),
        ('Дополнительные изображения', {
            'fields': (),
            'description': 'Управление дополнительными изображениями доступно ниже после сохранения продукта'
        }),
        ('Цены и наличие', {
            'fields': ('price', 'old_price', 'available')
        }),
        ('Ссылки', {
            'fields': ('vk_url', 'telegram_url')
        }),
        ('Описания', {
            'fields': ('short_text', 'description')
        }),
        ('Публикация', {
            'fields': ('is_published', ('created_at'))
        }),
    )
    date_hierarchy = 'datetime'
    ordering = ('-datetime',)
    list_per_page = 20
    actions = ['make_published', 'make_unpublished', 'set_available', 'set_unavailable']
    save_on_top = True

    def display_image(self, obj):
        content = []
        if obj.image and hasattr(obj.image, 'url'):
            content.append(format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;"/>', 
                obj.image.url
            ))
        
        additional_count = obj.images.count()
        if additional_count:
            content.append(format_html(
                '<div style="background: #f0ad4e; border-radius: 50%; width: 20px; height: 20px; '
                'text-align: center; color: white; position: absolute; top: -5px; right: -5px;">{}</div>',
                additional_count
            ))
        
        return format_html(
            '<div style="position: relative; display: inline-block;">{}</div>',
            mark_safe(''.join(content))
        ) if content else "-"
    display_image.short_description = "Изображения"

    def display_image_preview(self, obj):
        images = []
        if obj.image and hasattr(obj.image, 'url'):
            images.append(format_html(
                '<div style="float: left; margin-right: 20px;"><h4>Главное изображение</h4>'
                '<img src="{}" width="200" style="object-fit: contain;"/></div>', 
                obj.image.url
            ))
        
        additional = obj.images.all()
        if additional:
            additional_html = []
            for idx, img in enumerate(additional, 1):
                if img.image and hasattr(img.image, 'url'):
                    additional_html.append(
                        f'<div style=\"float: left; margin-right: 10px;\">'
                        f'<img src=\"{img.image.url}\" width=\"100\" style=\"object-fit: contain;\"/>'
                        f'<p>Изображение #{idx}</p></div>'
                    )
            if additional_html:
                images.append(format_html(
                    '<div style="clear: both; padding-top: 20px;"><h4>Дополнительные изображения</h4>{}</div>',
                    mark_safe(''.join(additional_html))
                ))
        
        return format_html('<div>{}</div>', mark_safe(''.join(images))) if images else "-"
    display_image_preview.short_description = "Все изображения продукта"

    @admin.display(description="Создан")
    def created_at(self, obj):
        return obj.datetime

    @admin.action(description="Опубликовать выбранные товары")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации выбранные товары")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Отметить как 'В наличии'")
    def set_available(self, request, queryset):
        queryset.update(available=True)

    @admin.action(description="Отметить как 'Нет в наличии'")
    def set_unavailable(self, request, queryset):
        queryset.update(available=False)
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images')


@admin.register(ContactLink)
class ContactLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "icon_class", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "url")
    list_filter = ("is_active",)
