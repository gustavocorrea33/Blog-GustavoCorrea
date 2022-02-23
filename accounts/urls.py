from django.urls import path
from .views import (
    template_crear_post,
    template_login,
    template_crear_user,
    template_perfil,
    template_inicio,
    template_obtener_paginas,
    # template_contacto_admin,
    template_actualizar_contenido,
    crear_usuario,
    inicio_session,
    logout_usuario,
    actualizar_datos,
    eliminar_perfil,
    crear_post,
    contenido_pagina,
    eliminar_contenido,
    actualizar_contenido_post,
    acerca_de_mi,

)

app_name = "accounts"

urlpatterns = [
    path(
        "accounts/pagina/actualizar/<int:id>",
        template_actualizar_contenido,
        name="actualizar-contenido",
    ),
    path("perfil/", template_perfil, name="perfil"),
    path("inicio/", template_inicio, name="inicio"),
    # path("contactar_administrador/", template_contacto_admin, name="contacto-admin"),
    path("accounts/", template_crear_post, name="post"),
    path("paginas/", template_obtener_paginas, name="paginas"),
    path("template_login/", template_login),
    path("template_crear_usuario/", template_crear_user, name="crear-usuario"),
    path(
        "accounts/pagina/actualizar/contenido/<int:id>",
        actualizar_contenido_post,
        name="actualizar-contenido-post",
    ),
    path(
        "accounts/pagina/eliminar/<int:id>",
        eliminar_contenido,
        name="eliminar-contenido",
    ),
    path("mostrar/<int:id>", contenido_pagina, name="contenido"),
    path("crear_post/", crear_post, name="crear-post"),
    path("login", inicio_session, name="login"),
    path("crear_usuario/", crear_usuario, name="logica-crear-usuario"),
    path("deslogearse/", logout_usuario, name="logica-logout"),
    path("actualizar_datos/", actualizar_datos, name="actualizar-datos"),
    path("elimnar_perfil", eliminar_perfil, name="eliminar-perfil"),
    path("about/", acerca_de_mi, name="acerca-de-mi")
]
