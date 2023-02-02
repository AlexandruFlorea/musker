from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.db.models import Q
from itertools import chain
from .models import Profile, Meep
from .forms import MeepForm


def home(request):
    if request.user.is_authenticated:
        meeps = Meep.objects.all().order_by('-created_at')

        return render(request, 'home.html', {
            'meeps': meeps,
        })
    else:
        return render(request, 'home.html', {})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)

        return render(request, 'profile_list.html', {
            'profiles': profiles
        })
    else:
        messages.warning(request, 'You must be logged in to view this page.')

        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by('-created_at')

        # Post form logic
        if request.method == 'POST':
            # Get current user
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            # save the profile
            current_user_profile.save()

        return render(request, 'profile.html', {
            'profile': profile,
            'meeps': meeps
        })
    else:
        messages.warning(request, 'You must be logged in to view this page.')

        return redirect('home')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('/')

    return render(request, 'register.html', {
        'form': form
    })


class MeepCreateView(CreateView):
    form_class = MeepForm
    model = Meep
    template_name = 'meep_create_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.body)
        return super().form_valid(form)


class MeepUpdateView(UpdateView):
    model = Meep
    fields = ['body']
    template_name = 'meep_update.html'
    success_url = reverse_lazy('home')



class MeepDeleteView(DeleteView):
    model = Meep
    template_name = 'meep_confirm_delete.html'
    success_url = reverse_lazy('home')  # We have to use reverse_lazy() instead of reverse(), as the urls are not loaded when the file is imported.


def search_site(request):
    if request.method == 'POST':
        query = request.POST.get('q')

        if query:
            meeps = Meep.objects.filter(Q(body__icontains=query))
            users = Profile.objects.filter(Q(user__username__icontains=query))

            return render(request, 'search_view.html', {
                'meeps': meeps,
                'users': users
            })
    return redirect(reverse('home'))
