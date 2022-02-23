from os import device_encoding
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect

from .models import *
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Decorador por defecto
from django.contrib.auth.decorators import login_required


# @login_required
# def template_contacto_admin(request):
#     return render(
#         request,
#         "contacto-admin.html",
#         {
#             "nombre": request.user.first_name,
#             "apellido": request.user.last_name,
#             "correo": request.user.email,
#         },
#     )

def acerca_de_mi (request):
    return render(request, "acerca_de_mi.html")


@login_required
def template_perfil(request):
    perfil = None
    datos = {}
    try:
        perfil = Perfiles.objects.get(usuario=request.user)
        datos = {
            "img": str(perfil.imagen) if perfil.imagen is not None else "img.png",
            "usuario": request.user.username,
            "correo": request.user.email,
            "descripcion": perfil.descripcion,
            "link": perfil.link,
            "pwd": request.user.password,
        }
        print("esta imagen se va a colocar en el img", str(perfil.imagen))
    except Exception as e:
        print("No se pudo obtener los perfiles ", str(e))

    return render(request, "perfil.html", datos)


@login_required
def template_actualizar_contenido(request, id):
    pagina = Paginas.objects.get(id=id)
    return render(
        request,
        "actualizar_post.html",
        {
            "titulo": pagina.titulo,
            "img": pagina.imagen,
            "contenido": pagina.contenido,
            "id": id,
        },
    )


def template_login(request):
    return render(request, "login.html")


@login_required
def template_obtener_paginas(request):
    paginas = Paginas.objects.select_related("usuario").filter(usuario=request.user)
    return render(
        request, "paginas.html", {"cantidad_paginas": len(paginas), "paginas": paginas}
    )


@login_required
def template_crear_post(request):
    return render(request, "post.html")


def template_crear_user(request):
    return render(request, "crear_usuario.html")


@login_required
def template_inicio(request):
    return render(
        request,
        "inicio.html",
        {
            "message": "Bienvenido ",
            "usuario": request.user.username,
            "nombre": request.user.first_name,
            "apellido": request.user.last_name,
            "correo": request.user.email,
        },
    )


@login_required
def contenido_pagina(request, id):
    pagina = Paginas.objects.get(id=id)
    # return render(request, "contenido_pagina.html", {"html": pagina.contenido})
    html = f"""
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Contenido de la página</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
            </head>

            <body>
                <div class='box'>
                    {pagina.contenido}
                </div>
            </body>

            </html>
    """
    return HttpResponse(f"{html}")


@login_required
def actualizar_contenido_post(request, id):
    datos = request.POST.dict()
    datos = {
        "imagen": datos.get("img"),
        "titulo": datos.get("titulo"),
        "contenido": datos.get("contenido"),
    }

    pagina = Paginas.objects.filter(id=id).update(**datos)
    print(f"se actualizo {pagina} pagina/s")
    return HttpResponseRedirect("/blog/accounts/paginas/")


@login_required
def eliminar_contenido(request, id):
    pagina = Paginas.objects.get(id=id).delete()
    return HttpResponseRedirect("/blog/accounts/paginas/")


@login_required
def actualizar_post(request, id):
    datos = request.POST.dict()
    pagina = Paginas.objects.get(id=id).update(**datos)
    return HttpResponseRedirect("/blog/accounts/paginas/")


@login_required
def crear_post(request):
    datos = request.POST.dict()
    pagina = Paginas.objects.create(
        titulo=datos.get("titulo"),
        usuario=request.user,
        contenido=datos.get("contenido"),
        imagen=datos.get("img"),
    )

    return HttpResponseRedirect("/blog/accounts/paginas/")


def crear_usuario(request):
    datos = request.POST.dict()
    if datos.get("pwd") != datos.get("pwd2"):
        datos.update({"message": "Error. Las contraseñas no son iguales"})
        return render(request, "crear_usuario.html", datos)
    else:
        from django.db.models import Q

        existe_correo = True
        correo = User.objects.filter(
            Q(email=datos.get("correo")) & Q(username=datos.get("usuario"))
        )
        if len(correo) == 0:
            existe_correo = False
        if existe_correo:
            datos.update({"usuario_creado": True})
            return render(request, "crear_usuario.html", datos)
        # print(datos.get("img"))
        usuario = User.objects.create(
            username=datos.get("usuario"),
            password=make_password(datos.get("pwd")),
            email=datos.get("correo"),
            first_name=datos.get("nombre"),
            last_name=datos.get("apellido"),
        )
        print(f"usuario creado satisfactoriamnete {usuario}")
        perfil = Perfiles.objects.create(
            imagen=request.FILES.get("img"),
            descripcion=datos.get("descripcion"),
            link=datos.get("link"),
            usuario=usuario,
        )
        login(request, usuario)
        return HttpResponseRedirect("/blog/accounts/inicio/")


def inicio_session(request):
    user_autenticado = authenticate(
        username=request.GET.get("user"), password=request.GET.get("pwd")
    )
    if user_autenticado is not None:
        login(request, user_autenticado)
        return render(
            request,
            "inicio.html",
            {"message": "Bienvenido ", "usuario": request.user.username, "nombre": request.user.first_name,
             "apellido": request.user.last_name,
             "correo": request.user.email},
        )
    else:
        return render(
            request, "login.html", {"message": "Usuario y/o contraseña incorrecta"}
        )


@login_required
def logout_usuario(request):
    logout(request)
    return HttpResponseRedirect("/blog/accounts/template_login")


@login_required
def actualizar_datos(request):
    datos = request.POST.dict()
    perfil = Perfiles.objects.select_related("usuario").get(usuario=request.user)
    if datos.get("usuario") != request.user.username:
        request.user.username = datos.get("usuario")
        request.user.save()
    if datos.get("pwd") != request.user.password:
        request.user.set_password(datos.get("pwd"))
    if datos.get("correo") != request.user.email:
        request.user.email = datos.get("correo")
        request.user.save()
    if datos.get("descripcion") != perfil.descripcion:
        perfil.descripcion = datos.get("descripcion")
        perfil.save()
    if datos.get("link") != perfil.link:
        perfil.link = datos.get("link")
        perfil.save()
    try:
        if request.FILES.get("img") != perfil.imagen:
            perfil.imagen = request.FILES.get("img")
            perfil.save()
    except:
        pass
    return HttpResponseRedirect("/blog/accounts/perfil/")


@login_required
def eliminar_perfil(request):
    request.user.delete()
    return HttpResponseRedirect("/blog/accounts/template_login/")
