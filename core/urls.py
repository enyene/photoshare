from django.urls import path,re_path
from .views import  PhotoListView,PhotoDetailView,PhotoCreateView,PhotoUpdateView,PhotoDeleteView,PhotoTagListView,PhotoSearchView
   

app_name = 'core'
urlpatterns = [
   path('',PhotoListView.as_view(),name='list'),
    path('create/',PhotoCreateView.as_view(),name='create'),
    path('photo/<slug:slug>/',PhotoDetailView.as_view(),name='detail'),
    path('photo/<slug:slug>/update/',PhotoUpdateView.as_view(),name='update'),
    path('photo/<slug:slug>/delete/',PhotoDeleteView.as_view(),name='delete'),
    path('tag/<slug:tag>/',PhotoTagListView.as_view(),name='tag'),
    re_path(r'^search/(\w+)/$', PhotoSearchView.as_view(),name='search'),
]