import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Page Configuration ----------
st.set_page_config(page_title="Job Finder by City", layout="wide")

# ---------- App Title ----------
st.title("📍 Job Finder by City")
st.markdown("Use this tool to explore job listings across Indian cities. Data is fetched from a shared dataset.")

# ---------- Load CSV from Google Drive ----------
FILE_ID = "15Z43942G9E9IWRtaULNhkCGGZBqUqOeC"  # Replace with your actual file ID
CSV_URL = f"https://drive.google.com/uc?id={FILE_ID}"

try:
    # Load dataset
    df = pd.read_csv(CSV_URL)

    # ---------- Data Cleaning ----------
    df.columns = df.columns.str.lower().str.strip()
    required_columns = {"job title", "city", "salary", "locality"}

    if not required_columns.issubset(df.columns):
        st.error("❌ Your CSV file must contain the following columns: **job title**, **city**, **salary**, **locality**")
    else:
        df["city"] = df["city"].astype(str).str.strip().str.title()
        df["salary"] = pd.to_numeric(df["salary"].astype(str).str.replace(r"[^\d.]", "", regex=True), errors='coerce')

        # ---------- Sidebar: City Selection ----------
        with st.sidebar:
            st.header("🔎 Filter Jobs")
            cities = sorted(df["city"].dropna().unique())
            selected_city = st.selectbox("Select a City", cities)

        # ---------- Filtered Data ----------
        results = df[df["city"] == selected_city]

        # ---------- Layout: Two Columns ----------
        col1, col2 = st.columns([1, 2])

        # ---------- Column 1: Job Listings ----------
        with col1:
            st.subheader(f"🧑‍💼 Available Jobs in {selected_city}")
            if not results.empty:
                for _, row in results.iterrows():
                    st.markdown(f"""
                    <div style="margin-bottom:15px; padding:10px; border:1px solid #e0e0e0; border-radius:8px; background-color:#f9f9f9;">
                        <h5 style="margin:0;">🧑‍💼 {row['job title']}</h5>
                        <p style="margin:0;">📍 <strong>{row['locality']}</strong><br>💰 Salary: <strong>{row['salary']}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No jobs found for the selected city.")

        # ---------- Column 2: Charts ----------
        with col2:
            if not results.empty:
                # --- Salary Distribution ---
                st.subheader("📊 Salary Distribution")
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.histplot(results["salary"].dropna(), bins=15, kde=True, ax=ax, color="skyblue")
                ax.set_xlabel("Salary")
                ax.set_ylabel("Count")
                ax.set_title(f"Salary Distribution in {selected_city}")
                st.pyplot(fig)

                # --- Jobs by Locality ---
                st.subheader("🏨 Jobs by Locality")
                locality_counts = results["locality"].value_counts().head(10)
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                sns.barplot(x=locality_counts.values, y=locality_counts.index, ax=ax2, palette="viridis")
                ax2.set_xlabel("Number of Jobs")
                ax2.set_ylabel("Locality")
                ax2.set_title(f"Top Hiring Localities in {selected_city}")
                st.pyplot(fig2)

except Exception as e:
    st.error(f"❌ Error while processing the file: {e}")
