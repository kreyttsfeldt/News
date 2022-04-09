import django.shortcuts
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def user_logout(request):
    logout(request)
    return django.shortcuts.redirect('login')


def mail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mails = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'antipov.in@gmail.com',
                             ['antipov_in@mail.ru'], fail_silently=False)
            if mails:
                messages.success(request, 'Отправлено.')
                return django.shortcuts.redirect('contact')
            else:
                messages.error(request, 'Ошибка')
        else:
            messages.error(request, 'Ошибка.')
    else:
        form = ContactForm()
    return render(request, 'news/email.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return django.shortcuts.redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации.')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


class CreateUser(CreateView):
    template_name = 'news/register.html'
    success_url = 'login'
    form_class = UserRegisterForm
    success_message = 'Привет'


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return django.shortcuts.redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 3

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # взяли старый контекст
        context['title'] = 'Главная страница'  # добавили свое
        return context

    def get_queryset(self):
        # select_related - для fk
        # refatch что-то там - manytomany
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = Category
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 3
    allow_empty = False  # не показывать пустые списки

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # взяли старый контекст
        context['title'] = Category.objects.get(pk=self.kwargs['category_id']).title  # добавили свое
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    template_name = 'news/news_details.html'
    pk_url_kwarg = 'news_id'  # определяет, что брать за pk
    context_object_name = 'news_item'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


class CreateNews(LoginRequiredMixin, CreateView):  # класс для работы с формами
    login_url = '/login/'
    redirect_field_name = 'login'
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # после добавления новости redirect на нее происходит благодаря методу модели get_absolute_url
    # но можем полностью переопределить атрибут для редиректа:
    # success_url = reverse_lazy('home')  # lazy используется тогда, когда для нее дойдет очередь


# Create your views here.
def index(request):
    news = News.objects.order_by('-created_at')
    context = {'news': news, 'title': 'Список новостей'}
    return render(request, template_name='news/index.html', context=context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, template_name='news/category.html',
                  context=
                  {
                      'news': news,
                      'category': category
                  })


def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})


# Для несвязанной формы
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)  # связанная с данными форма.
#         if form.is_valid():  # проверяем валидацию
#             news = News.objects.create(**form.cleaned_data)
#             return django.shortcuts.redirect(news)
#     else:
#         form = NewsForm()  # не связанная
#     return render(request, 'news/add_news.html', {'form': form})

# Для связанной формы
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)  # связанная с данными форма.
        if form.is_valid():  # проверяем валидацию
            news = form.save()
            return django.shortcuts.redirect(news)
    else:
        form = NewsForm()  # не связанная
    return render(request, 'news/add_news.html', {'form': form})
