# coding: utf-8
# Team : Quality Management Center
# Author：llh
# Date ：2020/6/18 15:23
# Tool ：PyCharm

from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def filter_all(art_dic, k):
    if k == 'category_id':
        val1 = art_dic['category_id']
        val2 = art_dic['article_type_id']
        if val1 == 0:
            ret = '<a class="active" href="/article-0-%s.html">全部</a>' % val2
        else:
            ret = '<a href="/article-0-%s.html">全部</a>' % val2
    else:
        val1 = art_dic['article_type_id']
        val2 = art_dic['category_id']
        if val1 == 0:
            ret = '<a class="active" href="/article-%s-0.html">全部</a>' % val2
        else:
            ret = '<a href="/article-%s-0.html">全部</a>' % val2
    return mark_safe(ret)


@register.simple_tag
def filter_category(category_list, art_dic):
    ret = []
    for row in category_list:
        print(row)
        if row[0] == art_dic['category_id']:
            temp = '<a class="active" href="/article-%s-%s.html">%s</a>' % (row[0], art_dic['article_type_id'], row[1],)
        else:
            temp = '<a href="/article-%s-%s.html">%s</a>' % (row[0], art_dic['article_type_id'], row[1],)
        ret.append(temp)
    return mark_safe(''.join(ret))


@register.simple_tag
def filter_article_type(article_type_list, art_dic):
    ret = []
    for row in article_type_list:
        if row[0] == art_dic['article_type_id']:
            temp = '<a class="active" href="/article-%s-%s.html">%s</a>' % (art_dic['category_id'], row[0], row[1],)
        else:
            temp = '<a href="/article-%s-%s.html">%s</a>' % (art_dic['category_id'], row[0], row[1],)
        ret.append(temp)
    return mark_safe(''.join(ret))
