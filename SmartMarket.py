import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(
    page_title="SmartMarket – Marketing Dashboard",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    return pd.read_csv("data/smartmarket_dashboard_data.csv")

df = load_data()

# ==================================================
# KPI CALCULATIONS
# ==================================================
df["CTR"] = df["clicks"] / df["impressions"]
df["ConversionRate"] = df["conversions"] / df["clicks"]
df["CPC"] = df["cost"] / df["clicks"]
df["CPA"] = df["cost"] / df["conversions"]

# ==================================================
# SIDEBAR NAVIGATION
# ==================================================
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Aller vers :",
    ["📊 Dashboard", "📘 KPI Listing"]
)

# ==================================================
# PAGE 1 – DASHBOARD
# ==================================================
if page == "📊 Dashboard":

    st.title("📊 SmartMarket – Marketing Performance Dashboard")
    st.markdown("Analyse des performances marketing – Septembre 2025")

    # KPI
    st.subheader("🔑 Indicateurs clés")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("CTR moyen", f"{df['CTR'].mean():.2%}")
    col2.metric("Taux de conversion", f"{df['ConversionRate'].mean():.2%}")
    col3.metric("CPC moyen (€)", f"{df['CPC'].mean():.2f}")
    col4.metric("CPA moyen (€)", f"{df['CPA'].mean():.2f}")

    st.divider()

    # -----------------------------
    # VISUALISATIONS
    # -----------------------------
    st.subheader("📈 Analyses visuelles")

    # 1. Conversions par canal
    fig1 = px.bar(
        df.groupby("channel", as_index=False)["conversions"].sum(),
        x="channel",
        y="conversions",
        title="Conversions par canal"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2. CTR par canal
    fig2 = px.bar(
        df.groupby("channel", as_index=False)["CTR"].mean(),
        x="channel",
        y="CTR",
        title="CTR moyen par canal"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Coût vs Conversions
    fig3 = px.scatter(
        df,
        x="cost",
        y="conversions",
        color="channel",
        size="clicks",
        title="Relation coût / conversions par canal"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Statuts CRM par région
    fig4 = px.histogram(
        df,
        x="region",
        color="status",
        title="Répartition des statuts CRM par région",
        barmode="stack"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # 5. Conversions par secteur
    fig5 = px.pie(
        df,
        names="sector",
        values="conversions",
        title="Part des conversions par secteur"
    )
    st.plotly_chart(fig5, use_container_width=True)

# ==================================================
# PAGE 2 – KPI LISTING
# ==================================================
elif page == "📘 KPI Listing":

    st.title("📘 KPI Marketing – Définitions & Interprétation")

    st.markdown("""
    Cette page présente les indicateurs clés utilisés dans le dashboard
    ainsi que leur interprétation métier.
    """)

    st.subheader("🔑 KPI utilisés")

    st.markdown("""
    ### 1️⃣ CTR – Click Through Rate  
    **Formule :** CTR = clicks / impressions  

    **Interprétation métier :**  
    Mesure l’attractivité d’une campagne et la pertinence du ciblage.
    """)

    st.markdown("""
    ### 2️⃣ Taux de conversion  
    **Formule :** ConversionRate = conversions / clicks  

    **Interprétation métier :**  
    Évalue l’efficacité du parcours utilisateur après le clic.
    """)

    st.markdown("""
    ### 3️⃣ CPC – Cost Per Click  
    **Formule :** CPC = cost / clicks  

    **Interprétation métier :**  
    Mesure le coût d’acquisition de trafic.
    """)

    st.markdown("""
    ### 4️⃣ CPA – Cost Per Acquisition  
    **Formule :** CPA = cost / conversions  

    **Interprétation métier :**  
    KPI central pour mesurer la rentabilité marketing.
    """)

    st.markdown("""
    ### 5️⃣ KPI complémentaire – Volume de conversions  
    **Interprétation métier :**  
    Permet d’identifier les canaux et segments les plus créateurs de valeur.
    """)
