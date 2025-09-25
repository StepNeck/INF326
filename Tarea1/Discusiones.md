# Discusión acerca de los eventuales trade-offs en la arquitectura implementada y si estos son de consideración o no en el dominio presentado.

## Ventajas

Desacoplamiento: El Publisher no necesita saber quiénes son los subscripciones, por lo que se reduce el acoplamiento al permitir que se envíen mensajes a pesar de que no hayan subscriptores conectados en ese instante, y permite añadir nuevos subscriptores como más regiones o sectores críticos.

Escalabilidad: El sistema puede escalarse fácilmente añadiendo más subscriptores, presenta escalabilidad horizontal que permite la recepción por parte de más subscriptores en distintas regiones del país.

Asincronía: Los mensajes son enviados a los subscriptores de forma asíncrona sin bloquear al publicador, lo cual permite enviar múltiples mensajes a la vez y que los reciba la región más cercana.

Reusabilidad: La arquitectura permite que otros sistemas reutilicen el sistema para otros fenómenos naturales haciendo leves modificaciones, como incendios o tsunamis.

## Desventajas

Complejidad en la gestión de mensajes: Gestionar los mensajes se complica al considerar que un subscriptor se interesa si una alerta ocurre a menos de 500\[km\] de distancia, por lo que no siempre un sismo se notifica al centro más cercano, si no que al subscriptor que se interese primero por la propia lógica del patrón.

Pérdida de mensajes: La propia naturaleza del patrón, con los mensajes asincrónicos, los mensajes pueden perderse, en caso de que los subscriptores en la distancia límite se caigan, o llegar con bits erróneos en la información entregada, como algún valor importante que debe ser mostrado con un valor distinto al original. 

Posibilidad de inundación de mensajes: Estando en Chile, un país sísmico, pueden llegar muchos mensajes a un solo subscriptor según la distribución proveída por el broker. Si los subscriptores no pueden seguir el ritmo de los mensajes del publicador, se genera una contrapresión que puede provocar la pérdida de mensajes si no se gestiona correctamente.

Trazabilidad: Es problemático determinar si una alerta llegó a todos los destinos, lo cual es crítico en un sistema que alerta emergencias.

Consistencia de datos: En caso de que se acumulen muchos mensajes en un corto periodo de tiempo, en caso de muchas réplicas de sismos por ejemplo, puede llegar información atrasada dado que los reportes deben ser inmediatos.

# Discusión acerca de cómo podría utilizar el “Back of the Evelope” del sistema para estimar el uso de este y justificar la arquitectura propuesta
*(no lo calcule; solo discuta cómo sería posible calcular con la información que posee del fenómeno que se notifica)*
 
Se podría utilizar esta estrategia para ver si la arquitectura soporta la carga esperada y puede entregar respuestas en tiempo requerido. Por ejemplo tomando la cantidad de subscriptores por la cantidad de mensajes esperados por día según la cantidad de sismos relevantes, además se puede tener en cuenta el tamaño de los mensajes para calcular el ancho de banda; y la distribución de los subscriptores para estimar si las alertas llegarán en un tiempo razonable, por ejemplo menos de 10 segundos.
