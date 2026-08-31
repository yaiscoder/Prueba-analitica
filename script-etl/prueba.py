import pandas as pd
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

df_original = pd.read_csv('./csv/dataset_ventas_pasteleria_sucio.csv')

df_original.info()


# Ver duplicados
num_duplicados = df_original.duplicated().sum()
print(f'Numero de duplicados: {num_duplicados}')
df_limpio = df_original.drop_duplicates()
print(f'Numero de duplicados: {df_limpio.duplicated().sum()}')

# normalizar nombres de los datos 
df_limpio['cliente'] = df_limpio['cliente'].str.strip().str.title()
df_limpio['tipo_cliente'] = df_limpio['tipo_cliente'].str.strip().str.title()
df_limpio['producto'] = df_limpio['producto'].str.strip().str.title()
df_limpio['categoria'] = df_limpio['categoria'].str.strip().str.title()
df_limpio['canal_venta'] = df_limpio['canal_venta'].str.strip().str.title()
df_limpio['metodo_pago'] = df_limpio['metodo_pago'].str.strip().str.title()
df_limpio['estado_venta'] = df_limpio['estado_venta'].str.strip().str.title()
df_limpio['sucursal'] = df_limpio['sucursal'].str.strip().str.title()


df_limpio['producto'] = df_limpio['producto'].replace({
    'Roll De  Canela' : 'Roll De Canela',
    'Roll Canela' : 'Roll De Canela',
    'Brownie Clasico' : 'Brownie Clásico',
    'Brownie  Clásico' : 'Brownie Clásico',
    'Torta Chocolate' : 'Torta De Chocolate',
    'Tres  Leches' : 'Tres Leches',
    'Tres Leches' : 'Torta tres Leches',
    'Red Velvet' : 'Torta Red Velvet'
})

df_limpio['producto'] = df_limpio['producto'].replace('Tres Leches', 'Torta tres Leches')

df_limpio['canal_venta'] = df_limpio['canal_venta'].replace({
    'En Tienda' : 'Tienda',
    'Whats App' : 'Whatsapp',
    'Delivery' : 'Domicilio',
    'Ig' : 'Instagram',
    'Web' : 'Página Web'
})

df_limpio['categoria'] = df_limpio['categoria'].replace({
    'Cup Cake' : 'Cupcakes',
    'Galleta' : 'Galletas',
    'Torta' : 'Tortas',
    'Panaderia' : 'Panadería',
    'Reposteria' : 'Repostería'
})

df_limpio['metodo_pago'] = df_limpio['metodo_pago'].replace('Transfer','Transferencia') 

df_limpio['estado_venta'] = df_limpio['estado_venta'].replace({
    'Completado' : 'Completada',
    'Cancelado' : 'Cancelada',
    'Devolución' : 'Devuelta'
})

df_limpio['sucursal'] = df_limpio['sucursal'].replace('Rio Mar', 'Riomar')



# Manejo de nulos 
nulos_colum = df_limpio.isna().sum()
print(nulos_colum)

df_limpio = df_limpio.fillna({
    'cliente' : 'Valor no conocido',
    'tipo_cliente' : 'Valor no conocido',
    'descuento' : 0,
    'canal_venta' : 'Valor no conocido',
    'metodo_pago' : 'Valor no conocido'
})

print(df_limpio.groupby('producto')['categoria'].value_counts())

df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Brownie', case=False, na=False),'categoria'] = 'Repostería'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Caja', case=False, na=False),'categoria'] = 'Combos'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Cheesecake', case=False, na=False),'categoria'] = 'Tortas'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Croissant', case=False, na=False),'categoria'] = 'Panadería'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Cupcake', case=False, na=False),'categoria'] = 'Cupcakes'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Galleta', case=False, na=False),'categoria'] = 'Galletas'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Macaron', case=False, na=False),'categoria'] = 'Macarons'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Roll', case=False, na=False),'categoria'] = 'Panadería'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Tarta', case=False, na=False),'categoria'] = 'Tartas'
df_limpio.loc[df_limpio['categoria'].isna() & df_limpio['producto'].str.contains('Torta', case=False, na=False),'categoria'] = 'Tortas'

# rellenar nulos con sus id correspondiente 
mapa_empleados = df_limpio.dropna(subset=['empleado']).drop_duplicates('id_empleado').set_index('id_empleado')['empleado']
df_limpio['empleado'] = df_limpio['empleado'].fillna(df_limpio['id_empleado'].map(mapa_empleados))

mapa_sucursales = df_limpio.dropna(subset=['sucursal']).drop_duplicates('id_sucursal').set_index('id_sucursal')['sucursal']
df_limpio['sucursal'] = df_limpio['sucursal'].fillna(df_limpio['id_sucursal'].map(mapa_sucursales))

df_limpio.loc[df_limpio['ciudad'].isna() & df_limpio['sucursal'].str.contains('Centro', case=False, na=False),'ciudad'] = 'Barranquilla'
df_limpio.loc[df_limpio['ciudad'].isna() & df_limpio['sucursal'].str.contains('Norte', case=False, na=False),'ciudad'] = 'Barranquilla'
df_limpio.loc[df_limpio['ciudad'].isna() & df_limpio['sucursal'].str.contains('Riomar', case=False, na=False),'ciudad'] = 'Barranquilla'
df_limpio.loc[df_limpio['ciudad'].isna() & df_limpio['sucursal'].str.contains('Soledad', case=False, na=False),'ciudad'] = 'Soledad'


print('-'*90)
print(df_limpio.isna().sum())


