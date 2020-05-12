from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
approval=[
        ('Assigned','Assigned'),
        ('YES','Completed'),
        ('NO','NOt completed')
    ]
app_name='blog'
class Post(models.Model):
    assigned_employee = models.ForeignKey(User, on_delete=models.CASCADE)

    work = models.CharField(max_length=50)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    deadline=models.CharField(max_length=100)
    status=models.CharField(max_length=10, choices=approval,default='assigned')
    
    

    def get_absolute_url(self):
        #print(reverse('post-detail',kwargs={'pk':self.pk}))
        #print(reverse('post-detail',args=[self.id]))
        return reverse('post-detail',kwargs={'pk':self.pk})

