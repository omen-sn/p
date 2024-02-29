from django import template
from django.db.models import Count

import stockcontrol.views as views
from stockcontrol.models import Category, TagProduct

register = template.Library()


@register.inclusion_tag('stockcontrol/list_categories.html')
def show_categories(cat_selected=0):
    #cats = Category.objects.annotate(total=Count('products')).filter(total__gt=0)
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('stockcontrol/list_tags.html')
def show_all_tags():
    #return {'tags': TagProduct.objects.annotate(total=Count("tags")).filter(total__gt=0git)}
    return {'tags': TagProduct.objects.all()}
