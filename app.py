"""
Dashboard narrativo: Desacoplo energético en América Latina (2000-actualidad)
Curso: Data Visualization - "El Dashboard que Convence"
Paleta: Sostenibilidad (verdes/neutros)

Incluye en un solo archivo: 
- Fase 2: exploración y limpieza del dataset (roles 1-3)
- Fase 4: dashboard narrativo con Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- CONFIG --------------------
st.set_page_config(page_title="El desacoplo pendiente: energía en LatAm", layout="wide")

PRIMARY = "#2a9d8f"        # dato principal (renovables)
ACCENT = "#e76f51"         # hallazgo clave / rezagados
CONTEXT = "#8d99ae"        # datos de contexto
ANNOTATION_BG = "#e9c46a"  # acento secundario para anotaciones

LATAM_COUNTRIES = [
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica",
    "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala",
    "Honduras", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru",
    "Uruguay", "Venezuela"
]

DATA_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

RAW_COLS = [
    "country", "year", "population", "gdp",
    "renewables_share_energy", "renewables_share_elec",
    "fossil_share_energy", "low_carbon_share_elec",
    "greenhouse_gas_emissions", "energy_per_capita",
    "per_capita_electricity", "primary_energy_consumption"
]


# ==================== FASE 2: EXPLORACION Y LIMPIEZA ====================

# --------- Rol 2: filtrado de países y columnas relevantes ---------
@st.cache_data(ttl=86400)
def load_and_filter():
    df = pd.read_csv(DATA_URL, usecols=lambda c: c in RAW_COLS)
    df = df[df["country"].isin(LATAM_COUNTRIES)]
    df = df[df["year"] >= 2000]
    return df


# --------- Rol 1: cobertura temporal y nulos por columna ---------
@st.cache_data(ttl=86400)
def audit_data(df):
    cobertura = df.groupby("country")["year"].agg(["min", "max", "count"])
    nulos = (df[RAW_COLS].isna().mean() * 100).round(1).sort_values(ascending=False)
    cobertura_energy = df.dropna(subset=["renewables_share_energy"])["country"].nunique()
    cobertura_elec = df.dropna(subset=["renewables_share_elec"])["country"].nunique()
    return {
        "cobertura": cobertura,
        "nulos": nulos,
        "cobertura_energy": cobertura_energy,
        "cobertura_elec": cobertura_elec,
    }


# --------- Rol 3: métricas derivadas ---------
def add_derived_metrics(df):
    df = df.copy()
    df["gdp_per_capita"] = df["gdp"] / df["population"]
    # Dependencia fósil de la electricidad = 100 - baja en carbono
    # (proxy con cobertura completa: renewables_share_energy y fossil_share_energy
    #  solo cubren 8/19 países en el rango 2000+, ver auditoría abajo)
    df["fossil_dependency_elec"] = 100 - df["low_carbon_share_elec"]
    return df


df_raw = load_and_filter()

if df_raw.empty:
    st.error("No se pudieron cargar datos. Verifica tu conexión.")
    st.stop()

audit = audit_data(df_raw)
df = add_derived_metrics(df_raw)

max_year = int(df["year"].max())
min_year = int(df["year"].min())

# -------------------- SIDEBAR: AUDITORIA DE LIMPIEZA (Fase 2) --------------------
with st.sidebar.expander("Fase 2 — Auditoría de limpieza del dataset"):
    st.markdown(
        f"**Cobertura de variables clave:**\n"
        f"- `renewables_share_energy` / `fossil_share_energy`: solo "
        f"{audit['cobertura_energy']}/19 países con dato.\n"
        f"- `renewables_share_elec` / `low_carbon_share_elec`: "
        f"{audit['cobertura_elec']}/19 países con dato.\n\n"
        f"**Decisión:** se descartaron las variables de energía total por baja "
        f"cobertura y se usaron las de electricidad como eje del storytelling."
    )
    st.caption("% de nulos por columna:")
    st.dataframe(audit["nulos"], width="stretch")
    st.caption("Cobertura temporal por país:")
    st.dataframe(audit["cobertura"], width="stretch")

# -------------------- SIDEBAR: FILTROS (propósito narrativo) --------------------
st.sidebar.header("Explora la historia")
st.sidebar.caption(
    "Usa estos filtros para comprobar si el patrón regional se sostiene "
    "en países o periodos específicos, sin perder la comparación con la región."
)

year_range = st.sidebar.slider(
    "Rango de años a analizar",
    min_value=min_year, max_value=max_year,
    value=(min_year, max_year)
)

selected_countries = st.sidebar.multiselect(
    "Países a resaltar en la línea de tiempo",
    options=sorted(df["country"].unique()),
    default=["Brazil", "Uruguay", "Costa Rica", "Venezuela", "Mexico"]
)

df_f = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
latest_year_f = df_f["year"].max()

# ==================== FASE 4: DASHBOARD NARRATIVO ====================

# -------------------- TITULO NARRATIVO --------------------
st.title("El desacoplo pendiente: pocos países de LatAm electrifican sin depender de fósiles")
st.markdown(
    "Un puñado de países ha aumentado la participación de renovables en su matriz eléctrica "
    "mientras su economía crece; la mayoría de la región sigue atada a los combustibles fósiles."
)

st.divider()

# -------------------- GRAFICO 1: Evolución renovables (línea) --------------------
st.subheader("1. La transición eléctrica hacia renovables no es pareja en la región")

line_df = df_f[df_f["country"].isin(selected_countries)].dropna(subset=["renewables_share_elec"])
palette_line = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"]  # paleta completa

fig1 = px.line(
    line_df, x="year", y="renewables_share_elec", color="country",
    color_discrete_sequence=palette_line,
    labels={"renewables_share_elec": "% renovables en generación eléctrica", "year": "Año"},
)
fig1.update_traces(line=dict(width=3))

# Anotación de hallazgo: país con mayor incremento en el rango filtrado
delta_df = (
    df_f.dropna(subset=["renewables_share_elec"])
    .sort_values("year")
    .groupby("country")["renewables_share_elec"]
    .agg(["first", "last"])
)
delta_df["incremento"] = delta_df["last"] - delta_df["first"]
if not delta_df.empty:
    top_country = delta_df["incremento"].idxmax()
    top_value = delta_df.loc[top_country, "incremento"]
    top_last_year_val = df_f[(df_f["country"] == top_country)].dropna(
        subset=["renewables_share_elec"]).sort_values("year").iloc[-1]

    fig1.add_annotation(
        x=top_last_year_val["year"], y=top_last_year_val["renewables_share_elec"],
        text=f"{top_country}: +{top_value:.1f} pts en el periodo",
        showarrow=True, arrowhead=2, bgcolor=ANNOTATION_BG, bordercolor="#333",
        font=dict(color="#333", size=12)
    )

fig1.update_layout(plot_bgcolor="white", legend_title_text="País")
st.plotly_chart(fig1, width="stretch")

st.divider()

# -------------------- GRAFICO 2: Dispersión GDP vs renovables --------------------
st.subheader("2. ¿Crecer implica renunciar a las renovables? No siempre")

# gdp tiene menos cobertura reciente que renewables_share_elec, así que se usa
# el último año dentro del rango filtrado donde ambas variables tengan dato.
gdp_available = df_f.dropna(subset=["gdp_per_capita", "renewables_share_elec"])
if gdp_available.empty:
    st.warning("No hay datos de PBI disponibles en el rango de años seleccionado.")
else:
    latest_year_gdp = gdp_available["year"].max()
    scatter_df = df_f[df_f["year"] == latest_year_gdp].dropna(
        subset=["gdp_per_capita", "renewables_share_elec", "population"]
    )

    fig2 = px.scatter(
        scatter_df, x="gdp_per_capita", y="renewables_share_elec",
        size="population", color="fossil_dependency_elec",
        color_continuous_scale=["#2a9d8f", "#e9c46a", "#e76f51"],
        hover_name="country",
        labels={
            "gdp_per_capita": "PBI per cápita (USD)",
            "renewables_share_elec": "% renovables en generación eléctrica",
            "fossil_dependency_elec": "% dependencia fósil (elec.)"
        },
        log_x=True,
    )
    fig2.update_layout(plot_bgcolor="white")
    fig2.add_annotation(
        xref="paper", yref="paper", x=0.02, y=0.98,
        text=f"Año de referencia: {int(latest_year_gdp)} (último con dato de PBI). El color revela dependencia fósil.",
        showarrow=False, bgcolor=ANNOTATION_BG, font=dict(size=11, color="#333")
    )
    st.plotly_chart(fig2, width="stretch")

st.divider()

# -------------------- GRAFICO 3: Ranking fósiles --------------------
st.subheader("3. Los rezagados: quiénes siguen dependiendo de fósiles para generar electricidad")

bar_df = df_f[df_f["year"] == latest_year_f].dropna(subset=["fossil_dependency_elec"]).sort_values(
    "fossil_dependency_elec", ascending=True
)
median_fossil = bar_df["fossil_dependency_elec"].median()
bar_df["categoria"] = bar_df["fossil_dependency_elec"].apply(
    lambda v: "Por encima de la mediana regional" if v >= median_fossil else "Por debajo de la mediana regional"
)

fig3 = px.bar(
    bar_df, x="fossil_dependency_elec", y="country", orientation="h",
    color="categoria",
    color_discrete_map={
        "Por encima de la mediana regional": ACCENT,
        "Por debajo de la mediana regional": PRIMARY,
    },
    labels={"fossil_dependency_elec": "% dependencia fósil en generación eléctrica", "country": ""},
)
fig3.add_vline(x=median_fossil, line_dash="dash", line_color=CONTEXT,
                annotation_text=f"Mediana regional: {median_fossil:.1f}%")
fig3.update_layout(plot_bgcolor="white", legend_title_text="")
st.plotly_chart(fig3, width="stretch")

st.caption(
    "Fuente: Our World in Data - World Energy Consumption. "
    f"Datos filtrados a países de América Latina, {year_range[0]}-{year_range[1]}."
)