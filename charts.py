import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set consistent style parameters
plt.rcParams['figure.facecolor'] = '#ffffff'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['grid.color'] = '#e9ecef'
plt.rcParams['xtick.color'] = '#495057'
plt.rcParams['ytick.color'] = '#495057'
plt.rcParams['text.color'] = '#212529'
plt.rcParams['axes.labelcolor'] = '#212529'

PALETTE = {
    "primary": "#1f77b4",     # Slate Blue
    "secondary": "#2ca02c",   # Forest Green
    "accent": "#ff7f0e",      # Amber Orange
    "danger": "#d62728",      # Crimson Red
    "muted": "#7f7f7f",       # Cool Gray
    "highlight": "#9467bd",   # Amethyst Purple
    "light": "#e377c2"        # Soft Pink
}

# Diverging palette for correlation heatmaps
CORR_CMAP = sns.diverging_palette(220, 20, as_cmap=True)

def plot_pie_chart(df):
    """
    1. Pie Chart: Proportional distribution of business status (Open vs. Closed).
    """
    fig, ax = plt.subplots(figsize=(6, 5))
    status_counts = df["is_open"].value_counts()
    
    # Map labels
    labels = ["Open" if idx == 1 else "Closed" for idx in status_counts.index]
    colors = [PALETTE["primary"], PALETTE["danger"]]
    
    if len(status_counts) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        ax.axis('off')
        return fig
        
    wedges, texts, autotexts = ax.pie(
        status_counts, 
        labels=labels, 
        autopct='%1.1f%%',
        startangle=140, 
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2),
        pctdistance=0.75
    )
    
    # Styling text inside pie
    plt.setp(texts, size=10, weight="bold")
    plt.setp(autotexts, size=9, weight="bold", color="white")
    
    ax.set_title("Proportional Distribution of Business Status (Open vs. Closed)", fontsize=12, pad=15, weight="bold")
    return fig


def plot_histogram(df):
    """
    2. Histogram: Frequency distribution of business stars ratings.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if len(df) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return fig
        
    sns.histplot(
        data=df, 
        x="stars", 
        bins=np.arange(0.75, 5.75, 0.5), 
        kde=False, 
        color=PALETTE["primary"], 
        edgecolor="w", 
        linewidth=1.5,
        ax=ax
    )
    
    ax.set_xlabel("Star Rating", fontsize=10, labelpad=8)
    ax.set_ylabel("Count of Businesses", fontsize=10, labelpad=8)
    ax.set_title("Frequency Distribution of Business Star Ratings", fontsize=12, pad=15, weight="bold")
    ax.set_xticks(np.arange(1.0, 5.5, 0.5))
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    sns.despine(ax=ax, top=True, right=True)
    return fig


def plot_line_chart(df_ts):
    """
    3. Line Chart: Trends of monthly check-ins and tips over time.
    """
    fig, ax1 = plt.subplots(figsize=(9, 4.5))
    if len(df_ts) == 0:
        ax1.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        ax1.axis('off')
        return fig
        
    # Group by month and sum
    df_monthly = df_ts.groupby("year_month")[["checkins", "tips"]].sum().reset_index()
    
    color1 = PALETTE["primary"]
    ax1.plot(df_monthly["year_month"], df_monthly["checkins"], color=color1, linewidth=2, label="Check-ins")
    ax1.set_xlabel("Time (Timeline)", fontsize=10, labelpad=8)
    ax1.set_ylabel("Monthly Check-ins", color=color1, fontsize=10, labelpad=8)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Twin axis for Tips since counts are much lower
    ax2 = ax1.twinx()
    color2 = PALETTE["accent"]
    ax2.plot(df_monthly["year_month"], df_monthly["tips"], color=color2, linewidth=2, label="Tips", linestyle="--")
    ax2.set_ylabel("Monthly Tips", color=color2, fontsize=10, labelpad=8)
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Combined Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True, facecolor="white", edgecolor="none")
    
    ax1.set_title("Monthly Trends of User Engagement Over Time (Check-ins & Tips)", fontsize=12, pad=15, weight="bold")
    sns.despine(ax=ax1, top=True, right=False)
    sns.despine(ax=ax2, top=True, left=True, right=False)
    return fig


def plot_bar_chart(df):
    """
    4. Bar Chart: Top 10 cities by number of businesses.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if len(df) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return fig
        
    city_counts = df["city"].value_counts().head(10).reset_index()
    city_counts.columns = ["city", "count"]
    
    sns.barplot(
        data=city_counts, 
        y="city", 
        x="count", 
        hue="city",
        palette="Blues_r", 
        legend=False,
        ax=ax, 
        edgecolor="none"
    )
    
    ax.set_ylabel("City", fontsize=10, labelpad=8)
    ax.set_xlabel("Number of Businesses", fontsize=10, labelpad=8)
    ax.set_title("Top 10 Cities by Number of Businesses", fontsize=12, pad=15, weight="bold")
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    sns.despine(ax=ax, top=True, right=True)
    return fig


