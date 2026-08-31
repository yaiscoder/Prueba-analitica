# Análisis de Ventas – Pastelería

origen: generado poruna intelegiencia artificial de acuerdo a lo requirimientos del dataset

Numero de registros: 1.565 filas.

Numero de columnas: 24 columnas.

El dataset contiene información relacionada con las ventas de una pastelería, incluyendo datos de clientes, productos, categorías, cantidades vendidas, precios, costos, descuentos, métodos de pago, canales de venta, sucursales y empleados. Se eligió este dataset porque permite analizar el comportamiento de las ventas y responder preguntas de negocio relacionadas con tendencias temporales, productos con mejor desempeño, distribución de ventas, rentabilidad y relación entre variables. Además, es un tema de interés.

##  Objetivo

Partiendo de un dataset de ventas "sucio" (`dataset_ventas_pasteleria_sucio.csv`), el proyecto realiza un proceso ETL en Python, carga los datos en un modelo relacional en PostgreSQL y construye un dashboard en Power BI para responder:

1. ¿Cuál ha sido nuestra ganancia a lo largo del año 2025?
2. ¿Qué canal de venta genera una mayor proporción de los ingresos totales?
3. ¿Cuál es el producto con mayor volumen de venta?
4. ¿Influye el precio de los productos en la cantidad vendida / en el ingreso?
5. ¿Qué categoría presenta un mayor porcentaje de descuento?


##  Estructura del proyecto

```
├── prueba.py                          # Script de limpieza (ETL) y carga a PostgreSQL
├── Dashboard.pbix                     # Dashboard de Power BI
├── csv/
│   ├── dataset_ventas_pasteleria_sucio.csv   # Dataset original (entrada)
│   └── dataset_limpio.csv                     # Dataset limpio (salida del ETL)
├── .env                                # Variables de conexión a la base de datos (no incluido)
└── README.md
```

##  Configuración

Crea un archivo `.env` en la raíz del proyecto con las credenciales de la base de datos PostgreSQL:

```env
db_user=usuario
db_password=contraseña
db_host=localhost
db_port=5432
db_name=pasteleria
```

##  Cómo ejecutar

1. Instala las dependencias:
   ```bash
   pip install pandas python-dotenv sqlalchemy psycopg2-binary
   ```
2. Ubica el dataset original en `./csv/dataset_ventas_pasteleria_sucio.csv`.
3. Ejecuta el script de limpieza y carga:
   ```bash
   python prueba.py
   ```
   Esto generará `./csv/dataset_limpio.csv` y creará/actualizará las tablas del modelo en PostgreSQL.
4. Abre `Dashboard.pbix` en Power BI Desktop y actualiza los datos (`Actualizar`) para conectarlo con la base de datos ya cargada.

## Hallazgos clave

1. Ganancia / Ingreso acumulado en 2025
El Ingreso Total del año 2025 alcanzó los $13 mil, superando holgadamente el objetivo proyectado de $5.600 en un +132,14%. El rendimiento en Utilidad Total muestra su pico más elevado en meses como Diciembre, Agosto y Julio, decreciendo progresivamente hacia el cierre de los demás periodos.

2. Canal de venta con mayor proporción de ingresos
El canal Tienda (física) lidera las ventas con un 37,37% del ingreso total. El podio lo completan WhatsApp con el 20,7% y Domicilio con el 15,94%.

3. Producto con mayor volumen de venta
El producto estrella en unidades vendidas es la Galleta Chispas, superando holgadamente las 400 unidades. Le siguen en volumen el Cupcake Chocolate y la Galleta Avena.

4. Influencia del precio en la cantidad vendida y el ingreso
Sí, existe una clara influencia. En la gráfica de dispersión (Unidades Vendidas vs. Costo Total), los productos de menor costo/precio unitario registran el mayor volumen de rotación (entre 250 y 450 unidades). Por el contrario, los artículos de mayor costo/precio (ubicados en la zona superior del eje Y) se venden en menores volúmenes (entre 80 y 200 unidades).

5. Categoría con mayor porcentaje de descuento
La categoría de Galletas registra el mayor porcentaje de descuento de todo el catálogo, seguida en menor medida por Repostería y Panadería.
