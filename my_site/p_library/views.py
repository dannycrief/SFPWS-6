from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import Book, Redaction, Authors, UserProfile
from .forms import AuthorForm, BookForm, ProfileCreationForm
from django.views.generic import CreateView, ListView, FormView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect
from allauth.socialaccount.models import SocialAccount


def index_redirect(request):
    return redirect('library/', request)


def profile(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        try:
            context['github_url'] = SocialAccount.objects.get(
                provider='github',
                user=request.user
            ).extra_data['html_utl']
            try:
                context['age'] = SocialAccount.objects.get(
                    provider='github',
                    user=request.user
                ).extra_data['age']
            except:
                context['age'] = ''
        except:
            context['age'] = UserProfile.objects.get(user=request.user).age
            context['github_url'] = ''
    return render(request, 'profile.html', context)


class CreateUserProfile(FormView):
    form_class = ProfileCreationForm
    template_name = 'profile-create.html'
    success_url = reverse_lazy('p_library:profile-page')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('p_library:login'))
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        try:
            data = SocialAccount.objects.get(
                provider='github',
                user=self.request.user
            )
            data.extra_data['age'] = str(form['age'].value())
            data.save()
        except:
            instance.user = self.request.user
            instance.save()
        return super(CreateUserProfile, self).form_valid(form)


def index(request):
    template = loader.get_template('library.html')
    books = Book.objects.all()
    biblio_data = {
        "title": "my library",
        "books": books,
    }
    return HttpResponse(template.render(biblio_data, request))


@csrf_exempt
def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


@csrf_exempt
def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def redactions(request):
    template = loader.get_template('publishes.html')
    redactions = Redaction.objects.all()
    data = {
        "redactions": redactions,
    }
    return HttpResponse(template.render(data, request))


class AuthorEdit(CreateView):
    model = Authors
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:author_list')
    template_name = 'author_edit.html'


class AuthorList(ListView):
    model = Authors
    template_name = 'author_list.html'


def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            return HttpResponseRedirect(
                reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
    return render(request, 'manage_authors.html', {'author_formset': author_formset})


def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
        request,
        'manage_books_authors.html',
        {
            'author_formset': author_formset,
            'book_formset': book_formset,
        }
    )