def plot_scatter_plot(df):
    """
    5. Scatter Plot: Relationship between review count and stars rating.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if len(df) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return fig
        
    # Sample data to avoid overlapping and slow render
    sample_df = df.sample(n=min(3000, len(df)), random_state=42)
    
    # Add a bit of jitter to stars (since they are discrete) to make scatter plot readable
    jitter_stars = sample_df["stars"] + np.random.normal(0, 0.08, size=len(sample_df))
    
    # Plot using review_count log scale to make relationship visible
    scatter = ax.scatter(
        jitter_stars, 
        sample_df["review_count"], 
        alpha=0.4, 
        c=sample_df["stars"], 
        cmap="coolwarm", 
        edgecolors="none", 
        s=15
    )
    
    ax.set_yscale('log')
    ax.set_xlabel("Star Rating (with Jitter)", fontsize=10, labelpad=8)
    ax.set_ylabel("Review Count (Log Scale)", fontsize=10, labelpad=8)
    ax.set_title("Relationship Between Review Count and Star Rating", fontsize=12, pad=15, weight="bold")
    ax.grid(True, which="both", linestyle='--', alpha=0.5)
    
    # Add a trendline using seaborn regression on log review counts
    sample_df["log_review"] = np.log10(sample_df["review_count"] + 1)
    sns.regplot(
        x="stars", 
        y="log_review", 
        data=sample_df, 
        scatter=False, 
        ax=ax, 
        color=PALETTE["danger"], 
        line_kws={"linewidth": 2, "label": "Log Review Count Trend"}
    )
    # Correct the twin/scale projection logic
    # Since we are drawing on a log scale axis, the regplot drawn directly on y might look weird if regplot operates on log scale.
    # Therefore, we just use the simple scatter and let regplot handle it by setting yscale log and plotting standard values
    plt.close(fig) # close old fig and redraw properly using seaborn regplot
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.regplot(
        x=jitter_stars,
        y=np.log10(sample_df["review_count"]),
        scatter_kws={"alpha": 0.4, "s": 15, "color": PALETTE["primary"]},
        line_kws={"color": PALETTE["danger"], "linewidth": 2, "label": "Log Trendline"},
        ax=ax
    )
    ax.set_xlabel("Star Rating (with jitter)", fontsize=10, labelpad=8)
    ax.set_ylabel("Log10(Review Count)", fontsize=10, labelpad=8)
    ax.set_title("Scatter Plot: Review Count vs. Star Rating (Log Scale)", fontsize=12, pad=15, weight="bold")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    sns.despine(ax=ax, top=True, right=True)
    return fig


def plot_box_plot(df):
    """
    6. Box Plot: Distribution of review counts across star ratings.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if len(df) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return fig
        
    sns.boxplot(
        data=df, 
        x="stars", 
        y="review_count", 
        hue="stars",
        palette="Spectral", 
        legend=False,
        ax=ax,
        fliersize=1, # reduce outlier dot size
        linewidth=1.2
    )
    
    ax.set_yscale('log')
    ax.set_xlabel("Star Rating", fontsize=10, labelpad=8)
    ax.set_ylabel("Review Count (Log Scale)", fontsize=10, labelpad=8)
    ax.set_title("Box Plot: Spread of Review Counts across Star Ratings", fontsize=12, pad=15, weight="bold")
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    sns.despine(ax=ax, top=True, right=True)
    return fig


def plot_heatmap(df):
    """
    7. Heatmap: Correlation matrix of business features.
    """
    fig, ax = plt.subplots(figsize=(7, 5.5))
    if len(df) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return fig
        
    corr_cols = ["stars", "review_count", "latitude", "longitude", "checkin_count", "tip_count"]
    # Check if columns exist
    existing_cols = [col for col in corr_cols if col in df.columns]
    
    corr_matrix = df[existing_cols].corr()
    
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt=".2f", 
        cmap=CORR_CMAP, 
        center=0,
        linewidths=1.5, 
        cbar_kws={"shrink": .8},
        ax=ax,
        square=True
    )
    
    ax.set_title("Correlation Heatmap of Numerical Features", fontsize=12, pad=15, weight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    return fig


def plot_area_chart(df_ts):
    """
    8. Area Chart: Cumulative check-ins and tips over time.
    """
    fig, ax = plt.subplots(figsize=(9, 4.5))
    if len(df_ts) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        ax.axis('off')
        return fig
        
    # Group by month and sum
    df_monthly = df_ts.groupby("year_month")[["checkins", "tips"]].sum().reset_index()
    
    # Calculate cumulative sums
    df_monthly["cum_checkins"] = df_monthly["checkins"].cumsum()
    df_monthly["cum_tips"] = df_monthly["tips"].cumsum()
    
    # Stack area chart
    ax.fill_between(df_monthly["year_month"], df_monthly["cum_checkins"], label="Cumulative Check-ins", color=PALETTE["primary"], alpha=0.6)
    ax.fill_between(df_monthly["year_month"], df_monthly["cum_tips"], label="Cumulative Tips", color=PALETTE["accent"], alpha=0.7)
    
    ax.set_xlabel("Time (Timeline)", fontsize=10, labelpad=8)
    ax.set_ylabel("Cumulative Volume", fontsize=10, labelpad=8)
    ax.set_title("Cumulative Engagement Volume Trends Over Time", fontsize=12, pad=15, weight="bold")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc="upper left")
    sns.despine(ax=ax, top=True, right=True)
    return fig


