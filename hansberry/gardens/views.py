from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from hansberry.gardens.models import Garden
from hansberry.gardens.forms import GardenForm

# Create your views here.


def index(request):
    return render(request, 'gardens/index.html')


class GardenActionMixin:
    """
    Makes the request.user object available
    """

    def get_form_kwargs(self):
        """This method injects forms with keyword args."""
        # grab the current set of form #kwargs
        kwargs = super(GardenActionMixin, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs


class GardenOwnerListView(LoginRequiredMixin, ListView):
    """
    Generic class-based view listing gardens created by current user.
    """
    model = Garden
    template_name = 'gardens/gardens_list_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Garden.objects.filter(created_by=self.request.user)


class GardenDetailView(DetailView):
    """
    Generic class-based view that displays information about a garden
    """
    model = Garden


class GardenCreateView(LoginRequiredMixin, GardenActionMixin, CreateView):
    """
    Generic class-based view that allows a logged in user
    to create a garden and displays a success message
    """
    model = Garden
    form_class = GardenForm


class GardenUpdateView(LoginRequiredMixin, GardenActionMixin, UpdateView):
    """
    Generic class-based view that allows a logged in user
    to update a garden and displays a success message
    """
    model = Garden
    form_class = GardenForm


class GardenDeleteView(LoginRequiredMixin, DeleteView):
    """
    Generic class-based view that allows a logged in user
    to delete a garden and displays a success message
    """
    model = Garden
    success_url = reverse_lazy('my-gardens')
