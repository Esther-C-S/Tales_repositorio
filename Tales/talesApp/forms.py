from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class': 'form-control'})
    )
    biografia = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Biografía', 'class': 'form-control'}),
        required=False
    )
    ciudad = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ciudad', 'class': 'form-control'}),
        required=False
    )
    foto_perfil = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha de nacimiento', 'class': 'form-control'}),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'fecha_nacimiento', 'password1', 'password2']