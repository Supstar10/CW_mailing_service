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
        queryset=Client.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Mailing
        exclude = ['user', 'is_active']

    def __init__(self, *args, **kwargs):
        # Получаем пользователя из kwargs, если он там есть
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Устанавливаем queryset для поля clients
        if user is not None:
            self.fields['clients'].queryset = Client.objects.filter(owner=user)

    def clean_day(self):
        cleaned_data = self.cleaned_data['day']
        if not (1 <= cleaned_data <= 31):
            raise forms.ValidationError('Число должно быть от 1 до 31')
        return cleaned_data
