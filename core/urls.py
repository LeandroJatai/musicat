from django.conf.urls import include, url
from core.views import ClasseListView, ClasseCreateView, ClasseUpdateView,\
    MusicaImportView, MusicaListView, MusicaDetailView

from .apps import AppConfig


app_name = AppConfig.name


urlpatterns = [


    url(r'^$', MusicaListView.as_view(), name='musica_list'),

    url(r'^config/classe/$', ClasseListView.as_view(), name='classe_list'),
    url(r'^config/classe/create',
        ClasseCreateView.as_view(), name='classe_create'),
    url(r'^config/classe/(?P<pk>[0-9]+)/change',
        ClasseUpdateView.as_view(), name='classe_change'),

    url(r'^musica/import',
        MusicaImportView.as_view(), name='musica_import'),


    url(r'^(?P<slug>[\w-]+)/(?P<versao_id>[0-9]*)$',
        MusicaDetailView.as_view(), name='musica_detail'),
]
