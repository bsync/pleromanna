from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .models import Upload, PrivateUpload

class DocumentCreateView(CreateView):
    model = Upload
    fields = ['theFile', ]
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploads'] = Upload.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class PrivateDocumentCreateView(CreateView):
    model = PrivateUpload
    fields = ['theFile', ]
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
