


## 🔗[DIAPOSITIVAS](https://www.canva.com/design/DAGgybOW2BA/73P5ctFVXqsGbul6IKVVkg/edit?utm_content=DAGgybOW2BA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)



#  Implementación del Patrón Cache-Aside en Azure con Redis y SQLite

##  Introducción

En aplicaciones distribuidas, es crucial optimizar el acceso a los datos y reducir la carga sobre la base de datos principal. Para ello, implementamos el patrón **Cache-Aside** utilizando **Redis** y **SQLite**, desplegado en **Microsoft Azure**.

Este patrón permite almacenar temporalmente los datos más consultados en caché, mejorando el rendimiento y reduciendo la latencia en las consultas. Si un dato no se encuentra en caché, se obtiene de la base de datos y se almacena en Redis para futuras consultas.

##  Objetivos

- Implementar el patrón **Cache-Aside** utilizando Redis y SQLite.
- Desplegar la solución en **Azure** y analizar las métricas de rendimiento.
- Reducir la carga sobre la base de datos mediante el uso eficiente de la caché.
- Evaluar el impacto del uso de Redis en la optimización de consultas frecuentes.

##  Cómo Ejecutar el Proyecto

###  Prerrequisitos

1. Tener instalado **Python 3.8+**.
2. Instalar las dependencias necesarias ejecutando:

   ```sh
   pip install redis sqlite3 logging
   ```

3. Contar con una instancia de **Azure Cache for Redis** y configurar correctamente la conexión.
4. Configurar la conexión a Redis en Azure:
   - En el archivo `cacheaside.py`, ubica la variable `host` y `port`.
   - Reemplázalas con los valores de tu instancia de Redis en Azure.

   ```python
   self.cache = redis.StrictRedis(host="<TU_HOST_AZURE>", port=6380, db=0, decode_responses=True, ssl=True)
   ```

###  Paso 1: Inicializar la Base de Datos
Ejecuta el script para crear la base de datos SQLite y poblarla con datos de prueba:

```sh
python cacheaside.py
```

###  Paso 2: Consultar Productos Usando Caché

El sistema permite consultar productos de la siguiente forma:

1. **Consulta en Caché (Redis)**: Si el dato está en caché, se obtiene rápidamente.
2. **Cache MISS**: Si el dato no está en caché, se consulta en SQLite y se almacena en Redis.
3. **Consulta Manual en BD**: Se obtiene el dato directamente de SQLite sin pasar por la caché.

Para consultar un producto:

```sh
python cacheaside.py
```

Selecciona la opción deseada en el menú interactivo.

##  Funcionalidades del Sistema

###  Base de Datos (SQLite)
- Almacena productos con ID y nombre.
- Registra logs de consultas manuales.

###  Caché (Redis en Azure)
- Guarda datos temporalmente para reducir consultas a la base de datos.
- Expira los datos tras un TTL configurable (ejemplo: 30 segundos).
- Optimiza la velocidad de acceso a los datos frecuentes.

###  Sistema de Registro (Logging)
- Muestra logs de consultas manuales.
- Indica si la consulta fue un **Cache HIT** o **Cache MISS**.

##  Beneficios del Patrón Cache-Aside

- **Reducción de carga** sobre la base de datos.
- **Menor latencia** en consultas repetitivas.
- **Optimización del rendimiento** gracias a Redis.
- **Alta disponibilidad** mediante Azure Cache for Redis.

##  Métricas en Azure

El sistema está desplegado en **Microsoft Azure**, lo que permite monitorear el rendimiento en **Azure Monitor**:

- **Métricas de Redis**: Uso de memoria, cantidad de aciertos en caché (Cache HITs) y fallos (Cache MISSes).
- **Rendimiento de la BD**: Cantidad de consultas directas a SQLite.
- **Latencia de respuesta**: Tiempo medio de respuesta en caché vs. base de datos.


## Conclusión

Esta implementación del patrón **Cache-Aside** demuestra cómo mejorar la eficiencia en el acceso a los datos utilizando **Redis en Azure**. Al almacenar en caché los datos más consultados, logramos reducir la carga en la base de datos y mejorar el rendimiento general del sistema.







