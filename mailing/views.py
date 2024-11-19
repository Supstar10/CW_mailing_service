from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from mailing.form import MailingForm
from mailing.models import Mailing, Client


def index(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(is_active=True).count()
    unique_clients = Client.objects.values('email').distinct().count()
    random_articles = Blog.objects.order_by('?')[:3]

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_articles': random_articles,
    }
    return render(request, "mailing/index.html", context)


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'  # Укажите ваш шаблон
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user  # Устанавливаем пользователя для рассылки
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    fields = ("date_time", "frequency", "status", "clients", "message")
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = (
        "mailing.can_block_user",
        "mailing.can_disable_mailing",
        "mailing.can_view_mailing",
    )

    def get_object(self, queryset=None):
        mailing = get_object_or_404(Mailing, id=self.kwargs["pk"])
        print(mailing.owner, self.request.user)
        if mailing.owner != self.request.user:
            raise PermissionDenied("У вас нет прав редактировать рассылку")
        return mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = 'mailing.delete_mailing'
