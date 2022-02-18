from django.db import models
from django.contrib.auth.models import User


# class Usuarios(User):
#     class Meta:
#         db_table = "usuarios"


class Perfiles(models.Model):
    imagen = models.ImageField(null=True)
    link = models.URLField(null=True)
    descripcion = models.TextField(null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "perfiles"


class Paginas(models.Model):
    titulo = models.CharField(max_length=40, null=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="accounts/img/")
    fecha_posteo = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Paginas"
