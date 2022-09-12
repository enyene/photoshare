from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from . models import Photo

from hitcount.models import HitCount
from hitcount.views import HitCountMixin

# Create your views here.
def home(request):
    return render(request, 'home.html')

import requests

url = "https://google-maps-search1.p.rapidapi.com/place-photos"

querystring = {"google_id":"0x89c259b5a9bd152b:0x31453e62a3be9f76","limit":"5"}

headers = {
	"X-RapidAPI-Key": "1a9e7fd576mshb3fa339ddb0b6c1p1edfdajsnb94f8d3f94fe",
	"X-RapidAPI-Host": "google-maps-search1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

#count = ViewedPhoto.post_view(self=ViewedPhoto)

class PhotoListView(ListView):
    model = Photo
    template_name = 'core/list.html'
    context_object_name = 'photos'
   


# class PhotoSearchListView(ListView):
#     model = Photo
#     template_name = 'core/list.html'
#     context_object_name = 'photos'
   
class PhotoSearchView(PhotoListView):
    model = Photo
    template_name = 'core/search.html'
    context_object_name = 'photos'
    photos = []
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Photo.objects.filter(name__icontains=self.args[0])
        else:
               return messages.info(self.request, "You didn't search for any photo.")
 
class PhotoTagListView(PhotoListView):
    template_name = 'core/taglist.html'
    def get_queryset(self):
        return Photo.objects.filter(tags__name=self.kwargs['tag'])


    def get_tag(self):
        return self.kwargs['tag']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.get_tag()
        return context

class PhotoDetailView(DetailView):
    template_name = 'core/detail.html'
    model = Photo
    context_object_name = 'photo'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        context.update({
        'popular_posts':Photo.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context


class PhotoCreateView(CreateView,LoginRequiredMixin):
    model = Photo
    template_name = 'core/create.html'
    fields = ['title','image','tags','location']
    success_url = reverse_lazy('core:list')
    context_object_name= 'photo'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # def post(self, request):
    #     photos = Photo.objects.all()
    #     res = response.json()
    #     photos.image = res['data'][0]['photo_url']
        
    #     return render(request, self.template_name, {'photos': photos}) 

    # def get_queryset(self):
    #     return Photo.objects.all()
    
class UserPhoto(UserPassesTestMixin):
    def get_photo(self):
        return get_object_or_404(Photo, slug=self.kwargs.get('slug'))

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().user
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserPhoto,UpdateView):
    model = Photo
    template_name = 'core/update.html'
    fields = ['title', 'image','tags']
    success_url = reverse_lazy('core:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PhotoDeleteView(UserPhoto,DeleteView):
    model = Photo
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:list')