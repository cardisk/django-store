from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from .models import User

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ProfileView(LoginRequiredMixin, UpdateView):
    """
    A view for users to view and edit their profile.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        """
        Returns the logged-in user
        """
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your profile has been updated successfully!')
        return response