## Instalación

### 1. RabbitMQ en Docker:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

### 2. FastAPI

### 2.1 Configurar entorno virtual

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

### 2.2 Instalar FastAPI

```bash
pip install "fastapi[standard]"
```

### 2.3 Iniciar API

```bash
fastapi dev main.py
```

### 3. RabbitMQ en Docker

```bash
docker run -d --name rabbitmq \
-p 5672:5672 -p 15672:15672 \
rabbitmq:4-management
```

### 4. Paquetes

```bash
pip install -r requirements.txt
```

## Ejecución

> **_NOTA:_** Se debe estar ejecutando El container de RabbitMQ en Docker para que el sistema funcione.

### 1. Subscriber's

- Debes abrir una terminal por cada publisher. En esta tarea hay **5 Subscriber's** que representan ciudades.

  - Arica
  - Coquimbo
  - Valparaiso
  - Concepcion
  - PuntaArenas

  en cada terminal debes ejecutar el siguiente comando.

  ```bash
  python3 subscriber.py <ciudad>
  ```

  \<ciudad> deben reemplazarlo por alguno de los nombres en la lista anterior.

### 2. Publisher

- Se encarga de enviar los eventos que se encuentran en _events.json_ que contienen datos mínimos de sismos.

  ```bash
  python3 publisher.py
  ```
