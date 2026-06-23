'''Photo app generic views'''

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .models import Photo

class PhotoListView(ListView):
    
    model = Photo     

    template_name = 'photoapp/list.html'

    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    
    template_name = 'photoapp/taglist.html'
    
    # Custom function
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context
     

class PhotoDetailView(DetailView):

    model = Photo

    template_name = 'photoapp/detail.html'

    context_object_name = 'photo'


class PhotoCreateView(CreateView):

    model = Photo
    
    fields = ['title', 'description', 'image', 'tags']

    template_name = 'photoapp/create.html'
    
    success_url = reverse_lazy('photo:list')

class PhotoUpdateView(UpdateView):
    
    template_name = 'photoapp/update.html'

    model = Photo

    fields = ['title', 'description', 'tags']
    
    success_url = reverse_lazy('photo:list')

class PhotoDeleteView(DeleteView):
    
    template_name = 'photoapp/delete.html'

    model = Photo

    success_url = reverse_lazy('photo:list')
