from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('AstronomicalEvent', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def like_count(self):
        return self.like_set.count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} comentó en {self.photo.title}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')
    
    def __str__(self):
        return f'{self.user.username} likes {self.photo.title}'

class AstronomicalEvent(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    
    def __str__(self):
        return self.name

class PhotoOfTheDay(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
    date = models.DateField()

class PhotoOfTheMonth(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
    month = models.DateField()

class PhotoOfTheYear(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
    year = models.DateField()
