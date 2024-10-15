from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo, Comment, Like, AstronomicalEvent

# Lista de fotos
class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'  # Debes crear este template
    context_object_name = 'photos'
    paginate_by = 12  # Número de fotos por página

# Detalle de la foto
class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'  # Debes crear este template
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(photo=self.object)
        context['like_count'] = Like.objects.filter(photo=self.object).count()
        return context

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
            # Si ya existe el like, lo eliminamos (dislike)
            like.delete()
        like_count = Like.objects.filter(photo=photo).count()
        return redirect('photo-detail', pk=pk)

# Lista de eventos astronómicos
class AstronomicalEventListView(ListView):
    model = AstronomicalEvent
    template_name = 'events/event_list.html'  # Debes crear este template
    context_object_name = 'events'
    paginate_by = 10  # Número de eventos por página

# Detalle de evento con fotos asociadas
class AstronomicalEventDetailView(DetailView):
    model = AstronomicalEvent
    template_name = 'events/event_detail.html'  # Debes crear este template
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(event=self.object)
        return context
