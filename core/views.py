from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Greatest
from django.views.generic import DetailView
from django.views.generic import ListView
from django.core.paginator import Paginator
from datetime import timedelta, datetime
from django.db.models import Count, Q
from django.contrib import messages
from urllib.parse import urlencode
from account.models import User
from django.views import View
from account.mixins import *
from .filters import *
from .models import *
from .forms import *
from . import tasks


class ArticleList(View):
	template_name = 'base/home.html'

	def get(self, request, slug=None):
		articles = Article.objects.published()
		fltr = ProductFilter(request.GET, queryset=articles)
		articles = fltr.qs
		paginator = Paginator(articles, 3)
		page_num = request.GET.get('page')
		data = request.GET.copy()
		if 'page' in data:
			del data['page']
		page_obj = paginator.get_page(page_num)
		categories = Category.objects.filter(is_sub=False)
		if slug:
			category = get_object_or_404(Category, slug=slug)
			page_obj = articles.filter(category=category)
		form = SearchForm()
		if 'search' in request.GET:
			form = SearchForm(request.GET)
			if form.is_valid():
				data = form.cleaned_data['search']
				page_obj = articles.annotate(similarity=Greatest(
					TrigramSimilarity('title', data),
					TrigramSimilarity('description', data)
					),).filter(similarity__gt=0.3).order_by('-similarity')
		context = {'articles': page_obj, 'categories': categories,
								'form': form, 'filter': fltr, 'data': urlencode(data)}
		return render(request, self.template_name, context)


class ArticleDetail(View):
	template_name = 'base/article_detail.html'

	def get(self, request, slug, id):
		article = get_object_or_404(Article, slug=slug, id=id)
		fav = False
		if article.favourite.filter(id=request.user.id).exists():
			fav = True
		ip_address = self.request.user.ip_address
		if ip_address not in article.visit_count.all():
			article.visit_count.add(ip_address)
						
		return render(request, self.template_name, {'article': article, 'fav': fav})


class ArticlePreview(AuthorAccessMixin, DetailView):
	template_name = 'base/article_preview.html'

	def get_object(self):
		pk = self.kwargs['pk']
		return get_object_or_404(Article, pk=pk)


class AuthorList(View):
	template_name = 'base/author_list.html'

	def get(self, request, username):
		author = get_object_or_404(User, username=username)
		articles = Article.objects.filter(author=author)
		paginator = Paginator(articles, 2)
		page_num = request.GET.get('page')
		page_obj = paginator.get_page(page_num)
		return render(request, self.template_name, {'author': author, 'articles': page_obj})

		
class FavouriteList(LoginRequiredMixin, View):
	template_name = 'base/favourite_list.html'
	login_url = 'account:login'

	def get(self, request):
		articles = Article.objects.filter(favourite=True)
		return render(request, self.template_name, {'articles': articles})




def add_favourite(request, id):
	url = request.META.get('HTTP_REFERER')
	article = get_object_or_404(Article, id=id)
	fav = False
	if article.favourite.filter(id=request.user.id).exists():
		article.favourite.remove(request.user)
		fav = False
	else:
		article.favourite.add(request.user)
		fav = True
	return redirect(url)
				

class BucketObjects(LoginRequiredMixin, View):
	template_name = 'base/bucket.html'
	login_url = 'account:login'

	def get(self, request):
		if not request.user.is_superuser:
			return redirect('/')
		objects = tasks.get_objects_list_tasks()
		return render(request, self.template_name, {'objects': objects})


class DownloadObject(LoginRequiredMixin, View):
	login_url = 'account:login'

	def get(self, request, key):
		url = request.META.get('HTTP_REFERER')
		tasks.download_object_tasks.delay(key)
		messages.success(request, 'your demand will be response soon', 'success')
		return redirect(url)
				

class DeleteObject(LoginRequiredMixin, View):
	login_url = 'account:login'

	def get(self, request, key):
		url = request.META.get('HTTP_REFERER')
		tasks.delete_object_tasks.delay(key)
		messages.success(request, 'your demand will be response soon', 'success')
		return redirect(url)
