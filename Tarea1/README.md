### Integrantes
- Cristóbal Benavides - 202073106-3 - cristobal.benavidesp@usm.cl
- Raúl Cuello - 201903007-8 - raul.cuello@sansano.usm.cl
- Kevin Vega - 202073064-4 - kevin.vega@usm.cl

## Instalación
### 1.  RabbitMQ en Docker:
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

### 2. FastAPI
```bash
pip install "fastapi[standard]" uvicorn
```
> **_NOTA:_**  Si no corre con el comando de arranque, instala uvicorn aparte.

* ### 2.1 Uvicorn
  ```bash
  pip install uvicorn
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
> **_NOTA:_**  Se debe estar ejecutando El container de RabbitMQ en Docker para que el sistema funcione.
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
- Se encarga de enviar los eventos que se encuentran en *events.json* que contienen datos mínimos de sismos.

  ```bash
  python3 publisher.py
  ```
