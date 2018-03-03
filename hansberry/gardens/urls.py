from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views


urlpatterns = [
    path(r'', views.index, name='index'),
    path('mygardens/', views.GardensOwnerListView.as_view(),
         name='my-gardens'),
    path('<int:pk>', views.GardenDetailView.as_view(), name='garden-detail'),
]

urlpatterns += staticfiles_urlpatterns()
