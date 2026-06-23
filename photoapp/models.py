'''Photoapp Models'''

from django.db import models

from taggit.managers import TaggableManager

class Photo(models.Model):
    
    title = models.CharField(max_length=45)
    
    description = models.CharField(max_length=250) 

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    tags = TaggableManager() 

    def __str__(self):
        return self.title
