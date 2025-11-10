# Arquitectura 2

Esta arquitectura considera un “url shortener” que, al recibir una petición GET con una URL corta, este responderá con el “response redirect” y un código HTTP 301, que indica que la redirección es permanente, permitiendo que el navegador pueda guardar en su caché la redirección.

## Tácticas arquitectónicas

- Controlar arribo de eventos por medio de un rate limiter en LiteStar
- Mantener múltiples copias de datos por medio del caching de las peticiones recibidas por el servicio LiteStar.

## Configurar entorno virtual

> **_NOTA:_** Si ya tiene un fichero .venv, omitir este paso.

Crear un entorno virtual

```bash
python -m venv .venv
```

Activar entorno virtual

Windows

```Powershell
.venv\Scripts\Activate.ps1
```

Linux/MacOS

```Linux/MacOS
source .venv/bin/activate
```

> **_NOTA:_** Habilitar ejecución de scripts si no funciona el comando anterior.

Entrar a powershell como administrador

```bash
Set-ExecutionPolicy Unrestricted
```

## Iniciar base de datos Redis

```shell
docker compose up -d
```

## Instalar dependencias

1. Entrar en la ruta de la carpeta api

```shell
cd ./api
```

2. Instalar dependencias

```shell
pip install -r requirements.txt
```

## Ejecución

- Iniciar api

```shell
litestar run
```

## Endpoints

- "/": Recibe solicitudes POST
  - Parámetros del body:
    - long_url: url larga que se desea acortar
  - Parámetros del response:
    - short_url: url acortada
- "/{hashcode}": Recibe peticiones GET
  - Parámetros de la url:
    - hashcode: hash que permite acceder a las url's largas
  - Response: Redirect hacia la url larga
