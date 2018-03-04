from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from hansberry.gardens.models import Garden

# Create your views here.


def index(request):
    return render(request, 'gardens/index.html')


class GardenActionMixin:
    """
    Mixin that queues up a confirmation message corresponding
    to the action performed in a view as well as capturing
    the user who created the form instance.
    """

    fields = ['name', 'description', 'address']

    @property
    def success_msg(self):
        return NotImplemented
    
    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        form.instance.created_by = self.request.user
        return super(GardenActionMixin, self).form_valid(form)


class GardensOwnerListView(LoginRequiredMixin, ListView):
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
    success_msg = 'Garden created!'


class GardenUpdateView(LoginRequiredMixin, GardenActionMixin, UpdateView):
    """
    Generic class-based view that allows a logged in user
    to update a garden and displays a success message
    """
    model = Garden
    success_msg = 'Garden updated!'


class GardenDeleteView(LoginRequiredMixin, GardenActionMixin, DeleteView):
    """
    Generic class-based view that allows a logged in user
    to delete a garden and displays a success message
    """
    model = Garden
    success_msg = 'Garden deleted!'
    success_url = reverse_lazy('my-gardens')

