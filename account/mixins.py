from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from core.models import Article


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ('author', 'title', 'slug', 'description', 'category', 'is_special', 'status', 'publish', 'image')
        elif request.user.is_author:
            self.fields = ('title', 'slug', 'description', 'category', 'is_special', 'publish', 'status', 'image')
        else:
            raise Http404('You cant access this page')
        return super().dispatch(request, *args, **kwargs)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['r', 'd'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('You cant access this page')


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)


class SuperUserMixin():
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser or request.user.is_author:
            return super().dispatch(request, *args, **kwargs)
        raise Http404('You can not access this page')


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser or request.user.is_author:
            return super().dispatch(request, *args, **kwargs)
        return redirect('account:profile')