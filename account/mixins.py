from django.http import Http404


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ('author', 'title', 'slug', 'description', 'category', 'status', 'publish', 'image')
        elif request.user.is_author:
            self.fields = ('title', 'slug', 'description', 'category', 'publish', 'image')
        else:
            raise Http404('You cant access this page')
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'Draft'
        return super().form_valid(form)