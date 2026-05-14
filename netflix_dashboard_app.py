
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Netflix Movies & TV Shows Dashboard",
    layout="wide"
)

st.title("🎬 Netflix Movies & TV Shows Dashboard")
st.markdown("Interactive analytics dashboard for Netflix dataset")

# --------------------------------
# LOAD DATA
# --------------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload Netflix Dataset",
    type=["csv", "xlsx"]
)

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df

if uploaded_file:

    df = load_data(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # --------------------------------
    # CLEANING
    # --------------------------------
    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    if 'release_year' in df.columns:
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

    # --------------------------------
    # KPI METRICS
    # --------------------------------
    st.subheader("📌 Key Insights")

    total_titles = len(df)

    total_movies = len(df[df['type'] == 'Movie']) if 'type' in df.columns else 0
    total_tv = len(df[df['type'] == 'TV Show']) if 'type' in df.columns else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Titles", total_titles)
    col2.metric("Movies", total_movies)
    col3.metric("TV Shows", total_tv)

    # --------------------------------
    # GRAPH 1 - CONTENT TYPE
    # --------------------------------
    st.subheader("1️⃣ Movies vs TV Shows")

    fig1, ax1 = plt.subplots()

    df['type'].value_counts().plot(
        kind='bar',
        ax=ax1
    )

    ax1.set_xlabel("Type")
    ax1.set_ylabel("Count")

    st.pyplot(fig1)

    # --------------------------------
    # GRAPH 2 - RELEASE YEAR TREND
    # --------------------------------
    st.subheader("2️⃣ Content Released by Year")

    fig2, ax2 = plt.subplots(figsize=(10,5))

    df['release_year'].value_counts().sort_index().plot(
        ax=ax2
    )

    ax2.set_xlabel("Release Year")
    ax2.set_ylabel("Number of Titles")

    st.pyplot(fig2)

    # --------------------------------
    # GRAPH 3 - TOP COUNTRIES
    # --------------------------------
    if 'country' in df.columns:

        st.subheader("3️⃣ Top Countries Producing Content")

        top_countries = (
            df['country']
            .dropna()
            .str.split(', ')
            .explode()
            .value_counts()
            .head(10)
        )

        fig3, ax3 = plt.subplots(figsize=(10,5))

        top_countries.plot(
            kind='bar',
            ax=ax3
        )

        ax3.set_xlabel("Country")
        ax3.set_ylabel("Titles")

        st.pyplot(fig3)

    # --------------------------------
    # GRAPH 4 - RATINGS DISTRIBUTION
    # --------------------------------
    if 'rating' in df.columns:

        st.subheader("4️⃣ Ratings Distribution")

        fig4, ax4 = plt.subplots(figsize=(10,5))

        df['rating'].value_counts().head(10).plot(
            kind='bar',
            ax=ax4
        )

        ax4.set_xlabel("Rating")
        ax4.set_ylabel("Count")

        st.pyplot(fig4)

    # --------------------------------
    # GRAPH 5 - TOP GENRES
    # --------------------------------
    if 'listed_in' in df.columns:

        st.subheader("5️⃣ Most Popular Genres")

        genres = (
            df['listed_in']
            .dropna()
            .str.split(', ')
            .explode()
            .value_counts()
            .head(10)
        )

        fig5, ax5 = plt.subplots(figsize=(10,5))

        genres.plot(
            kind='bar',
            ax=ax5
        )

        ax5.set_xlabel("Genre")
        ax5.set_ylabel("Count")

        st.pyplot(fig5)

    # --------------------------------
    # GRAPH 6 - CONTENT ADDED OVER TIME
    # --------------------------------
    if 'date_added' in df.columns:

        st.subheader("6️⃣ Content Added to Netflix Over Time")

        added = (
            df['date_added']
            .dt.year
            .value_counts()
            .sort_index()
        )

        fig6, ax6 = plt.subplots(figsize=(10,5))

        added.plot(
            ax=ax6
        )

        ax6.set_xlabel("Year Added")
        ax6.set_ylabel("Titles Added")

        st.pyplot(fig6)

    # --------------------------------
    # GRAPH 7 - DURATION ANALYSIS
    # --------------------------------
    if 'duration' in df.columns:

        st.subheader("7️⃣ Movie Duration Distribution")

        movie_df = df[df['type'] == 'Movie'].copy()

        movie_df['duration_int'] = (
            movie_df['duration']
            .str.extract('(\d+)')
            .astype(float)
        )

        fig7, ax7 = plt.subplots(figsize=(10,5))

        ax7.hist(movie_df['duration_int'].dropna(), bins=20)

        ax7.set_xlabel("Duration (Minutes)")
        ax7.set_ylabel("Frequency")

        st.pyplot(fig7)

    # --------------------------------
    # GRAPH 8 - PIE CHART
    # --------------------------------
    st.subheader("8️⃣ Content Share")

    fig8, ax8 = plt.subplots()

    df['type'].value_counts().plot(
        kind='pie',
        autopct='%1.1f%%',
        ax=ax8
    )

    ax8.set_ylabel("")

    st.pyplot(fig8)

    # --------------------------------
    # RAW DATA DOWNLOAD
    # --------------------------------
    st.subheader("⬇ Download Processed Dataset")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download CSV",
        csv,
        "processed_netflix_data.csv",
        "text/csv"
    )

else:
    st.info("⬅ Upload your Netflix dataset to begin.")
