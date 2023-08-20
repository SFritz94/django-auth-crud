from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)#Permite que el campo no tenga contenido
    date_created = models.DateTimeField(auto_now_add=True)#Crea la fecha y la hora actual a menos que le pasemos la fecha
    date_completed = models.DateTimeField(null=True, blank=True)#Campo vacio inicialmente
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)#Relaciono la tabla con el id del usuario o modelo que se le pase.
    
    def __str__(self):
        return f"{self.title} - assigned to {self.user.username}"