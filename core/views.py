from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView
from account.models import User
from django.views import View
from .models import *


class ArticleList(View):
    template_name = 'base/home.html'

    def get(self, request, slug=None):
        articles = Article.objects.filter(status='Published').order_by('-publish')
        paginator = Paginator(articles, 3)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        categories = Category.objects.filter(is_sub=False)
        if slug:
            category = get_object_or_404(Category, slug=slug)
            page_obj = articles.filter(category=category)
        return render(request, self.template_name, {'articles': page_obj, 'categories': categories})


class ArticleDetail(View):
    template_name = 'base/article_detail.html'

    def get(self, request, slug, id):
        article = get_object_or_404(Article, slug=slug, id=id)
        return render(request, self.template_name, {'article': article})


class AuthorList(View):
    template_name = 'base/author_list.html'

    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        articles = Article.objects.filter(author=author)
        paginator = Paginator(articles, 2)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        return render(request, self.template_name, {'author': author, 'articles': page_obj})

    
    