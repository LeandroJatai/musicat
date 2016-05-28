from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.list import ListView

from core.models import Classe


# Create your views here.
class ClasseListView(ListView):
    model = Classe
    paginate_by = 10
    verbose_name = model._meta.verbose_name
    verbose_name_plural = model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.setdefault('title', self.verbose_name_plural)
        return context

    @property
    def create_url(self):
        return reverse_lazy('core:classe_list')
