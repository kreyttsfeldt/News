from django import template

from news.models import Category
from django.db.models import Count, F
from django.core.cache import cache

register = template.Library()  # регитрация тэга.


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(
            cnt__gt=0)  # отображать непустые категории, в цифрах фильтровать неопубликованные
    cache.set('categories', categories, 60)
    return {"categories": categories}
