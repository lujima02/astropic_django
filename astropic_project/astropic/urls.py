from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    WelcomeView, PhotoListView, PhotoDetailView, AddCommentView, LikePhotoView, AstronomicalEventListView, AstronomicalEventDetailView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView, SearchView, SignupView, PhotoListAPIView,
)

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('photos/', PhotoListView.as_view(), name='photo-list'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
    path('photo/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('photo/<int:pk>/like/', LikePhotoView.as_view(), name='like-photo'),
    path('photo/create/', PhotoCreateView.as_view(), name='photo-create'),
    path('photo/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo-edit'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo-delete'),
    path('events/', AstronomicalEventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', AstronomicalEventDetailView.as_view(), name='event-detail'),
    path('photo-search/', SearchView.as_view(), name='photo-search'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='photo-list'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('api/', PhotoListAPIView.as_view(), name='api_photo_list'),
]
