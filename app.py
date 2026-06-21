import streamlit as st
import pandas as pd
import numpy as np
import datetime
from filters import load_data, filter_businesses, filter_time_series, MAJOR_CATEGORIES
import charts

# Page configurations
st.set_page_config(
    page_title="Yelp Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling for custom cards, margins, and dashboard look
st.markdown("""
    <style>
        /* Modern font styling and layout */
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }
        h1 {
            color: #1f77b4;
            font-weight: 800;
            margin-bottom: 0.1rem !important;
        }
        .subtitle {
            color: #666666;
            font-size: 1rem;
            margin-bottom: 1.2rem;
        }
        
        /* Metric card in Sidebar styling */
        .kpi-card {
            background-color: #f8f9fa;
            border-left: 5px solid #1f77b4;
            padding: 10px 15px;
            border-radius: 6px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .kpi-label {
            font-size: 0.8rem;
            font-weight: 600;
            color: #495057;
            text-transform: uppercase;
        }
        .kpi-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1f77b4;
            margin-top: 2px;
        }
        
        /* Tab labels styling */
        button[data-baseweb="tab"] {
            font-size: 1.1rem !important;
            font-weight: bold !important;
            color: #495057 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #1f77b4 !important;
            border-bottom-color: #1f77b4 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 1. Load Datasets
df_biz, df_ts = load_data()

# Initialize session states for filters if not present
if "selected_states" not in st.session_state:
    st.session_state.selected_states = []
if "selected_cities" not in st.session_state:
    st.session_state.selected_cities = []
if "selected_categories" not in st.session_state:
    st.session_state.selected_categories = []
if "selected_stars" not in st.session_state:
    st.session_state.selected_stars = (1.0, 5.0)
if "selected_reviews" not in st.session_state:
    st.session_state.selected_reviews = (
        int(df_biz["review_count"].min()),
        int(df_biz["review_count"].max())
    )
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# Date slider states
min_date = df_ts["year_month"].min().to_pydatetime()
max_date = df_ts["year_month"].max().to_pydatetime()
if "selected_dates" not in st.session_state:
    st.session_state.selected_dates = (min_date, max_date)

# Reset Function
def reset_filters():
    st.session_state.selected_states = []
    st.session_state.selected_cities = []
    st.session_state.selected_categories = []
    st.session_state.selected_stars = (1.0, 5.0)
    st.session_state.selected_reviews = (
        int(df_biz["review_count"].min()),
        int(df_biz["review_count"].max())
    )
    st.session_state.search_query = ""
    st.session_state.selected_dates = (min_date, max_date)

# 2. Main Panel Title
st.markdown("<h1>Yelp Business Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A modular tabbed grid BI interface analyzing 150,000+ businesses and millions of interactions.</p>", unsafe_allow_html=True)

# 3. Horizontal Toolbar (Top Panel Filters)
with st.container(border=True):
    st.markdown("##### 🛠️ Interactive Filter Controls")
    
    # Filter Row 1: Selectors
    col_state, col_city, col_cat = st.columns(3)
    
    with col_state:
        all_states = sorted(df_biz["state"].dropna().unique().tolist())
        states = st.multiselect(
            "Filter by States",
            options=all_states,
            key="selected_states",
            help="If empty, all states are shown."
        )
        
    with col_city:
        if states:
            available_cities = sorted(df_biz[df_biz["state"].isin(states)]["city"].dropna().unique().tolist())
        else:
            available_cities = sorted(df_biz["city"].dropna().unique().tolist())
            
        cities = st.multiselect(
            "Filter by Cities",
            options=available_cities,
            key="selected_cities",
            help="Only cities matching selected states will be shown."
        )
        
    with col_cat:
        categories = st.multiselect(
            "Filter by Primary Category",
            options=MAJOR_CATEGORIES + ["Other"],
            key="selected_categories",
            help="Filter by primary industry classification."
        )
        
    # Filter Row 2: Sliders & Search
    col_stars, col_reviews, col_dates, col_search = st.columns(4)
    
    with col_stars:
        stars_range = st.slider(
            "Stars Rating Range",
            min_value=1.0,
            max_value=5.0,
            step=0.5,
            key="selected_stars"
        )
        
    with col_reviews:
        review_max_val = int(df_biz["review_count"].max())
        review_count_range = st.slider(
            "Review Count Range",
            min_value=0,
            max_value=review_max_val,
            step=10,
            key="selected_reviews"
        )
        
    with col_dates:
        date_range = st.slider(
            "Timeline Date Range",
            min_value=min_date,
            max_value=max_date,
            key="selected_dates",
            format="YYYY-MM"
        )
        
    with col_search:
        search_query = st.text_input(
            "Search Business Name/Keywords",
            key="search_query"
        )
        
    # Reset button inside the toolbar container
    st.button(
        "🔄 Reset Filters to Default",
        on_click=reset_filters,
        help="Clear all input fields and return to defaults."
    )

# 4. Filter Datasets dynamically based on inputs
filtered_biz = filter_businesses(
    df_biz,
    states=states,
    cities=cities,
    categories=categories,
    stars_range=stars_range,
    review_count_range=review_count_range,
    search_query=search_query
)

filtered_ts = filter_time_series(
    df_ts,
    states=states,
    cities=cities,
    categories=categories,
    date_range=date_range
)

# 5. Sidebar: Metrics Command Center (KPI Cards)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Yelp_Logo.svg/1024px-Yelp_Logo.svg.png", width=110)
st.sidebar.markdown("### 📊 Metrics Console")

total_records = filtered_biz.shape[0]
avg_stars = filtered_biz["stars"].mean() if total_records > 0 else 0.0
total_reviews = filtered_biz["review_count"].sum() if total_records > 0 else 0
total_checkins = filtered_biz["checkin_count"].sum() if total_records > 0 else 0
total_tips = filtered_biz["tip_count"].sum() if total_records > 0 else 0

# Vertical list of styled KPI cards in Sidebar
st.sidebar.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Businesses</div>
        <div class="kpi-value">{total_records:,}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Average Star Rating</div>
        <div class="kpi-value">{avg_stars:.2f} ⭐</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Total Reviews</div>
        <div class="kpi-value">{total_reviews:,}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Total Check-ins</div>
        <div class="kpi-value">{total_checkins:,}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Total Tips Left</div>
        <div class="kpi-value">{total_tips:,}</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("All statistics dynamically adjust with current filters.")

# 6. Main Panel: Tabbed Grid Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Geospatial & Engagement Timeline",
    "⭐ Ratings & Popularity Profiles",
    "🏢 Regional & Demographic Breakdowns",
    "🧠 Advanced Insights & Growth"
])

# Tab 1: Geospatial & Engagement Timeline
with tab1:
    col_sec1_left, col_sec1_right = st.columns([1.2, 1])
    
    with col_sec1_left:
        with st.container(border=True):
            st.markdown("**Interactive Business Mapping (Geospatial Map)**")
            fig_map = charts.plot_bubble_chart(filtered_biz)
            st.pyplot(fig_map, width='stretch')
            st.caption("Coordinates are plotted within North America (size represents review counts, color represents average ratings).")
            
    with col_sec1_right:
        with st.container(border=True):
            st.markdown("**Monthly User Interactions over Time (Line Chart)**")
            fig_line = charts.plot_line_chart(filtered_ts)
            st.pyplot(fig_line, width='stretch')
            st.caption("Dual axis timelines indicating monthly check-in counts and tip counts.")

# Tab 2: Ratings & Popularity Profiles
with tab2:
    col_sec2_left, col_sec2_mid, col_sec2_right = st.columns([1, 1, 0.8])
    
    with col_sec2_left:
        with st.container(border=True):
            st.markdown("**Distribution of Ratings (Histogram)**")
            fig_hist = charts.plot_histogram(filtered_biz)
            st.pyplot(fig_hist, width='stretch')
            st.caption("Histogram showing the distribution of Yelp stars ratings in 0.5 bins.")
            
    with col_sec2_mid:
        with st.container(border=True):
            st.markdown("**Review Count vs. Star Ratings (Scatter Plot)**")
            fig_scatter = charts.plot_scatter_plot(filtered_biz)
            st.pyplot(fig_scatter, width='stretch')
            st.caption("Log-scale scatter plot showing correlation of popularity and rating averages.")
            
    with col_sec2_right:
        with st.container(border=True):
            st.markdown("**Business Status (Pie Chart)**")
            fig_pie = charts.plot_pie_chart(filtered_biz)
            st.pyplot(fig_pie, width='stretch')
            st.caption("Proportion of active open businesses compared to permanently closed ones.")

# Tab 3: Regional & Demographic Breakdowns
with tab3:
    col_sec3_left, col_sec3_mid, col_sec3_right = st.columns([1, 1, 1])
    
    with col_sec3_left:
        with st.container(border=True):
            st.markdown("**Business Counts by State (Count Plot)**")
            fig_count = charts.plot_count_plot(filtered_biz)
            st.pyplot(fig_count, width='stretch')
            st.caption("Bar counts indicating which states have the highest business densities.")
            
    with col_sec3_mid:
        with st.container(border=True):
            st.markdown("**Top 10 Cities by Business Count (Bar Chart)**")
            fig_bar = charts.plot_bar_chart(filtered_biz)
            st.pyplot(fig_bar, width='stretch')
            st.caption("Horizontal bar comparison of top 10 metropolitan hubs in dataset.")
            
    with col_sec3_right:
        with st.container(border=True):
            st.markdown("**Ratings Density by State (Violin Plot)**")
            fig_violin = charts.plot_violin_plot(filtered_biz)
            st.pyplot(fig_violin, width='stretch')
            st.caption("Violin plot mapping density shape and quartiles of ratings for top 5 states.")

# Tab 4: Advanced Insights & Growth
with tab4:
    col_sec4_left, col_sec4_mid, col_sec4_right = st.columns([1.1, 1, 1])
    
    with col_sec4_left:
        with st.container(border=True):
            st.markdown("**Cumulative Growth over Time (Area Chart)**")
            fig_area = charts.plot_area_chart(filtered_ts)
            st.pyplot(fig_area, width='stretch')
            st.caption("Area chart mapping total cumulative check-in and tip growth timeline.")
            
    with col_sec4_mid:
        with st.container(border=True):
            st.markdown("**Spread of Review Counts by Rating (Box Plot)**")
            fig_box = charts.plot_box_plot(filtered_biz)
            st.pyplot(fig_box, width='stretch')
            st.caption("Log-scale box-whisker plot revealing review count distribution outliers.")
            
    with col_sec4_right:
        with st.container(border=True):
            st.markdown("**Numerical Correlation Heatmap (Heatmap)**")
            fig_heat = charts.plot_heatmap(filtered_biz)
            st.pyplot(fig_heat, width='stretch')
            st.caption("Correlation coefficients between coordinates, ratings, check-ins, and tips.")
