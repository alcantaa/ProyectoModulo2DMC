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
