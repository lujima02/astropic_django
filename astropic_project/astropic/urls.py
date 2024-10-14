from django.urls import path
from .views import (
    PhotoListView, PhotoDetailView, AddCommentView, LikePhotoView, AstronomicalEventListView, AstronomicalEventDetailView
)

urlpatterns = [
    path('', PhotoListView.as_view(), name='photo-list'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('photo/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('photo/<int:pk>/like/', LikePhotoView.as_view(), name='like-photo'),
    path('events/', AstronomicalEventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', AstronomicalEventDetailView.as_view(), name='event-detail'),
]
