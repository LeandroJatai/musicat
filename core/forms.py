from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset
from django import forms
from django.utils.translation import ugettext_lazy as _

from core.models import Classe
from crispy_layout_mixin import MusicatFormLayout, to_row


class ClasseForm(forms.ModelForm):

    class Meta:
        model = Classe
        fields = ['titulo']

    def __init__(self, *args, **kwargs):

        row1 = to_row([
            ('titulo', 12),
        ])

        self.helper = FormHelper()
        self.helper.layout = MusicatFormLayout(
            row1)

        super(ClasseForm, self).__init__(*args, **kwargs)
