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


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
 
# =============================================================================
# CONFIGURACIÓN GENERAL
# =============================================================================
st.set_page_config(page_title="EDA - Bank Marketing", page_icon="📊", layout="wide")
sns.set_style("whitegrid")
 
AUTOR = "Alexander [Completa tu apellido aquí]"
CURSO = "Especialización en Python for Analytics — DMC Institute"
ANIO = 2026
 
 
# =============================================================================
# CLASE (POO) — DataAnalyzer
# Encapsula estadísticas descriptivas, clasificación de variables y
# funciones de visualización reutilizables en toda la app.
# =============================================================================
class DataAnalyzer:
    """Encapsula la lógica de análisis exploratorio sobre un DataFrame."""
 
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.numericas, self.categoricas = self._clasificar_variables()
 
    def _clasificar_variables(self):
        """Función personalizada que separa columnas numéricas de categóricas."""
        numericas = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categoricas = self.df.select_dtypes(include=["object", "category"]).columns.tolist()
        return numericas, categoricas
 
    def resumen_info(self) -> pd.DataFrame:
        """Equivalente tabular a .info(): tipos de dato y conteo de nulos."""
        return pd.DataFrame({
            "Columna": self.df.columns,
            "Tipo de dato": self.df.dtypes.astype(str).values,
            "No nulos": self.df.notnull().sum().values,
            "Nulos": self.df.isnull().sum().values,
        })
 
    def estadisticas_descriptivas(self, columnas):
        """Devuelve .describe() transpuesto para un subconjunto de columnas."""
        return self.df[columnas].describe().T
 
    def medidas_tendencia(self, columna: str) -> dict:
        """Media, mediana, moda y desviación estándar de una columna numérica."""
        serie = self.df[columna]
        return {
            "media": serie.mean(),
            "mediana": serie.median(),
            "moda": serie.mode().iloc[0] if not serie.mode().empty else np.nan,
            "std": serie.std(),
        }
 
    def conteo_nulos(self) -> pd.DataFrame:
        nulos = self.df.isnull().sum()
        porcentaje = (nulos / len(self.df) * 100).round(2)
        return pd.DataFrame({"Nulos": nulos, "% Nulos": porcentaje}).sort_values(
            "Nulos", ascending=False
        )
 
    def conteo_unknown(self) -> pd.DataFrame:
        """Cuenta la categoría 'unknown', frecuente en este dataset como faltante disfrazado."""
        unknown = (self.df[self.categoricas] == "unknown").sum()
        unknown = unknown[unknown > 0].sort_values(ascending=False)
        return unknown.rename("Conteo 'unknown'").to_frame()
 
    # --------------------------- Visualizaciones ---------------------------
    def plot_histograma(self, columna: str, kde: bool = True):
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.histplot(self.df[columna], kde=kde, ax=ax, color="teal")
        ax.set_title(f"Distribución de '{columna}'")
        return fig
 
    def plot_barras_categorica(self, columna: str):
        conteo = self.df[columna].value_counts()
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(x=conteo.index, y=conteo.values, ax=ax, color="coral")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_ylabel("Conteo")
        ax.set_title(f"Frecuencia de '{columna}'")
        return fig
 
    def plot_boxplot_num_cat(self, num_col: str, cat_col: str):
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.boxplot(x=cat_col, y=num_col, data=self.df, ax=ax, palette="Set2")
        ax.set_title(f"'{num_col}' según '{cat_col}'")
        return fig
 
    def plot_barras_apiladas_cat_cat(self, cat1: str, cat2: str):
        tabla = pd.crosstab(self.df[cat1], self.df[cat2], normalize="index") * 100
        fig, ax = plt.subplots(figsize=(8, 4.5))
        tabla.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
        ax.set_ylabel("Proporción (%)")
        ax.set_title(f"'{cat1}' vs '{cat2}' (proporciones)")
        ax.legend(title=cat2, bbox_to_anchor=(1.02, 1), loc="upper left")
        return fig, tabla
 
 
# =============================================================================
# ESTADO DE SESIÓN
# =============================================================================
if "df" not in st.session_state:
    st.session_state.df = None
 
 
