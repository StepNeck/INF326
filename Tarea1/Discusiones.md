## Discusiones

### 1. Trade-off en la arquitectura implementada

- ### Ventajas
  * **Mantenibilidad**: El Publisher no necesita conocer a los Subscriber, lo que reduce el acoplamiento. Esto facilita agregar o eliminar suscriptores sin modificar el Publisher, mejorando la mantenibilidad y la capacidad de adaptación del sistema.

  * **Escalabilidad**: La arquitectura permite escalado horizontal debido a la facilidad de añadir subscriptores.

  * **Usabilidad**: Los mensajes son enviados a los subscriptores de forma asíncrona evitando bloquear al Publisher, lo que permite enviar múltiples eventos simultáneamente y garantizar que los reciba la región más cercana.

  * **Reusabilidad**: La solución permite que otros sistemas reutilicen la arquitectura para otros fenómenos naturales (ej. Tsunamis o incendios) haciendo leves modificaciones.

- ### Desventajas
  * **Fiabilidad**: La propia naturaleza del patrón hace que exista un riesgo de pérdida de mensajes si los suscriptores fallan esto debido a la comunicación asíncrona. Los mensajes pueden perderse o ser susceptibles a corrupciones. 

  * **Trazabilidad limitada** (Fiabilidad): Es complejo verificar que todos los eventos llegaron efectivamente a cada destino, lo que es crítico en un sistema que alerta emergencias.

  * **Disponibilidad**: En caso de múltiples réplicas de sismos seguidas, algunos mensajes pueden retrasarse. Esto genera inconsistencias temporales cr´ticas en un sistema de emergencias.



### 2. “Back of the Envelope” del sistema para estimar su uso y justificar la propuesta
Se podría utilizar esta estrategia para ver si la arquitectura soporta la carga esperada y puede entregar respuestas en tiempo requerido. Por ejemplo tomando la cantidad de subscriptores por la cantidad de mensajes esperados por día según la cantidad de sismos relevantes, además se puede tener en cuenta el tamaño de los mensajes para calcular el ancho de banda; y la distribución de los subscriptores para estimar si las alertas llegarán en un tiempo razonable, por ejemplo, [entre 6 a 12 segundos](https://www.usgs.gov/data/data-release-latency-testing-wireless-emergency-alerts-intended-shakealert-earthquake-early).

