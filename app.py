import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Global Seismic Trends",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# LOAD COMPRESSED CSV DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = "global_earthquake_cleaned.csv.gz"

    df = pd.read_csv(
        file_path,
        compression="gzip"
    )

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    df["updated"] = pd.to_datetime(
        df["updated"],
        errors="coerce"
    )

    numeric_columns = [
        "latitude",
        "longitude",
        "depth_km",
        "mag",
        "sig",
        "nst",
        "dmin",
        "rms",
        "gap",
        "magError",
        "depthError",
        "magNst",
        "year",
        "month",
        "day",
        "strong_earthquake",
        "tsunami"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "❌ global_earthquake_cleaned.csv.gz was not found. "
        "Make sure the file is in the same folder as app.py."
    )

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🌍 Global Seismic Trends")

st.subheader(
    "Data-Driven Earthquake Insights"
)

st.markdown(
    """
    This dashboard analyzes global earthquake data using
    **Python, Pandas, Streamlit and Plotly**.

    **Dataset:** USGS Earthquake Records  
    **Records:** 136,973  
    **Time Period:** 2021–2026
    """
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


available_years = sorted(
    df["year"]
    .dropna()
    .astype(int)
    .unique()
)

selected_years = st.sidebar.multiselect(
    "Select Year",
    available_years,
    default=available_years
)


min_magnitude = float(
    df["mag"].dropna().min()
)

max_magnitude = float(
    df["mag"].dropna().max()
)

selected_magnitude = st.sidebar.slider(
    "Magnitude Range",
    min_value=min_magnitude,
    max_value=max_magnitude,
    value=(
        min_magnitude,
        max_magnitude
    ),
    step=0.1
)


depth_options = [
    "Shallow",
    "Intermediate",
    "Deep"
]

selected_depth = st.sidebar.multiselect(
    "Depth Category",
    depth_options,
    default=depth_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["year"].isin(selected_years))
    &
    (df["mag"] >= selected_magnitude[0])
    &
    (df["mag"] <= selected_magnitude[1])
    &
    (df["depth_category"].isin(selected_depth))
].copy()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📊 Dashboard Sections",
    [
        "Overview",
        "Strength & Depth",
        "Time Analysis",
        "Geographic Analysis",
        "Magnitude Analysis",
        "Network & Data Quality",
        "Event Analysis",
        "Earthquake Map",
        "Detailed Data"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Earthquakes",
            f"{len(filtered_df):,}"
        )

    with col2:

        st.metric(
            "Average Magnitude",
            f"{filtered_df['mag'].mean():.2f}"
        )

    with col3:

        st.metric(
            "Maximum Magnitude",
            f"{filtered_df['mag'].max():.1f}"
        )

    with col4:

        st.metric(
            "Average Depth",
            f"{filtered_df['depth_km'].mean():.2f} km"
        )

    st.markdown("---")

    strong_count = filtered_df[
        filtered_df["strong_earthquake"] == 1
    ].shape[0]

    tsunami_count = filtered_df[
        filtered_df["tsunami"] == 1
    ].shape[0]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Strong Earthquakes (≥ 6.0)",
            f"{strong_count:,}"
        )

    with col2:

        st.metric(
            "Tsunami Flagged Events",
            f"{tsunami_count:,}"
        )

    with col3:

        st.metric(
            "Countries / Regions",
            f"{filtered_df['country'].nunique():,}"
        )

    st.markdown("---")

    st.subheader(
        "Magnitude Distribution"
    )

    fig = px.histogram(
        filtered_df,
        x="mag",
        nbins=40,
        title="Distribution of Earthquake Magnitudes"
    )

    fig.update_layout(
        xaxis_title="Magnitude",
        yaxis_title="Number of Earthquakes"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# STRENGTH & DEPTH
# ============================================================

elif page == "Strength & Depth":

    st.header("💥 Strength & Depth Analysis")

    st.subheader(
        "1️⃣ Top 10 Strongest Earthquakes"
    )

    top_10_strongest = filtered_df[
        [
            "id",
            "time",
            "place",
            "mag",
            "depth_km"
        ]
    ].sort_values(
        by="mag",
        ascending=False
    ).head(10)

    st.dataframe(
        top_10_strongest,
        use_container_width=True
    )

    st.subheader(
        "2️⃣ Top 10 Deepest Earthquakes"
    )

    top_10_deepest = filtered_df[
        [
            "id",
            "time",
            "place",
            "mag",
            "depth_km"
        ]
    ].sort_values(
        by="depth_km",
        ascending=False
    ).head(10)

    st.dataframe(
        top_10_deepest,
        use_container_width=True
    )

    st.subheader(
        "3️⃣ Shallow Earthquakes with Magnitude > 7.5"
    )

    shallow_strong = filtered_df[
        (filtered_df["depth_km"] < 50)
        &
        (filtered_df["mag"] > 7.5)
    ][
        [
            "id",
            "time",
            "place",
            "mag",
            "depth_km"
        ]
    ].sort_values(
        by="mag",
        ascending=False
    )

    st.write(
        f"Number of events: **{len(shallow_strong)}**"
    )

    st.dataframe(
        shallow_strong,
        use_container_width=True
    )

    st.subheader(
        "Depth Category Distribution"
    )

    depth_counts = (
        filtered_df["depth_category"]
        .value_counts()
        .reset_index()
    )

    depth_counts.columns = [
        "depth_category",
        "count"
    ]

    fig = px.bar(
        depth_counts,
        x="depth_category",
        y="count",
        title="Earthquakes by Depth Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TIME ANALYSIS
# ============================================================

elif page == "Time Analysis":

    st.header("⏰ Time-Based Analysis")

    st.subheader(
        "6️⃣ Earthquakes by Year"
    )

    yearly = (
        filtered_df
        .groupby("year")
        .size()
        .reset_index(
            name="earthquake_count"
        )
        .sort_values("year")
    )

    fig = px.bar(
        yearly,
        x="year",
        y="earthquake_count",
        title="Earthquake Count by Year"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        yearly,
        use_container_width=True
    )

    st.subheader(
        "7️⃣ Earthquakes by Month"
    )

    monthly = (
        filtered_df
        .groupby("month")
        .size()
        .reset_index(
            name="earthquake_count"
        )
        .sort_values("month")
    )

    fig = px.bar(
        monthly,
        x="month",
        y="earthquake_count",
        title="Earthquake Count by Month"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "8️⃣ Earthquakes by Day of Week"
    )

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    daily = (
        filtered_df["day_of_week"]
        .value_counts()
        .reindex(day_order)
        .fillna(0)
        .reset_index()
    )

    daily.columns = [
        "day_of_week",
        "earthquake_count"
    ]

    fig = px.bar(
        daily,
        x="day_of_week",
        y="earthquake_count",
        title="Earthquakes by Day of Week"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "9️⃣ Earthquakes by Hour"
    )

    hourly_df = filtered_df.copy()

    hourly_df["hour"] = (
        hourly_df["time"].dt.hour
    )

    hourly = (
        hourly_df
        .groupby("hour")
        .size()
        .reset_index(
            name="earthquake_count"
        )
        .sort_values("hour")
    )

    fig = px.line(
        hourly,
        x="hour",
        y="earthquake_count",
        markers=True,
        title="Earthquake Count by Hour"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "1️⃣9️⃣ Tsunami-Flagged Earthquakes by Year"
    )

    tsunami_year = (
        filtered_df[
            filtered_df["tsunami"] == 1
        ]
        .groupby("year")
        .size()
        .reset_index(
            name="tsunami_events"
        )
    )

    fig = px.bar(
        tsunami_year,
        x="year",
        y="tsunami_events",
        title="Tsunami-Flagged Events by Year"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "2️⃣3️⃣ Year-over-Year Earthquake Growth"
    )

    yearly_growth = (
        filtered_df
        .groupby("year")
        .size()
        .reset_index(
            name="earthquake_count"
        )
        .sort_values("year")
    )

    yearly_growth["previous_year_count"] = (
        yearly_growth[
            "earthquake_count"
        ].shift(1)
    )

    yearly_growth["growth_percent"] = (
        (
            yearly_growth["earthquake_count"]
            -
            yearly_growth["previous_year_count"]
        )
        /
        yearly_growth["previous_year_count"]
        *
        100
    )

    yearly_growth["growth_percent"] = (
        yearly_growth[
            "growth_percent"
        ].round(2)
    )

    st.dataframe(
        yearly_growth,
        use_container_width=True
    )


# ============================================================
# GEOGRAPHIC ANALYSIS
# ============================================================

elif page == "Geographic Analysis":

    st.header("🌎 Geographic Analysis")

    st.subheader(
        "2️⃣1️⃣ Countries with Highest Average Magnitude"
    )

    country_avg = (
        filtered_df[
            filtered_df["country"].notna()
            &
            (filtered_df["country"] != "")
        ]
        .groupby("country")
        .agg(
            earthquake_count=("mag", "count"),
            average_magnitude=("mag", "mean")
        )
        .reset_index()
        .sort_values(
            "average_magnitude",
            ascending=False
        )
        .head(10)
    )

    country_avg["average_magnitude"] = (
        country_avg[
            "average_magnitude"
        ].round(2)
    )

    st.dataframe(
        country_avg,
        use_container_width=True
    )

    st.subheader(
        "2️⃣2️⃣ Countries with Both Shallow and Deep Earthquakes"
    )

    shallow = (
        filtered_df[
            filtered_df["depth_km"] <= 300
        ]
        .groupby(
            [
                "country",
                "year",
                "month"
            ]
        )
        .size()
        .reset_index(
            name="shallow_count"
        )
    )

    deep = (
        filtered_df[
            filtered_df["depth_km"] > 600
        ]
        .groupby(
            [
                "country",
                "year",
                "month"
            ]
        )
        .size()
        .reset_index(
            name="deep_count"
        )
    )

    both = pd.merge(
        shallow,
        deep,
        on=[
            "country",
            "year",
            "month"
        ],
        how="inner"
    )

    st.write(
        f"Country-year-month combinations: **{len(both)}**"
    )

    st.dataframe(
        both,
        use_container_width=True
    )

    st.subheader(
        "2️⃣4️⃣ Top 3 Most Active Regions"
    )

    region_activity = (
        filtered_df[
            filtered_df["region"].notna()
            &
            (filtered_df["region"] != "")
        ]
        .groupby("region")
        .agg(
            earthquake_count=("mag", "count"),
            average_magnitude=("mag", "mean")
        )
        .reset_index()
    )

    region_activity["activity_score"] = (
        region_activity["earthquake_count"]
        *
        region_activity["average_magnitude"]
    )

    region_activity = (
        region_activity
        .sort_values(
            "activity_score",
            ascending=False
        )
        .head(3)
    )

    region_activity[
        "average_magnitude"
    ] = (
        region_activity[
            "average_magnitude"
        ].round(2)
    )

    region_activity[
        "activity_score"
    ] = (
        region_activity[
            "activity_score"
        ].round(2)
    )

    st.dataframe(
        region_activity,
        use_container_width=True
    )

    st.info(
        "Activity Score = earthquake frequency × average magnitude. "
        "This is a project-defined indicator, not an official seismic hazard index."
    )

    st.subheader(
        "2️⃣5️⃣ Average Depth Near the Equator (±5° Latitude)"
    )

    equator_df = filtered_df[
        filtered_df["latitude"].between(-5, 5)
    ]

    equator_analysis = (
        equator_df[
            equator_df["country"].notna()
        ]
        .groupby("country")
        .agg(
            earthquake_count=("depth_km", "count"),
            average_depth=("depth_km", "mean")
        )
        .reset_index()
        .sort_values(
            "average_depth",
            ascending=False
        )
    )

    equator_analysis[
        "average_depth"
    ] = (
        equator_analysis[
            "average_depth"
        ].round(2)
    )

    st.dataframe(
        equator_analysis,
        use_container_width=True
    )

    st.subheader(
        "2️⃣6️⃣ Highest Shallow-to-Deep Earthquake Ratio"
    )

    shallow_ratio = (
        filtered_df[
            filtered_df["depth_km"] <= 300
        ]
        .groupby("country")
        .size()
        .reset_index(
            name="shallow_count"
        )
    )

    deep_ratio = (
        filtered_df[
            filtered_df["depth_km"] > 600
        ]
        .groupby("country")
        .size()
        .reset_index(
            name="deep_count"
        )
    )

    ratio = pd.merge(
        shallow_ratio,
        deep_ratio,
        on="country",
        how="inner"
    )

    ratio = ratio[
        ratio["deep_count"] > 0
    ]

    ratio[
        "shallow_to_deep_ratio"
    ] = (
        ratio["shallow_count"]
        /
        ratio["deep_count"]
    )

    ratio = (
        ratio
        .sort_values(
            "shallow_to_deep_ratio",
            ascending=False
        )
        .head(10)
    )

    ratio[
        "shallow_to_deep_ratio"
    ] = (
        ratio[
            "shallow_to_deep_ratio"
        ].round(2)
    )

    st.dataframe(
        ratio,
        use_container_width=True
    )

    st.subheader(
        "3️⃣0️⃣ Regions with Highest Deep-Focus Earthquakes"
    )

    deep_regions = (
        filtered_df[
            filtered_df["depth_km"] > 300
        ]
        .groupby("region")
        .size()
        .reset_index(
            name="deep_earthquake_count"
        )
        .sort_values(
            "deep_earthquake_count",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        deep_regions,
        use_container_width=True
    )


# ============================================================
# MAGNITUDE ANALYSIS
# ============================================================

elif page == "Magnitude Analysis":

    st.header("📈 Magnitude Analysis")

    st.subheader(
        "5️⃣ Average Magnitude by Magnitude Type"
    )

    mag_type = (
        filtered_df[
            filtered_df["magType"].notna()
        ]
        .groupby("magType")
        .agg(
            earthquake_count=("mag", "count"),
            average_magnitude=("mag", "mean")
        )
        .reset_index()
        .sort_values(
            "average_magnitude",
            ascending=False
        )
    )

    mag_type[
        "average_magnitude"
    ] = (
        mag_type[
            "average_magnitude"
        ].round(2)
    )

    st.dataframe(
        mag_type,
        use_container_width=True
    )

    fig = px.bar(
        mag_type,
        x="magType",
        y="average_magnitude",
        title="Average Magnitude by Magnitude Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "2️⃣7️⃣ Average Magnitude: Tsunami vs No Tsunami"
    )

    tsunami_comparison = (
        filtered_df
        .groupby("tsunami")
        .agg(
            average_magnitude=("mag", "mean"),
            earthquake_count=("mag", "count")
        )
        .reset_index()
    )

    tsunami_comparison[
        "tsunami"
    ] = (
        tsunami_comparison[
            "tsunami"
        ].map(
            {
                0: "No Tsunami Flag",
                1: "Tsunami Flag"
            }
        )
    )

    tsunami_comparison[
        "average_magnitude"
    ] = (
        tsunami_comparison[
            "average_magnitude"
        ].round(2)
    )

    st.dataframe(
        tsunami_comparison,
        use_container_width=True
    )

    fig = px.bar(
        tsunami_comparison,
        x="tsunami",
        y="average_magnitude",
        title="Average Magnitude: Tsunami vs No Tsunami"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "The tsunami field is a USGS record flag. "
        "It does not by itself prove that a damaging tsunami occurred."
    )


# ============================================================
# NETWORK & DATA QUALITY
# ============================================================

elif page == "Network & Data Quality":

    st.header("📡 Network & Data Quality")

    st.subheader(
        "🔟 Most Active Reporting Networks"
    )

    networks = (
        filtered_df
        .groupby("net")
        .size()
        .reset_index(
            name="earthquake_count"
        )
        .sort_values(
            "earthquake_count",
            ascending=False
        )
    )

    st.dataframe(
        networks,
        use_container_width=True
    )

    fig = px.bar(
        networks.head(10),
        x="net",
        y="earthquake_count",
        title="Top Reporting Networks"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "1️⃣4️⃣ Reviewed vs Automatic Events"
    )

    reviewed = (
        filtered_df[
            "status"
        ]
        .value_counts()
        .reset_index()
    )

    reviewed.columns = [
        "status",
        "earthquake_count"
    ]

    st.dataframe(
        reviewed,
        use_container_width=True
    )

    st.subheader(
        "1️⃣6️⃣ Earthquake Data Types"
    )

    type_counts = {}

    for value in filtered_df[
        "types"
    ].dropna():

        values = str(value).split(",")

        for item in values:

            item = item.strip()

            if item:

                type_counts[item] = (
                    type_counts.get(item, 0) + 1
                )

    type_df = pd.DataFrame(
        list(type_counts.items()),
        columns=[
            "data_type",
            "earthquake_count"
        ]
    ).sort_values(
        "earthquake_count",
        ascending=False
    )

    st.dataframe(
        type_df,
        use_container_width=True
    )

    st.subheader(
        "1️⃣8️⃣ High Station Coverage"
    )

    station_threshold = st.slider(
        "Station Count Threshold",
        min_value=10,
        max_value=300,
        value=100
    )

    high_station = filtered_df[
        filtered_df["nst"] > station_threshold
    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "High Coverage Events",
            f"{len(high_station):,}"
        )

    with col2:

        average_stations = (
            high_station["nst"].mean()
            if len(high_station) > 0
            else 0
        )

        st.metric(
            "Average Stations",
            f"{average_stations:.2f}"
        )

    with col3:

        maximum_stations = (
            high_station["nst"].max()
            if len(high_station) > 0
            else 0
        )

        st.metric(
            "Maximum Stations",
            f"{maximum_stations:.0f}"
        )

    st.subheader(
        "2️⃣8️⃣ Lowest Reliability Indicator"
    )

    reliability = filtered_df[
        filtered_df["gap"].notna()
        &
        filtered_df["rms"].notna()
    ].copy()

    reliability[
        "reliability_indicator"
    ] = (
        reliability["gap"]
        +
        reliability["rms"]
    ) / 2

    reliability = (
        reliability[
            [
                "id",
                "time",
                "place",
                "mag",
                "gap",
                "rms",
                "reliability_indicator"
            ]
        ]
        .sort_values(
            "reliability_indicator",
            ascending=False
        )
        .head(10)
    )

    reliability[
        "reliability_indicator"
    ] = (
        reliability[
            "reliability_indicator"
        ].round(2)
    )

    st.dataframe(
        reliability,
        use_container_width=True
    )

    st.info(
        "Reliability Indicator = (gap + rms) / 2. "
        "This is a project-defined indicator. Gap and RMS have different units, "
        "so this should not be treated as an official USGS reliability score."
    )


# ============================================================
# EVENT ANALYSIS
# ============================================================

elif page == "Event Analysis":

    st.header("⚡ Event Analysis")

    st.subheader(
        "1️⃣5️⃣ Earthquake Count by Event Type"
    )

    event_types = (
        filtered_df[
            "type"
        ]
        .value_counts()
        .reset_index()
    )

    event_types.columns = [
        "event_type",
        "earthquake_count"
    ]

    st.dataframe(
        event_types,
        use_container_width=True
    )

    fig = px.bar(
        event_types,
        x="event_type",
        y="earthquake_count",
        title="Earthquake Count by Event Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader(
        "⚠️ Tasks Requiring Additional Data"
    )

    st.info(
        """
        The current USGS earthquake dataset does not contain the fields
        required to calculate the following tasks:

        **Task 4:** Average depth per continent

        **Task 11:** Top places with highest casualties

        **Task 12:** Total estimated economic loss per continent

        **Task 13:** Average economic loss by alert level

        **Task 17:** Average RMS/GAP per continent

        **Task 20:** Count by alert level

        These require additional geographic, casualty, economic-loss,
        or alert-level data.
        """
    )


# ============================================================
# EARTHQUAKE MAP
# ============================================================

elif page == "Earthquake Map":

    st.header("🗺️ Global Earthquake Map")

    st.write(
        f"Showing **{len(filtered_df):,}** earthquakes "
        "based on the selected filters."
    )

    map_df = filtered_df.dropna(
        subset=[
            "latitude",
            "longitude",
            "mag"
        ]
    ).copy()

    if len(map_df) > 50000:

        st.warning(
            "More than 50,000 earthquakes match the filters. "
            "The map displays the first 50,000 records for performance."
        )

        map_df = map_df.head(50000)

    fig = px.scatter_geo(
        map_df,
        lat="latitude",
        lon="longitude",
        color="mag",
        size="mag",
        hover_name="place",
        hover_data=[
            "time",
            "depth_km",
            "mag",
            "country",
            "region"
        ],
        projection="natural earth",
        title="Global Earthquake Distribution"
    )

    fig.update_layout(
        height=650
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DETAILED DATA
# ============================================================

elif page == "Detailed Data":

    st.header("📋 Detailed Earthquake Data")

    st.write(
        f"Showing **{len(filtered_df):,}** filtered records."
    )

    search_text = st.text_input(
        "🔍 Search by place or country"
    )

    display_df = filtered_df.copy()

    if search_text:

        search_text = search_text.lower()

        display_df = display_df[
            display_df[
                "place"
            ]
            .fillna("")
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
            |
            display_df[
                "country"
            ]
            .fillna("")
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
        ]

    st.dataframe(
        display_df,
        use_container_width=True,
        height=600
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Global Seismic Trends | Data-Driven Earthquake Insights | "
    "USGS Earthquake Data | Built with Python, Pandas, Streamlit and Plotly"
)