from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views


urlpatterns = [
    path(r'', views.index, name='index'),
    path('mygardens/', views.GardensCreatedByUserListView.as_view(),
         name='my-gardens'),
]

urlpatterns += staticfiles_urlpatterns()
