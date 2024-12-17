from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Photo, Comment, Like, AstronomicalEvent
from .forms import PhotoForm
from rest_framework import generics
from .serializers import PhotoSerializer

# Página de bienvenida
class WelcomeView(TemplateView):
    template_name = 'welcome.html'

# Lista de fotos
class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 12

# Detalle de la foto
class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(photo=self.object)
        context['like_count'] = Like.objects.filter(photo=self.object).count()
        return context
    
    def get_object(self, queryset = None):
        photo = super().get_object(queryset)
        photo.visits += 1
        photo.save()
        return photo

# Crear un comentario
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(user=request.user, photo=photo, comment=comment_text)
        return redirect('photo-detail', pk=pk)

# Manejar likes
class LikePhotoView(LoginRequiredMixin, View):
    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, photo=photo)
        if not created:
            like.delete()  # Si ya existe el like, lo eliminamos
        return redirect('photo-detail', pk=pk)

# Crear una nueva foto
class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo_form.html'
    success_url = reverse_lazy('photo-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Editar una foto existente
class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/photo_form.html'
    success_url = reverse_lazy('photo-list')

    def get_queryset(self):
        # Solo permite editar fotos del usuario actual
        return Photo.objects.filter(user=self.request.user)

# Eliminar una foto
class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'
    success_url = reverse_lazy('photo-list')

    def get_queryset(self):
        # Solo permite eliminar fotos del usuario actual
        return Photo.objects.filter(user=self.request.user)
    

# Lista de eventos astronómicos
class AstronomicalEventListView(ListView):
    model = AstronomicalEvent
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 10

# Detalle de evento con fotos asociadas
class AstronomicalEventDetailView(DetailView):
    model = AstronomicalEvent
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(event=self.object)
        return context

# Busqueda
class SearchView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'photos'

    def get_queryset(self):
        titles = self.request.GET.get('titles', '')
        if titles:
            return Photo.objects.filter(title__icontains=titles)
        return Photo.objects.all()

# Registro de usuarios
class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('photo-list')
        return render(request, 'registration/signup.html', {'form': form})
    
#Api http://127.0.0.1:8000/api/
class PhotoListAPIView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
