from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MusicatModelMixin(models.Model):
    created = models.DateTimeField(
        verbose_name=_('created'),
        editable=False, auto_now_add=True)

    modifier = models.ForeignKey(
        User, verbose_name=_('modifier'), related_name='+')

    class Meta:
        abstract = True


class Classe(models.Model):
    titulo = models.CharField(max_length=256, verbose_name=_('Título'))

    class Meta:
        verbose_name = _('Classe')
        verbose_name_plural = _('Classes')

    def __str__(self):
        return self.titulo


class Musica(models.Model):
    uri = models.CharField(max_length=100, verbose_name=_('URI'))

    class Meta:
        verbose_name = _('Música')
        verbose_name_plural = _('Músicas')

    def __str__(self):
        return self.uri


class MusicaHistory(MusicatModelMixin):
    musica = models.ForeignKey(
        Musica, verbose_name=_('Música'), related_name='historico_musica_set')
    titulo = models.CharField(max_length=256, verbose_name=_('Título'))

    classes = models.ManyToManyField(Classe)

    class Meta:
        verbose_name = _('Música')
        verbose_name_plural = _('Músicas')

    def __str__(self):
        return self.titulo


class Versao(models.Model):
    musica = models.ForeignKey(
        Musica, verbose_name=_('Música'), related_name='versoes_set')

    class Meta:
        verbose_name = _('Versão')
        verbose_name_plural = _('Versões')

    def __str__(self):
        return self.uri


class VersaoHistory(MusicatModelMixin):
    versao = models.ForeignKey(
        Versao, verbose_name=_('Versão'), related_name='historico_versao_set')
    descr = models.CharField(max_length=256, verbose_name=_('Descrição'))
    texto = models.TextField(verbose_name=_('Texto'))

    class Meta:
        verbose_name = _('Versão')
        verbose_name_plural = _('Versões')

    def __str__(self):
        return self.descr
