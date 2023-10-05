from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class task_user(models.Model):
    first_name = models.CharField(max_length=100, )
    last_name = models.CharField(max_length=100, )
    email = models.EmailField(max_length=200, )
    password = models.IntegerField()
   

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low' , 'Low'),
        ('medium' , 'Medium'),
        ('high' , 'High')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.CharField()
    photos = models.ManyToManyField('Photo', blank=True, related_name='task_photos')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('task_detail', args=[str(self.id)])

    
class Photo(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='task_photos/')

    def __str__(self):
        return self.image.name
    
    @property
    def image_url(self):
        return self.image.url
