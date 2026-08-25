import streamlit as st
import pandas as pd

st.title("Manejo de DataFrames")
st.sidebar.title("Herramientas")

archivo = st.sidebar.file_uploader(
    "Seleccione su archivo",
    type=["csv", "xlsx"]
)

if archivo is not None:

    try:
        if archivo.name.lower().endswith(".csv"):
            datos = pd.read_csv(archivo)

        elif archivo.name.lower().endswith(".xlsx"):
            datos = pd.read_excel(archivo)

        st.success("Su archivo ha sido cargado correctamente")

        st.subheader("Vista previa de los datos")
        st.dataframe(datos, use_container_width=True)

        st.write(f"**Filas:** {datos.shape[0]}")
        st.write(f"**Columnas:** {datos.shape[1]}")

    except Exception as error:
        st.error(f"No fue posible leer el archivo: {error}")

else:
    st.info("Cargue un archivo CSV o Excel para visualizar los datos.")

import pandas as pd

df = pd.read_csv("/content/BankMarketing.csv")

df

print("Conteo de valores nulos por columna:")
display(df.isnull().sum())

"""2. Clasificación de variables"""

def classify_variables(df):
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    return numerical_cols, categorical_cols

numerical_cols, categorical_cols = classify_variables(df)

print(f"Variables Numéricas ({len(numerical_cols)}): {numerical_cols}")
print(f"Variables Categóricas ({len(categorical_cols)}): {categorical_cols}")

"""3: Estadísticas descriptivas"""

df.describe()

df.info()

"""5. Distribución de variables numéricas"""

import matplotlib.pyplot as plt
import seaborn as sns

# Obtener las columnas numéricas (excluyendo 'pdays' por su particularidad)
numerical_cols_for_hist = [col for col in numerical_cols if col != 'pdays']

plt.figure(figsize=(15, 12))
for i, col in enumerate(numerical_cols_for_hist):
    plt.subplot(4, 3, i + 1) # Ajusta la cuadrícula de subplots según sea necesario
    sns.histplot(df[col], kde=True, bins=30)
    plt.title(f'Distribución de {col}')
    plt.xlabel(col)
    plt.ylabel('Frecuencia')
plt.tight_layout()
plt.show()

"""6. Análisis de variables categóricas"""

import matplotlib.pyplot as plt
import seaborn as sns

# Establecer el estilo de los gráficos
sns.set_style("whitegrid")

# Iterar sobre las columnas categóricas
for col in categorical_cols:
    print(f"\n--- Análisis de la variable categórica: {col} ---")

    # Conteo de valores
    value_counts = df[col].value_counts()
    print("Conteo de valores:\n")
    display(value_counts)

    # Proporciones
    proportions = df[col].value_counts(normalize=True) * 100
    print("\nProporciones (%):\n")
    display(proportions)

    # Gráfico de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(x=value_counts.index, y=value_counts.values, palette='viridis')
    plt.title(f'Distribución de {col}')
    plt.xlabel(col)
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=45, ha='right') # Rotar etiquetas para mejor lectura
    plt.tight_layout()
    plt.show()

"""7. Análisis bivariado (numérico vs categórico)"""

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

plt.figure(figsize=(8, 6))
sns.boxplot(x='y', y='age', data=df, palette='viridis')
plt.title('Distribución de Edad por Suscripción (y)')
plt.xlabel('Suscripción (y)')
plt.ylabel('Edad')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(x='y', y='duration', data=df, palette='magma')
plt.title('Distribución de Duración de Contacto por Suscripción (y)')
plt.xlabel('Suscripción (y)')
plt.ylabel('Duración de Contacto')
plt.tight_layout()
plt.show()

"""8. Análisis bivariado (categórico vs categórico)"""

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# --- Análisis de 'education' vs 'y' ---
print("\n--- Análisis de 'education' vs 'y' ---")

crosstab_education_y = pd.crosstab(df['education'], df['y'])
display(crosstab_education_y)

# Proporciones normalizadas para 'education' vs 'y'
crosstab_education_y_prop = pd.crosstab(df['education'], df['y'], normalize='index') * 100
display(crosstab_education_y_prop)

crosstab_education_y_prop.plot(kind='bar', stacked=True, figsize=(12, 7), cmap='viridis')
plt.title('Proporción de Suscripción (y) por Nivel Educativo')
plt.xlabel('Nivel Educativo')
plt.ylabel('Proporción (%)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Suscripción (y)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# --- Análisis de 'contact' vs 'y' ---
print("\n--- Análisis de 'contact' vs 'y' ---")

crosstab_contact_y = pd.crosstab(df['contact'], df['y'])
display(crosstab_contact_y)

# Proporciones normalizadas para 'contact' vs 'y'
crosstab_contact_y_prop = pd.crosstab(df['contact'], df['y'], normalize='index') * 100
display(crosstab_contact_y_prop)

crosstab_contact_y_prop.plot(kind='bar', stacked=True, figsize=(8, 6), cmap='magma')
plt.title('Proporción de Suscripción (y) por Tipo de Contacto')
plt.xlabel('Tipo de Contacto')
plt.ylabel('Proporción (%)')
plt.xticks(rotation=0)
plt.legend(title='Suscripción (y)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

"""9. Análisis basado en parámetros seleccionados"""

import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style("whitegrid")

# Excluir 'y' de las variables categóricas seleccionables para el análisis independiente
selectable_categorical_cols = [col for col in categorical_cols if col != 'y']

# Crear un Dropdown para seleccionar la variable categórica
category_dropdown = widgets.Dropdown(
    options=selectable_categorical_cols,
    description='Selecciona Categoría:',
    disabled=False,
)

def plot_category_vs_y(category_col):
    if category_col and category_col in df.columns:
        clear_output(wait=True)
        print(f"--- Análisis de '{category_col}' vs 'y' ---")

        crosstab_cat_y = pd.crosstab(df[category_col], df['y'])
        print("Tabla de contingencia:")
        display(crosstab_cat_y)

        crosstab_cat_y_prop = pd.crosstab(df[category_col], df['y'], normalize='index') * 100
        print("Proporciones normalizadas (%):")
        display(crosstab_cat_y_prop)

        plt.figure(figsize=(10, 6))
        crosstab_cat_y_prop.plot(kind='bar', stacked=True, figsize=(12, 7), cmap='viridis', ax=plt.gca())
        plt.title(f'Proporción de Suscripción (y) por {category_col}')
        plt.xlabel(category_col)
        plt.ylabel('Proporción (%)')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Suscripción (y)', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    else:
        clear_output(wait=True)
        print("Por favor, selecciona una columna categórica.")

# Enlazar el dropdown con la función de ploteo
output = widgets.interactive_output(plot_category_vs_y, {'category_col': category_dropdown})

# Mostrar el widget y el output
display(category_dropdown, output)

"""10. Hallazgos clave"""

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

plt.figure(figsize=(7, 5))
sns.countplot(x='y', data=df, palette='viridis')
plt.title('Distribución de la Variable Objetivo (y)')
plt.xlabel('Suscripción a Depósito a Plazo')
plt.ylabel('Frecuencia')

# Añadir porcentajes al gráfico
total = float(len(df))
for p in plt.gca().patches:
    height = p.get_height()
    plt.gca().text(p.get_x() + p.get_width()/2.,
            height + 3,
            '{:1.1f}%'.format(100*height/total),
            ha='center', va='bottom')

plt.tight_layout()
plt.show()
