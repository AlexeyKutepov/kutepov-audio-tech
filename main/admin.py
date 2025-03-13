from django.contrib import admin
from main.models import Feedback, Subscriber, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


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