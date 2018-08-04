from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Lesson

@method_decorator(login_required, name='dispatch')
class UploadView(CreateView):
   model = Lesson
   fields = ['name', 'description', 'recorded', 'theFile' ]
   success_url = reverse_lazy('home')
   context_object_name='lesson'

def get_context_data(self, **kwargs):
   context = super().get_context_data(**kwargs)
   context['lessons'] = Lesson.objects.all()
   return context

class CatalogView(ListView):
   model = Lesson
   paginate_by = 100  