@st.cache_data
def cargar_csv(archivo) -> pd.DataFrame:
    return pd.read_csv(archivo, sep=";")
 
 
# =============================================================================
# SIDEBAR — NAVEGACIÓN PRINCIPAL
# =============================================================================
st.sidebar.title("📊 Bank Marketing EDA")
modulo = st.sidebar.radio(
    "Navegación",
    ["🏠 Home", "📂 Carga del dataset", "🔍 Análisis Exploratorio (EDA)", "✅ Conclusiones"],
)
 
st.sidebar.markdown("---")
st.sidebar.caption(f"👤 {AUTOR}")
st.sidebar.caption(f"🎓 {CURSO}")
st.sidebar.caption(f"📅 {ANIO}")
 
df_cargado = st.session_state.df is not None
 
# =============================================================================
# MÓDULO 1: HOME
# =============================================================================
if modulo == "🏠 Home":
    st.title("📊 EDA — Bank Marketing Campaign")
    st.subheader("Caso de Estudio N°1 — Especialización en Python for Analytics")
 
    st.markdown(
        f"""
    ### Objetivo del análisis
    Esta aplicación realiza un **Análisis Exploratorio de Datos (EDA)** sobre la
    última campaña de marketing telefónico de una institución financiera, cuya
    efectividad (ventas/base) cayó de **12% a 8%** en los últimos 6 meses. El
    objetivo **no es construir un modelo predictivo**, sino identificar
    relaciones y patrones entre variables que sirvan de base para la toma de
    decisiones comerciales.
 
    ### Datos del autor
    - **Nombre completo:** {AUTOR}
    - **Curso / Especialización:** {CURSO}
    - **Año:** {ANIO}
 
    ### Sobre el dataset
    `BankMarketing.csv` contiene **41,188 registros** y **21 variables** sobre
    clientes contactados telefónicamente (datos demográficos, canal y
    resultado del contacto, indicadores socioeconómicos, y la variable
    objetivo `y`: si el cliente aceptó o no la oferta).
 
    ### Tecnologías utilizadas
    - **Python** — lenguaje base
    - **Pandas / NumPy** — manipulación y análisis de datos
    - **Matplotlib / Seaborn** — visualización
    - **Streamlit** — interfaz interactiva
    - **Programación Orientada a Objetos** — clase `DataAnalyzer` que
      encapsula la lógica de análisis
    """
    )
 
    st.info("👉 Ve al módulo **'📂 Carga del dataset'** en la barra lateral para comenzar.")
 
# =============================================================================
# MÓDULO 2: CARGA DEL DATASET
# =============================================================================
elif modulo == "📂 Carga del dataset":
    st.title("📂 Carga del dataset")
 
    archivo = st.file_uploader("Sube el archivo BankMarketing.csv", type=["csv"])
 
    if archivo is not None:
        try:
            df = cargar_csv(archivo)
            st.session_state.df = df
            st.success(f"✅ Archivo cargado correctamente: **{archivo.name}**")
 
            col1, col2 = st.columns(2)
            col1.metric("Filas", df.shape[0])
            col2.metric("Columnas", df.shape[1])
 
            st.subheader("Vista previa (head)")
            st.dataframe(df.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"❌ No se pudo leer el archivo: {e}")
            st.session_state.df = None
    else:
        st.warning("⚠️ Ningún análisis se ejecutará hasta que cargues el archivo CSV.")
 
