### Integrantes
- Cristóbal Benavides - 202073106-3 - cristobal.benavidesp@usm.cl
- Raúl Cuello - 201903007-8 - raul.cuello@sansano.usm.cl
- Kevin Vega - 202073064-4 - kevin.vega@usm.cl
---

## 1. Explicación del Trabajo realizado
> **Suposición 1:** El sistema que pide desarrollar la tarea es del tipo Bitly donde su función principal es el servicio de acortamiento de URL.

> **Suposición 2:** Cómo la arquitectura 1 y 2 son nodos distintos, se hace el supuesto que "Shortener DB" es individual para cada arquitectura y solo fue un alcance de nombre en el esquema.

Ambas arquitecturas implementan la misma API REST con dos endpoints principales (POST /shorten y GET /{hash_code}), pero difieren en su diseño interno, composición de servicios y tecnologías complementarias:

### Arquitectura 1
La Arquitectura 1 implementa un sistema distribuido de acortamiento de URLs compuesto por tres servicios principales:

-  Shortener (API principal) → genera y gestiona URLs cortas.
- Redis → almacena las asociaciones entre URLs cortas y largas.
- Log Service (gRPC) → registra cada acceso a una URL corta en un servicio de logs externo.

Redirige con código 302 (Found), indicando una redirección temporal.

### Arquitectura 2

Está compuesta por dos servicios:

- api: servicio web principal (maneja acortamiento, redirecciones y cacheo).
- redis: base de datos en memoria para almacenamiento y cache.

Implementa las mismas rutas REST que la Arquitectura 1, pero:

- Añade Rate Limiting (máximo 5 solicitudes/minuto).
- Añade Response Cache con Redis (respuestas cacheadas 60 segundos).

Redirige con código 301 (Moved Permanently), ideal para SEO y caché de navegador.

## 2. Instalación

### Debe tener Docker instalado! (obligatorio)

## 3. Ejecución

> **_NOTA:_** Debe estar ejecutándose Docker en el sistema.
### 1. La carpeta raíz debe ser "Tarea2".

### 2. Para ejecutar la arquitectura 1:
    
    docker-compose -f arquitectura-1/docker-compose.yml up -d --build

### 3. Para ejecutar la arquitectura 2:
    
    docker-compose -f arquitectura-2/docker-compose.yml up -d --build


## 4. Tabla de Endpoints

Ambas arquitecturas implementan los mismos endpoints y formato de comunicación.  
La **única diferencia** para consumirlos es el **puerto del servicio**:

- **Arquitectura 1:** `http://localhost:8000`
- **Arquitectura 2:** `http://localhost:8080`

| Método | Endpoint | Descripción | Cuerpo / Parámetros | Respuesta esperada | Código de estado |
|---------|-----------|--------------|----------------------|--------------------|------------------|
| `POST` | `/shorten` | Genera una URL corta a partir de una URL larga. | **Body (JSON):**<br>`{ "url": "https://www.youtube.com/watch?v=IfqhToJsYEs" }` | **Body (JSON):**<br>`{ "short_url": "http://localhost:8000/eRgfR" }` | `200 OK` o `500 Internal Server Error` |
| `GET` | `/{short_hash}` | Redirige a la URL larga correspondiente al hash. | **Parámetro de ruta:** `short_hash` (ej. `http://localhost:8080/eRgfT`) | Redirección HTTP a la URL original | `302 Found` o `404 Not Found` |
|||||
