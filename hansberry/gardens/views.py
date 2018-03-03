from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from hansberry.gardens.models import Garden

# Create your views here.


def index(request):
    return render(request, 'gardens/index.html')


class GardensOwnerListView(LoginRequiredMixin, ListView):
    """
    Generic class-based view listing gardens created by current user.
    """
    model = Garden
    template_name = 'gardens/gardens_list_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Garden.objects.filter(garden_author=self.request.user)
