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
### 1. publisher's
- Debes abrir una terminal por cada publisher. En esta tarea hay **5 publisher** que representan ciudades.
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

### 2. Subscriber
- Se encarga de enviar los eventos que se encuentran en *events.json* que contienen datos mínimos de sismos.

  ```bash
  python3 publisher.py
  ```
