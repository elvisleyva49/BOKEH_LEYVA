from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure

import pandas as pd

# Cargar datos
try:
    data = pd.read_csv('train.csv')
    print("Archivo cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el archivo: {e}")

# Función para crear gráficos con etiquetas
def create_category_chart():
    category_data = data.groupby('Category')['Sales'].sum().reset_index()
    source = ColumnDataSource(category_data)
    
    p = figure(
        title="Ventas por Categoría",
        x_range=category_data['Category'].tolist(),
        height=450, 
        width=600,
        toolbar_location=None
    )
    
    p.vbar(x='Category', top='Sales', width=0.9, source=source, fill_color="#6baed6")
    p.xaxis.major_label_orientation = 0.7
    p.y_range.start = 0
    
    # Agregar etiquetas encima de las barras
    p.text(x='Category', y='Sales', source=source, text='Sales', 
           text_font_size="10px", text_align="center", text_baseline="bottom")
    
    return p, source

def create_region_chart():
    region_data = data.groupby('Region')['Sales'].sum().reset_index()
    source = ColumnDataSource(region_data)
    
    p = figure(
        title="Ventas por Región",
        x_range=region_data['Region'].tolist(),
        height=450, 
        width=600,
        toolbar_location=None
    )
    
    p.vbar(x='Region', top='Sales', width=0.9, source=source, fill_color="#fd8d3c")
    p.xaxis.major_label_orientation = 0.7
    p.y_range.start = 0
    
    # Agregar etiquetas encima de las barras
    p.text(x='Region', y='Sales', source=source, text='Sales', 
           text_font_size="10px", text_align="center", text_baseline="bottom")
    
    return p, source

def create_subcategory_chart():
    subcategory_data = data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
    source = ColumnDataSource(subcategory_data)
    
    p = figure(
        title="Top 5 Sub-Categorías",
        x_range=subcategory_data['Sub-Category'].tolist(),
        height=450, 
        width=600,
        toolbar_location=None
    )
    
    p.vbar(x='Sub-Category', top='Sales', width=0.9, source=source, fill_color="#74c476")
    p.xaxis.major_label_orientation = 0.7
    p.y_range.start = 0
    
    # Agregar etiquetas encima de las barras
    p.text(x='Sub-Category', y='Sales', source=source, text='Sales', 
           text_font_size="10px", text_align="center", text_baseline="bottom")
    
    return p, source

def create_shipmode_chart():
    shipmode_data = data.groupby('Ship Mode')['Sales'].sum().reset_index()
    source = ColumnDataSource(shipmode_data)
    
    p = figure(
        title="Ventas por Modo de Envío",
        x_range=shipmode_data['Ship Mode'].tolist(),
        height=450, 
        width=600,
        toolbar_location=None
    )
    
    p.vbar(x='Ship Mode', top='Sales', width=0.9, source=source, fill_color="#9e9ac8")
    p.xaxis.major_label_orientation = 0.7
    p.y_range.start = 0
    
    # Agregar etiquetas encima de las barras
    p.text(x='Ship Mode', y='Sales', source=source, text='Sales', 
           text_font_size="10px", text_align="center", text_baseline="bottom")
    
    return p, source

# Crear los gráficos y obtener sus fuentes de datos
category_plot, category_source = create_category_chart()
region_plot, region_source = create_region_chart()
subcategory_plot, subcategory_source = create_subcategory_chart()
shipmode_plot, shipmode_source = create_shipmode_chart()

# Widget para filtrar por región (simplificado)
region_options = ["Todas"] + sorted(data['Region'].unique().tolist())
region_select = Select(title="Región", value="Todas", options=region_options)

# Función para actualizar los gráficos al cambiar la región
def update(attr, old, new):
    selected_region = region_select.value
    
    if selected_region == "Todas":
        filtered_data = data
    else:
        filtered_data = data[data['Region'] == selected_region]
    
    # Actualizar cada gráfico
    # Categoría
    new_category_data = filtered_data.groupby('Category')['Sales'].sum().reset_index()
    category_source.data = {
        'Category': new_category_data['Category'].tolist(),
        'Sales': new_category_data['Sales'].tolist()
    }
    
    # Región
    new_region_data = filtered_data.groupby('Region')['Sales'].sum().reset_index()
    region_source.data = {
        'Region': new_region_data['Region'].tolist(),
        'Sales': new_region_data['Sales'].tolist()
    }
    
    # Sub-Categoría
    new_subcategory_data = filtered_data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
    subcategory_source.data = {
        'Sub-Category': new_subcategory_data['Sub-Category'].tolist(),
        'Sales': new_subcategory_data['Sales'].tolist()
    }
    
    # Ship Mode
    new_shipmode_data = filtered_data.groupby('Ship Mode')['Sales'].sum().reset_index()
    shipmode_source.data = {
        'Ship Mode': new_shipmode_data['Ship Mode'].tolist(),
        'Sales': new_shipmode_data['Sales'].tolist()
    }

# Conectar el callback
region_select.on_change('value', update)

# Organizar el layout de manera simple
layout = column(
    region_select,
    row(category_plot, region_plot),
    row(subcategory_plot, shipmode_plot)
)

# Agregar el layout al documento
curdoc().add_root(layout)
curdoc().title = "Superstore Dashboard"
