# Arquitectura 2

Esta arquitectura considera un “url shortener” que, al recibir una petición GET con una URL corta, este responderá con el “response redirect” y un código HTTP 301, que indica que la redirección es permanente, permitiendo que el navegador pueda guardar en su caché la redirección.

## Tácticas arquitectónicas

- Controlar arribo de eventos por medio de un rate limiter en LiteStar
- Mantener múltiples copias de datos por medio del caching de las peticiones recibidas por el servicio LiteStar.

## Dependencias

Las dependencias se pueden instalar utilizando el archivo requirements.txt

```shell
pip install -r requirements.txt
```

Dependencias utilizadas:

- litestar[standard]