# valores atipicos
print(df_limpio['precio_unitario'].unique())
df_limpio['precio_unitario'] = df_limpio['precio_unitario'].str.replace('$','', regex=False).str.replace('.', '', regex=False)
df_limpio['costo_unitario'] = df_limpio['costo_unitario'].str.replace('$','', regex=False).str.replace('.', '', regex=False)
df_limpio['total_venta'] = df_limpio['total_venta'].str.replace('$','', regex=False).str.replace(',', '.', regex=False)

print(df_limpio['precio_unitario'].unique())


# corregir tipos de datos 

df_limpio.info()

df_limpio['precio_unitario'] = pd.to_numeric(df_limpio['precio_unitario'], errors='coerce')
df_limpio['costo_unitario'] = pd.to_numeric(df_limpio['costo_unitario'], errors='coerce')
df_limpio['total_venta'] = pd.to_numeric(df_limpio['total_venta'], errors='coerce')
df_limpio['fecha_venta'] = df_limpio['fecha_venta'].str.replace('/', '-', regex=False)
df_limpio['fecha_venta'] = pd.to_datetime(df_limpio['fecha_venta'], format='mixed', dayfirst=False, errors='coerce')

df_limpio.info()

# columnas derivadas

df_limpio['nombre_mes'] = df_limpio['fecha_venta'].dt.month_name(locale='es_CO')
df_limpio['costo_total'] = df_limpio['cantidad'] * df_limpio['costo_unitario']

print('-'*90)
# verificar las informacion
print(f'Numero de duplicados: {df_limpio.duplicated().sum()}')
df_final = df_limpio.drop_duplicates()
print(f'Numero de duplicados: {df_final.duplicated().sum()}')
print(f'Numero de nulos en cada columna: {df_final.isna().sum()}')
print(df_final['fecha_venta'].min())
print(df_final['fecha_venta'].max())
df_final.info()

# guardar csv
df_limpio.to_csv('./csv/dataset_limpio.csv', index=False, encoding='utf-8-sig')






# Creación de tablas para postgres

# Lectura de las variables de entorno
user = os.getenv("db_user")
password = os.getenv("db_password")
host = os.getenv("db_host")
port = os.getenv("db_port")
db_name = os.getenv("db_name")

DATABASE_URL = (f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}")

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    connection.execute(text("SELECT 1"))

print("Conexión exitosa")

dim_clientes = df_final[['id_cliente', 'cliente', 'tipo_cliente']].drop_duplicates(subset=['id_cliente'])
dim_productos = df_final[['id_producto', 'producto', 'categoria', 'sabor_tipo']].drop_duplicates(subset=['id_producto'])
dim_sucursales = df_final[['id_sucursal', 'sucursal', 'ciudad', 'departamento']].drop_duplicates(subset=['id_sucursal'])
dim_empleados = df_final[['id_empleado', 'empleado', 'cargo']].drop_duplicates(subset=['id_empleado'])
dim_ventas = df_final[['id_venta', 'fecha_venta', 'nombre_mes', 'id_cliente', 'canal_venta', 'metodo_pago','estado_venta', 'id_sucursal', 'id_empleado']].drop_duplicates(subset=['id_venta'])
fact_venta_detalle = df_final[['id_venta', 'id_producto', 'cantidad', 'precio_unitario', 'costo_unitario', 'descuento', 'total_venta', 'costo_total']]
fact_venta_detalle.insert(0, 'id_detalle', range(1, 1 + len(fact_venta_detalle)))


dim_clientes.to_sql('dim_clientes', engine, if_exists='replace', index=False)
dim_productos.to_sql('dim_productos', engine, if_exists='replace', index=False)
dim_sucursales.to_sql('dim_sucursales', engine, if_exists='replace', index=False)
dim_empleados.to_sql('dim_empleados', engine, if_exists='replace', index=False)
dim_ventas.to_sql('dim_ventas', engine, if_exists='replace', index=False)
fact_venta_detalle.to_sql('fact_venta_detalle', engine, if_exists='replace', index=False)


with engine.connect() as conn:
    conn.execute(text("ALTER TABLE dim_clientes ADD PRIMARY KEY (id_cliente);"))
    conn.execute(text("ALTER TABLE dim_productos ADD PRIMARY KEY (id_producto);"))
    conn.execute(text("ALTER TABLE dim_sucursales ADD PRIMARY KEY (id_sucursal);"))
    conn.execute(text("ALTER TABLE dim_empleados ADD PRIMARY KEY (id_empleado);"))
    conn.execute(text("ALTER TABLE dim_ventas ADD PRIMARY KEY (id_venta);"))
    conn.execute(text("ALTER TABLE fact_venta_detalle ADD PRIMARY KEY (id_detalle);"))
        
       
    conn.execute(text("ALTER TABLE dim_ventas ADD CONSTRAINT fk_ventas_clientes FOREIGN KEY (id_cliente) REFERENCES dim_clientes(id_cliente);"))
    conn.execute(text("ALTER TABLE dim_ventas ADD CONSTRAINT fk_ventas_sucursales FOREIGN KEY (id_sucursal) REFERENCES dim_sucursales(id_sucursal);"))
    conn.execute(text("ALTER TABLE dim_ventas ADD CONSTRAINT fk_ventas_empleados FOREIGN KEY (id_empleado) REFERENCES dim_empleados(id_empleado);"))
        
       
    conn.execute(text("ALTER TABLE fact_venta_detalle ADD CONSTRAINT fk_detalle_ventas FOREIGN KEY (id_venta) REFERENCES dim_ventas(id_venta);"))
    conn.execute(text("ALTER TABLE fact_venta_detalle ADD CONSTRAINT fk_detalle_productos FOREIGN KEY (id_producto) REFERENCES dim_productos(id_producto);"))


conn.commit()

engine.dispose()
print('proceso terminado')






