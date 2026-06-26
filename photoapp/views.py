#gpt 5.5 assisted in the creation of this code

'''Photo app generic views'''

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import Photo



class PhotoListView(ListView):
    model = Photo
    template_name = 'photoapp/list.html'
    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    template_name = 'photoapp/taglist.html'

    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        #the tag value from the URL is passed to the ORM as a parameterised filter, never concatenated into raw SQL. This makes the lookup safe from SQL injection by construction.
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photoapp/detail.html'
    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    #Authentication required (LoginRequiredMixin):
    #an anonymous request is redirected to LOGIN_URL with a ?next= parameter instead of being allowed to create content.
    model = Photo

    #'user' is deliberately ABSENT from this field list.
    #The owner is assigned server-side from the authenticated session (see form_valid below) and is never read from the submitted form. This blocks a mass-assignment / object-ownership-forgery attack where a user POSTs a 'user' field to create content "as" somebody else.
    fields = ['title', 'description', 'image', 'tags']

    template_name = 'photoapp/create.html'
    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        # Trusted assignment: request.user is set by Django's authentication middleware from the signed session cookie and cannot be spoofed by form input.
        form.instance.user = self.request.user
        return super().form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Defense in depth: two layered server-side gates run before any edit:
    #1. LoginRequiredMixin  - must be authenticated, else redirect to login.
    #2. UserPassesTestMixin - must pass test_func, else 403 Forbidden.
    template_name = 'photoapp/update.html'
    model = Photo
    fields = ['title', 'description', 'tags']
    success_url = reverse_lazy('photo:list')

    def test_func(self):
        #object-level access control / least privilege.
        #Complete mediation: this runs on the SERVER for every request, regardless of whether the UI happened to show an "Edit" link.
        #Fail-safe default: access is granted ONLY if the requester owns the object OR is an administrator (is_staff). 
        #Every other case: a non-owner, or an object with no owner evaluates to False = denied.
        photo = self.get_object()
        return self.request.user == photo.user or self.request.user.is_staff


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'photoapp/delete.html'
    model = Photo
    success_url = reverse_lazy('photo:list')

    def test_func(self):
        # Same ownership-or-admin rule as update: one access policy, applied identically to both destructive operations.
        photo = self.get_object()
        return self.request.user == photo.user or self.request.user.is_staff


class SignUpView(CreateView):
    #registration uses Django's built-in UserCreationForm, which hashes passwords with encryption and runs AUTH_PASSWORD_VALIDATORS to reject weak passwords.
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
