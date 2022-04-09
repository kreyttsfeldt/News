from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from django import forms
from .models import News, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_published', 'category', 'views',
                    'get_photo')  # что надо видеть
    list_display_links = ('id', 'title')  # чтобы поля стали ссылками
    search_fields = ('title', 'content')  # добавить поиск по полям
    list_editable = ('is_published',)  # чтобы можно было редактировать интерактивно
    list_filter = ('is_published', 'category')  # чтобы можно было фильтровать

    fields = ('title', 'content', 'created_at', 'updated_at', 'is_published', 'category', 'views',
              'get_photo', 'photo')  # для просмотра одной новости
    readonly_fields = ('created_at', 'updated_at', 'views', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')  # неэкранирование html


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')  # что надо видеть
    list_display_links = ('id', 'title')  # чтобы поля стали ссылками
    search_fields = ('title',)  # добавить поиск по полям


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