def plot_count_plot(df):
    """
    9. Count Plot: Count of businesses per state (Top 10 states).
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if len(df) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return fig
        
    state_order = df["state"].value_counts().head(10).index
    
    sns.countplot(
        data=df, 
        x="state", 
        order=state_order, 
        hue="state",
        palette="viridis", 
        legend=False,
        ax=ax,
        edgecolor="w",
        linewidth=1.2
    )
    
    ax.set_xlabel("State", fontsize=10, labelpad=8)
    ax.set_ylabel("Number of Businesses", fontsize=10, labelpad=8)
    ax.set_title("Business Count by State (Top 10 States)", fontsize=12, pad=15, weight="bold")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    sns.despine(ax=ax, top=True, right=True)
    return fig


def plot_violin_plot(df):
    """
    10. Violin Plot: Distribution of star ratings across top 5 states.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if len(df) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return fig
        
    # Get top 5 states by business count
    top_5_states = df["state"].value_counts().head(5).index
    df_top_states = df[df["state"].isin(top_5_states)]
    
    if len(df_top_states) == 0:
        ax.text(0.5, 0.5, "No Data Available for Top States", ha='center', va='center')
        return fig
        
    sns.violinplot(
        data=df_top_states, 
        x="state", 
        y="stars", 
        order=top_5_states, 
        hue="state",
        palette="muted", 
        legend=False,
        ax=ax,
        inner="quartile",
        linewidth=1.2
    )
    
    ax.set_xlabel("State", fontsize=10, labelpad=8)
    ax.set_ylabel("Star Rating", fontsize=10, labelpad=8)
    ax.set_title("Violin Plot: Density and Spread of Star Ratings Across Top 5 States", fontsize=12, pad=15, weight="bold")
    ax.set_yticks(np.arange(1.0, 5.5, 0.5))
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    sns.despine(ax=ax, top=True, right=True)
    return fig


def plot_bubble_chart(df):
    """
    11. (Bonus) Bubble Chart: Geospatial Scatter Map using Latitude and Longitude.
    Marker size represents review count, and color represents stars rating.
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    if len(df) == 0:
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center')
        return fig
        
    # Filter out invalid coordinates
    valid_coords = df[(df["latitude"].notnull()) & (df["longitude"].notnull())]
    # Filter coordinates to a typical range of North America to prevent outliers from squishing the scale
    valid_coords = valid_coords[
        (valid_coords["latitude"] > 24) & (valid_coords["latitude"] < 60) &
        (valid_coords["longitude"] > -130) & (valid_coords["longitude"] < -65)
    ]
    
    if len(valid_coords) == 0:
        # Fallback if filtered range is empty (e.g. data is in Europe or other places)
        valid_coords = df[(df["latitude"].notnull()) & (df["longitude"].notnull())]
        
    # Sample data to make it load fast and look clean
    sample_df = valid_coords.sample(n=min(5000, len(valid_coords)), random_state=42)
    
    # Scale marker size based on review count
    # Size logic: log2 scale + 2 to make sure minimum size is visible and max is bounded
    sizes = np.log2(sample_df["review_count"] + 1) * 6
    
    scatter = ax.scatter(
        sample_df["longitude"], 
        sample_df["latitude"], 
        s=sizes, 
        c=sample_df["stars"], 
        cmap="RdYlBu_r", 
        alpha=0.5, 
        edgecolors="none"
    )
    
    ax.set_xlabel("Longitude", fontsize=10, labelpad=8)
    ax.set_ylabel("Latitude", fontsize=10, labelpad=8)
    ax.set_title("Geospatial Business Map (Bubble size: Reviews | Color: Star Rating)", fontsize=12, pad=15, weight="bold")
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax, orientation="vertical", shrink=0.7, pad=0.03)
    cbar.set_label("Star Rating", fontsize=10, labelpad=8)
    
    # Remove grid to make it look like a map, but draw map boundary box
    ax.grid(True, linestyle='--', alpha=0.3)
    sns.despine(ax=ax, top=True, right=True)
    return fig