# =============================================================================
# MÓDULO 3: ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# =============================================================================
elif modulo == "🔍 Análisis Exploratorio (EDA)":
    st.title("🔍 Análisis Exploratorio de Datos (EDA)")
 
    if not df_cargado:
        st.warning(
            "⚠️ Debes cargar el archivo en el módulo **'📂 Carga del dataset'** "
            "antes de ejecutar cualquier análisis."
        )
    else:
        df = st.session_state.df
        analyzer = DataAnalyzer(df)
 
        tabs = st.tabs([
            "1️⃣ Info general", "2️⃣ Variables", "3️⃣ Descriptivas", "4️⃣ Faltantes",
            "5️⃣ Distribución", "6️⃣ Categóricas", "7️⃣ Bivariado num-cat",
            "8️⃣ Bivariado cat-cat", "9️⃣ Dinámico", "🔟 Hallazgos",
        ])
 
        # ---------------- Ítem 1: Información general ----------------
        with tabs[0]:
            st.header("Información general del dataset")
            c1, c2, c3 = st.columns(3)
            c1.metric("Filas", df.shape[0])
            c2.metric("Columnas", df.shape[1])
            c3.metric("Duplicados", int(df.duplicated().sum()))
            st.dataframe(analyzer.resumen_info(), use_container_width=True)
 
        # ---------------- Ítem 2: Clasificación de variables ----------------
        with tabs[1]:
            st.header("Clasificación de variables")
            c1, c2 = st.columns(2)
            with c1:
                st.subheader(f"Numéricas ({len(analyzer.numericas)})")
                st.write(analyzer.numericas)
            with c2:
                st.subheader(f"Categóricas ({len(analyzer.categoricas)})")
                st.write(analyzer.categoricas)
            st.dataframe(pd.DataFrame({
                "Tipo": ["Numéricas", "Categóricas"],
                "Cantidad": [len(analyzer.numericas), len(analyzer.categoricas)],
            }), use_container_width=True)
 
        # ---------------- Ítem 3: Estadísticas descriptivas ----------------
        with tabs[2]:
            st.header("Estadísticas descriptivas")
            st.subheader(".describe() — Variables numéricas")
            st.dataframe(analyzer.estadisticas_descriptivas(analyzer.numericas), use_container_width=True)
            st.subheader(".describe() — Variables categóricas")
            st.dataframe(df[analyzer.categoricas].describe().T, use_container_width=True)
 
            col_sel = st.selectbox("Explorar medidas de tendencia central de:", analyzer.numericas)
            m = analyzer.medidas_tendencia(col_sel)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Media", f"{m['media']:.2f}")
            c2.metric("Mediana", f"{m['mediana']:.2f}")
            c3.metric("Moda", f"{m['moda']:.2f}")
            c4.metric("Desv. estándar", f"{m['std']:.2f}")
            st.markdown(
                f"**Interpretación:** en `{col_sel}`, si la media y la mediana difieren "
                f"notablemente, la distribución está sesgada. Una desviación estándar alta "
                f"respecto a la media indica mayor dispersión de los datos."
            )
 
        # ---------------- Ítem 4: Valores faltantes ----------------
        with tabs[3]:
            st.header("Análisis de valores faltantes")
            nulos_df = analyzer.conteo_nulos()
            st.dataframe(nulos_df, use_container_width=True)
 
            if nulos_df["Nulos"].sum() > 0:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.barplot(x=nulos_df.index, y=nulos_df["Nulos"], ax=ax, color="steelblue")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                st.pyplot(fig)
            else:
                st.info(
                    "No hay valores nulos explícitos (NaN). Sin embargo, el dataset codifica "
                    "los desconocidos como la categoría **'unknown'** en varias columnas "
                    "categóricas, lo que funciona como un valor faltante disfrazado."
                )
                st.dataframe(analyzer.conteo_unknown(), use_container_width=True)
 
            st.markdown(
                "**Discusión:** conviene decidir si estas categorías 'unknown' se imputan, "
                "se agrupan como 'otros' o se mantienen como una categoría informativa "
                "propia, antes de cualquier análisis posterior o modelado."
            )
 
        # ---------------- Ítem 5: Distribución numéricas ----------------
        with tabs[4]:
            st.header("Distribución de variables numéricas")
            var_hist = st.selectbox("Variable numérica", analyzer.numericas, key="hist_var")
            mostrar_kde = st.checkbox("Mostrar curva de densidad (KDE)", value=True)
 
            st.pyplot(analyzer.plot_histograma(var_hist, kde=mostrar_kde))
 
            st.markdown(
                f"**Interpretación visual:** observa la forma de `{var_hist}` (simétrica, "
                f"sesgada, con colas largas o posibles outliers) y compárala con la media "
                f"({df[var_hist].mean():.2f}) y mediana ({df[var_hist].median():.2f}) vistas "
                f"en el ítem anterior."
            )
 
        # ---------------- Ítem 6: Variables categóricas ----------------
        with tabs[5]:
            st.header("Análisis de variables categóricas")
            var_cat = st.selectbox("Variable categórica", analyzer.categoricas, key="cat_var")
 
            conteo = df[var_cat].value_counts()
            proporcion = (df[var_cat].value_counts(normalize=True) * 100).round(2)
            st.dataframe(pd.DataFrame({"Conteo": conteo, "Proporción (%)": proporcion}),
                         use_container_width=True)
            st.pyplot(analyzer.plot_barras_categorica(var_cat))
 
        # ---------------- Ítem 7: Bivariado num vs cat ----------------
        with tabs[6]:
            st.header("Análisis bivariado: numérico vs categórico")
            c1, c2 = st.columns(2)
            with c1:
                num_biv = st.selectbox(
                    "Variable numérica", analyzer.numericas,
                    index=analyzer.numericas.index("age") if "age" in analyzer.numericas else 0,
                    key="biv_num",
                )
            with c2:
                cat_biv = st.selectbox(
                    "Variable categórica", analyzer.categoricas,
                    index=analyzer.categoricas.index("y") if "y" in analyzer.categoricas else 0,
                    key="biv_cat",
                )
            st.pyplot(analyzer.plot_boxplot_num_cat(num_biv, cat_biv))
            st.dataframe(
                df.groupby(cat_biv)[num_biv].agg(["mean", "median", "std"]).round(2),
                use_container_width=True,
            )
            st.caption("Ejemplos sugeridos: `age` vs `y`, `duration` vs `y`.")
 
        # ---------------- Ítem 8: Bivariado cat vs cat ----------------
        with tabs[7]:
            st.header("Análisis bivariado: categórico vs categórico")
            c1, c2 = st.columns(2)
            with c1:
                cat1 = st.selectbox(
                    "Variable categórica 1", analyzer.categoricas,
                    index=analyzer.categoricas.index("education") if "education" in analyzer.categoricas else 0,
                    key="cat1",
                )
            with c2:
                cat2 = st.selectbox(
                    "Variable categórica 2", analyzer.categoricas,
                    index=analyzer.categoricas.index("y") if "y" in analyzer.categoricas else 1,
                    key="cat2",
                )
            fig, tabla = analyzer.plot_barras_apiladas_cat_cat(cat1, cat2)
            st.dataframe(tabla.round(2), use_container_width=True)
            st.pyplot(fig)
            st.caption("Ejemplos sugeridos: `education` vs `y`, `contact` vs `y`.")
 
        # ---------------- Ítem 9: Análisis dinámico ----------------
        with tabs[8]:
            st.header("Análisis dinámico según parámetros seleccionados")
 
            cols_sel = st.multiselect(
                "Columnas numéricas a analizar",
                analyzer.numericas,
                default=analyzer.numericas[:2] if len(analyzer.numericas) >= 2 else analyzer.numericas,
            )
            filtro_cat = st.selectbox(
                "Filtrar por variable categórica (opcional)",
                ["(ninguna)"] + analyzer.categoricas, key="filtro_cat",
            )
 
            df_din = df.copy()
            if filtro_cat != "(ninguna)":
                valores_disp = df[filtro_cat].unique().tolist()
                valores = st.multiselect(f"Valores de '{filtro_cat}'", valores_disp, default=valores_disp)
                df_din = df_din[df_din[filtro_cat].isin(valores)]
 
            if "age" in df.columns:
                rango_edad = st.slider(
                    "Filtrar rango de edad (age)",
                    int(df["age"].min()), int(df["age"].max()),
                    (int(df["age"].min()), int(df["age"].max())),
                )
                df_din = df_din[(df_din["age"] >= rango_edad[0]) & (df_din["age"] <= rango_edad[1])]
 
            st.caption(f"Filas resultantes tras filtros: **{len(df_din)}**")
 
            if cols_sel:
                st.dataframe(df_din[cols_sel].describe().T, use_container_width=True)
                fig, ax = plt.subplots(figsize=(9, 4))
                df_din[cols_sel].boxplot(ax=ax)
                plt.xticks(rotation=30)
                st.pyplot(fig)
            else:
                st.info("Selecciona al menos una columna numérica para ver el análisis.")
 
        # ---------------- Ítem 10: Hallazgos clave ----------------
        with tabs[9]:
            st.header("Hallazgos clave")
 
            if "y" in df.columns:
                tasa = (df["y"].value_counts(normalize=True) * 100).round(2)
                c1, c2 = st.columns([1, 1])
                with c1:
                    fig, ax = plt.subplots(figsize=(5, 5))
                    ax.pie(tasa, labels=tasa.index, autopct="%1.1f%%",
                           colors=sns.color_palette("pastel"))
                    ax.set_title("Distribución de la variable objetivo 'y'")
                    st.pyplot(fig)
                with c2:
                    st.metric("Tasa de aceptación ('yes')", f"{tasa.get('yes', 0)}%")
                    st.metric("Tasa de no aceptación ('no')", f"{tasa.get('no', 0)}%")
 
            st.markdown(
                """
            **Insights principales del EDA:**
            1. La variable objetivo `y` está **fuertemente desbalanceada** — la gran mayoría
               de los clientes contactados no acepta la oferta.
            2. `duration` (duración de la llamada) muestra la **relación más marcada** con
               la aceptación, aunque no debe usarse como predictor real ya que se conoce
               solo después de realizar la llamada.
            3. Variables como `education`, `job` y `contact` presentan **diferencias
               visibles** en las proporciones de aceptación entre categorías.
            4. No hay `NaN` explícitos, pero sí un volumen relevante de categorías
               `'unknown'` que deben tratarse como faltantes antes de un análisis más
               profundo.
            5. Variables como `campaign`, `previous` y `pdays` muestran **distribuciones
               sesgadas**, con posibles valores atípicos que conviene revisar.
            """
            )
 
# =============================================================================
# MÓDULO 4: CONCLUSIONES
# =============================================================================
elif modulo == "✅ Conclusiones":
    st.title("✅ Conclusiones finales")
 
    if not df_cargado:
        st.warning("⚠️ Carga el dataset primero para generar conclusiones basadas en datos reales.")
    else:
        st.markdown(
            """
        A partir del Análisis Exploratorio de Datos realizado sobre `BankMarketing.csv`,
        se plantean las siguientes conclusiones orientadas a la **toma de decisiones**
        (no a la predicción):
 
        1. **Bajo desempeño estructural de la campaña.** La proporción de clientes que
           acepta la oferta es baja respecto al total contactado, lo que es consistente
           con la caída de efectividad reportada (de 12% a 8%) y sugiere revisar el
           enfoque general de la campaña, no solo la ejecución puntual.
 
        2. **La duración de la llamada es el indicador más asociado al éxito.**
           Los contactos más largos se asocian con mayor aceptación, lo que sugiere que
           la calidad de la conversación (no solo el volumen de llamadas) importa para
           el resultado comercial.
 
        3. **El perfil educativo y el canal de contacto influyen en la respuesta.**
           Se observan diferencias claras en la tasa de aceptación según `education` y
           `contact`, lo que permite priorizar segmentos y canales más receptivos.
 
        4. **Existe información faltante disfrazada como 'unknown'** en variables clave
           como `job`, `education` y `default`, que debe tratarse explícitamente en
           futuros análisis para no sesgar las conclusiones.
 
        5. **Los indicadores macroeconómicos (`emp.var.rate`, `euribor3m`,
           `cons.conf.idx`) varían junto con los resultados de la campaña**, lo que
           sugiere que el contexto económico general condiciona la efectividad
           comercial y debería monitorearse al planificar campañas futuras.
        """
        )
 
        st.info(
            "💡 Recomendación: usar estos hallazgos para **rediseñar el guion de llamada**, "
            "priorizar segmentos con mayor propensión histórica y ajustar el momento de la "
            "campaña según el contexto macroeconómico, antes de considerar un modelo "
            "predictivo formal."
        )
