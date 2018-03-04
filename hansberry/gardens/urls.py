from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views


urlpatterns = [
    path(r'', views.index, name='index'),
    path('mygardens/', views.GardenOwnerListView.as_view(), name='my-gardens'),
    path('<int:pk>', views.GardenDetailView.as_view(), name='garden-detail'),
    path('create/', views.GardenCreateView.as_view(), name='garden-create'),
    path('<int:pk>/update', views.GardenUpdateView.as_view(), name='garden-update'),
    path('<int:pk>/delete', views.GardenDeleteView.as_view(), name='garden-delete')
]

urlpatterns += staticfiles_urlpatterns()
