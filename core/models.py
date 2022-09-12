from urllib import request
from django.db import models
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin,HitCount
#from ipware import get_client_ip
import random
import geocoder



# Create your models here.

Token ='pk.eyJ1IjoiaWVueWVuZSIsImEiOiJjbDVwYzV3bW0wcmp6M2lvZWRmamN4cnV3In0.G3yaMn224wCZg4kS1CMbnQ'

class Photo(models.Model,HitCountMixin):
    title =models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='photos')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='photo_user')
    tags = TaggableManager()
    location = models.CharField(max_length=200, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    hit_count_generic = GenericRelation(HitCount,object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')
    # location TODOO
    #def get_absolute_url(self):
        #return reverse('photo_detail', args=[self.slug])

    def current_hit_count(self):
        return self.hit_count_generic.hit_count()

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title + "-" + str(random.randint(10000,99999)))
        g =geocoder.mapbox(self.location,key=Token)
        g = g.latlng
        self.lat = g[0]
        self.lon = g[1]
        super(Photo,self).save(*args,**kwargs)

    class Meta:
        ordering = ['-created']

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[-1].strip()
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# class ViewedPhoto(models.Model):
#     photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='viewed_photo')
#     ip = models.CharField(max_length=20)
    

#     def __str__(self):
#         return self.photo.title

#     def post_view(self):
#         viewed_photo,created = ViewedPhoto.objects.get_or_create(photo=self.photo)
#         if created:
#             counter = viewed_photo.photo.count
#             counter += 1
#             return counter
#         return False