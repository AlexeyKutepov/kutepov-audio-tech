from django import forms
from django.contrib import admin
from django.utils.html import format_html
from main.models import Feedback, Subscriber, Post, ProductInfo
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
    short_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), help_text="Краткое описание для карточки товара")

    class Meta:
        model = ProductInfo
        fields = '__all__'


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    form = ProductInfoAdminForm
    list_display = ('display_image', 'name', 'category', 'price', 'old_price', 'available', 'is_published', 'created_at')
    list_display_links = ('display_image', 'name')
    list_filter = ('category', 'available', 'is_published', 'datetime')
    search_fields = ('name', 'short_text', 'description')
    readonly_fields = ('display_image_preview', 'created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'url', 'category', 'image', 'display_image_preview')
        }),
        ('Цены и наличие', {
            'fields': ('price', 'old_price', 'available')
        }),
        ('Описания', {
            'fields': ('short_text', 'description')
        }),
        ('Публикация', {
            'fields': ('is_published', ('datetime', 'created_at', 'updated_at'))
        }),
    )
    date_hierarchy = 'datetime'
    ordering = ('-datetime',)
    list_per_page = 20
    actions = ['make_published', 'make_unpublished', 'set_available', 'set_unavailable']
    save_on_top = True

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    display_image.short_description = "Изображение"

    def display_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="object-fit: contain;" />', obj.image.url)
        return "-"
    display_image_preview.short_description = "Предпросмотр изображения"

    def created_at(self, obj):
        return obj.datetime.strftime("%d.%m.%Y %H:%M")
    created_at.short_description = "Создан"

    def updated_at(self, obj):
        return obj.update_date.strftime("%d.%m.%Y %H:%M")
    updated_at.short_description = "Обновлен"

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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['datetime'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        form.base_fields['update_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        return form