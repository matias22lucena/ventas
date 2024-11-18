import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def crear_grafico_ventas(datos_producto, producto):
    # Agrupar las ventas por año y mes, sumando las unidades vendidas de todas las sucursales
    ventas_por_producto = datos_producto.groupby(['Año', 'Mes'])['Unidades_vendidas'].sum().reset_index()
    
    # Crear el gráfico de evolución de ventas
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(len(ventas_por_producto)), ventas_por_producto['Unidades_vendidas'], label=producto)
    
    # Calcular la línea de tendencia
    x = np.arange(len(ventas_por_producto))
    y = ventas_por_producto['Unidades_vendidas']
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    # Agregar la línea de tendencia al gráfico
    ax.plot(x, p(x), linestyle='--', color='red', label='Tendencia')
    
    ax.set_title('Evolución de Ventas Mensual')
    ax.set_xlabel('Año-Mes')
    ax.set_xticks(range(len(ventas_por_producto)))
    
    etiquetas = []
    for i, row in enumerate(ventas_por_producto.itertuples()):
        if row.Mes == 1:
            etiquetas.append(f"{row.Año}")
        else:
            etiquetas.append("")
    ax.set_xticklabels(etiquetas)
    ax.set_ylabel('Unidades Vendidas')
    ax.set_ylim(0, None)  # Asegurar que el eje y comience en 0
    ax.legend(title='Producto')
    ax.grid(True)
    
    return fig

def mostrar_informacion_alumno():
    with st.container(border=True):
        st.markdown('**Legajo:** 55.555')
        st.markdown('**Nombre:** Juan Pérez')
        st.markdown('**Comisión:** C1')

# Cargar los datos desde un archivo en el sidebar
st.sidebar.header("Cargar archivo de datos")
archivo_cargado = st.sidebar.file_uploader("Subir archivo CSV", type=["csv"])

if archivo_cargado is not None:
    datos = pd.read_csv(archivo_cargado)
    
    # Obtener la lista de sucursales
    sucursales = ["Todas"] + datos['Sucursal'].unique().tolist()
    
    # Seleccionar una sucursal
    sucursal_seleccionada = st.sidebar.selectbox("Seleccionar Sucursal", sucursales)
    
    # Filtrar datos por sucursal si no se selecciona "Todas"
    if sucursal_seleccionada != "Todas":
        datos = datos[datos['Sucursal'] == sucursal_seleccionada]
        st.title(f"Datos de {sucursal_seleccionada}")
    else:
        st.title("Datos de Todas las Sucursales")
    
    # Calcular las métricas y gráficos por producto
    productos = datos['Producto'].unique()

    for producto in productos:
        with st.container(border=True):
            # Filtrar datos por producto
            st.subheader(f"{producto}")
            datos_producto = datos[datos['Producto'] == producto]
            
            # Calcular el precio promedio
            datos_producto['Precio_promedio'] = datos_producto['Ingreso_total'] / datos_producto['Unidades_vendidas']
            precio_promedio = datos_producto['Precio_promedio'].mean()
            
            # Calcular la variación anual del precio promedio
            precio_promedio_anual = datos_producto.groupby('Año')['Precio_promedio'].mean()
            variacion_precio_promedio_anual = precio_promedio_anual.pct_change().mean() * 100
            
            # Calcular las ganancias promedio y el margen
            datos_producto['Ganancia'] = datos_producto['Ingreso_total'] - datos_producto['Costo_total']
            datos_producto['Margen'] = (datos_producto['Ganancia'] / datos_producto['Ingreso_total']) * 100
            margen_promedio = datos_producto['Margen'].mean()
            
            # Calcular la variación anual del margen promedio
            margen_promedio_anual = datos_producto.groupby('Año')['Margen'].mean()
            variacion_margen_promedio_anual = margen_promedio_anual.pct_change().mean() * 100
            
            # Calcular las unidades vendidas promedio
            unidades_promedio = datos_producto['Unidades_vendidas'].mean()
            unidades_vendidas = datos_producto['Unidades_vendidas'].sum()
            
            # Calcular la variación anual de las unidades vendidas
            unidades_por_año = datos_producto.groupby('Año')['Unidades_vendidas'].sum()
            variacion_anual_unidades = unidades_por_año.pct_change().mean() * 100
            
            # Crear columnas para las métricas y el gráfico
            col1, col2 = st.columns([0.25, 0.75])
            
            # Mostrar las métricas en la primera columna
            with col1:
                st.metric(label="Precio Promedio", value=f"${precio_promedio:,.0f}".replace(",", "."), delta=f"{variacion_precio_promedio_anual:.2f}%")
                st.metric(label="Margen Promedio", value=f"{margen_promedio:.0f}%".replace(",", "."), delta=f"{variacion_margen_promedio_anual:.2f}%")
                st.metric(label="Unidades Vendidas", value=f"{unidades_vendidas:,.0f}".replace(",", "."), delta=f"{variacion_anual_unidades:.2f}%")
            
            # Mostrar el gráfico en la segunda columna ocupando todo el ancho disponible
            with col2:
                fig = crear_grafico_ventas(datos_producto, producto)
                st.pyplot(fig)
else:
    st.subheader("Por favor, sube un archivo CSV desde la barra lateral.")
    mostrar_informacion_alumno()
