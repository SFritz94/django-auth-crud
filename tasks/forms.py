#Formulario personalizado
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task#Le indicamos a que modelo se refiere este formulario.
        fields = ['title', 'description', 'important']#Le indicamos los campos que va a mostrar el form
        widgets = {#Forma de estilizar los formularios creados por uno mismo
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }