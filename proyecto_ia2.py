import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURACIÓN
# =====================================================
st.set_page_config(page_title="Dashboard RRHH", layout="wide")
st.title("Dashboard de Analítica de RRHH con Streamlit & IA")

# =====================================================
# CARGA DATA
# =====================================================
DATA_URL = "https://raw.githubusercontent.com/bdelgado/Proyectos/master/employees.csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url, sep=None, engine="python", on_bad_lines="skip")
    return df

df = load_data(DATA_URL)

# =====================================================
# LIMPIEZA
# =====================================================
df.columns = df.columns.str.strip()

df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
df["YearsAtCompany"] = pd.to_numeric(df["YearsAtCompany"], errors="coerce")
df["PerformanceScore"] = pd.to_numeric(df["PerformanceScore"], errors="coerce")
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

# =====================================================
# FILTROS
# =====================================================
st.sidebar.header("Filtros")

departamentos = st.sidebar.multiselect(
    "Departamento",
    df["Department"].unique(),
    default=df["Department"].unique()
)


# Filtro por rango salarial
min_salary = int(df["Salary"].min())
max_salary = int(df["Salary"].max())

rango_salario = st.sidebar.slider(
    "Rango de Sueldo",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary)
)

# Aplicar filtros
df = df[
    (df["Department"].isin(departamentos)) &
    (df["Salary"] >= rango_salario[0]) &
    (df["Salary"] <= rango_salario[1])
]

# =====================================================
# KPIs SUPERIORES
# =====================================================
total_empleados = len(df)
salario_promedio = df["Salary"].mean()
departamento_mayor = df["Department"].value_counts().idxmax()
antiguedad_promedio = df["YearsAtCompany"].mean()
desempeno_promedio = df["PerformanceScore"].mean()
edad_promedio = df["Age"].mean()

k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Total Empleados", total_empleados)
k2.metric("Salario Promedio", f"${salario_promedio:,.0f}")
k3.metric("Depto Más Grande", departamento_mayor)
k4.metric("Antigüedad Promedio", f"{antiguedad_promedio:.1f} años")
k5.metric("Desempeño Promedio", f"{desempeno_promedio:.1f}")
k6.metric("Edad Promedio", f"{edad_promedio:.1f} años")

st.markdown("---")

# =====================================================
# 1️⃣ DISTRIBUCIÓN DE SALARIOS
# =====================================================
st.subheader("Distribución de Salarios")

col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(
        df,
        x="Salary",
        nbins=20,
        title="Histograma de Salarios",
        template="plotly_white"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(
        df,
        y="Salary",
        title="Boxplot de Salarios",
        template="plotly_white"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# =====================================================
# 2️⃣ EMPLEADOS POR DEPARTAMENTO
# =====================================================
st.subheader("Empleados por Departamento")

conteo_dept = df["Department"].value_counts().reset_index()
conteo_dept.columns = ["Department", "Cantidad"]

fig_bar = px.bar(
    conteo_dept,
    x="Department",
    y="Cantidad",
    color="Department",
    title="Cantidad de Empleados por Departamento",
    template="plotly_white"
)

st.plotly_chart(fig_bar, use_container_width=True)

# =====================================================
# 3️⃣ RELACIÓN ANTIGÜEDAD VS SALARIO
# =====================================================
st.subheader("Relación Antigüedad vs Salario")

fig_scatter = px.scatter(
    df,
    x="YearsAtCompany",
    y="Salary",
    color="Department",
    size="PerformanceScore",
    hover_data=["Name", "Position"],
    title="Antigüedad vs Salario",
    template="plotly_white"
)

st.plotly_chart(fig_scatter, use_container_width=True)