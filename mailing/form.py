from django import forms
from mailing.models import Mailing, Client

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['clients', 'user', 'is_active']:
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),  # Получаем всех клиентов
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Mailing
        exclude = ['user', 'is_active']

    def __init__(self, *args, user=None, **kwargs):  # Добавляем user как аргумент
        super().__init__(*args, **kwargs)
        # Теперь вы можете использовать user, если это необходимо
        # Например, если вы хотите делать что-то с user, вы можете добавить логику здесь

    def clean_day(self):
        cleaned_data = self.cleaned_data['day']
        if not (1 <= cleaned_data <= 31):
            raise forms.ValidationError('Число должно быть от 1 до 31')
        return cleaned_data
