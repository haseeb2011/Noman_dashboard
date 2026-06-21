import os
import json
import pandas as pd
import streamlit as st
import time

MAJOR_CATEGORIES = [
    "Restaurants", "Food", "Shopping", "Home Services", "Beauty & Spas",
    "Nightlife", "Health & Medical", "Local Services", "Bars", "Automotive",
    "Event Planning & Services"
]

def get_primary_category(cats):
    if not cats:
        return "Other"
    for cat in cats:
        if cat in MAJOR_CATEGORIES:
            return cat
    return cats[0] if len(cats) > 0 else "Other"

def run_preprocessing(data_dir):
    """
    Fallback preprocessing pipeline. Loads raw Yelp JSON datasets,
    cleans and aggregates them, and writes the lightweight CSV files.
    """
    biz_path = os.path.join(data_dir, "yelp_academic_dataset_business.json")
    checkin_path = os.path.join(data_dir, "yelp_academic_dataset_checkin.json")
    tip_path = os.path.join(data_dir, "yelp_academic_dataset_tip.json")
    
    if not os.path.exists(biz_path):
        raise FileNotFoundError(f"Raw business dataset not found at: {biz_path}")
        
    print("Preprocessing raw datasets (this runs once)...")
    
    # 1. Load Business Dataset
    biz_dict = {}
    with open(biz_path, "r", encoding="utf-8") as f:
        for line in f:
            bj = json.loads(line)
            biz_id = bj["business_id"]
            cats = [c.strip() for c in bj["categories"].split(",")] if bj["categories"] else []
            primary_cat = get_primary_category(cats)
            
            biz_dict[biz_id] = {
                "business_id": biz_id,
                "name": bj["name"],
                "address": bj["address"],
                "city": bj["city"],
                "state": bj["state"],
                "stars": float(bj["stars"]),
                "review_count": int(bj["review_count"]),
                "is_open": int(bj["is_open"]),
                "latitude": float(bj["latitude"]),
                "longitude": float(bj["longitude"]),
                "categories": ", ".join(cats),
                "primary_category": primary_cat,
                "checkin_count": 0,
                "tip_count": 0
            }

    # 2. Process Checkins
    checkin_rows = []
    if os.path.exists(checkin_path):
        with open(checkin_path, "r", encoding="utf-8") as f:
            for line in f:
                cj = json.loads(line)
                biz_id = cj["business_id"]
                if biz_id in biz_dict:
                    dates = cj["date"].split(", ")
                    biz_dict[biz_id]["checkin_count"] = len(dates)
                    
                    state = biz_dict[biz_id]["state"]
                    city = biz_dict[biz_id]["city"]
                    cat = biz_dict[biz_id]["primary_category"]
                    
                    for dt_str in dates:
                        ym = dt_str[:7]
                        checkin_rows.append((state, city, cat, ym))
                        
    # Aggregate checkins
    df_checkin_raw = pd.DataFrame(checkin_rows, columns=["state", "city", "category", "year_month"])
    df_checkin_agg = df_checkin_raw.groupby(["state", "city", "category", "year_month"]).size().reset_index(name="checkins")
    
    # 3. Process Tips
    tip_rows = []
    if os.path.exists(tip_path):
        with open(tip_path, "r", encoding="utf-8") as f:
            for line in f:
                tj = json.loads(line)
                biz_id = tj["business_id"]
                if biz_id in biz_dict:
                    biz_dict[biz_id]["tip_count"] += 1
                    
                    state = biz_dict[biz_id]["state"]
                    city = biz_dict[biz_id]["city"]
                    cat = biz_dict[biz_id]["primary_category"]
                    ym = tj["date"][:7]
                    tip_rows.append((state, city, cat, ym))
                    
    # Aggregate tips
    df_tip_raw = pd.DataFrame(tip_rows, columns=["state", "city", "category", "year_month"])
    df_tip_agg = df_tip_raw.groupby(["state", "city", "category", "year_month"]).size().reset_index(name="tips")
    
    # Merge Checkins and Tips Time Series
    df_ts = pd.merge(df_checkin_agg, df_tip_agg, on=["state", "city", "category", "year_month"], how="outer").fillna(0)
    df_ts["checkins"] = df_ts["checkins"].astype(int)
    df_ts["tips"] = df_ts["tips"].astype(int)
    
    # Save Dataframes
    df_biz_all = pd.DataFrame(biz_dict.values())
    
    cleaned_biz_path = os.path.join(data_dir, "cleaned_businesses.csv")
    cleaned_ts_path = os.path.join(data_dir, "cleaned_time_series.csv")
    
    df_biz_all.to_csv(cleaned_biz_path, index=False)
    df_ts.to_csv(cleaned_ts_path, index=False)
    print("Preprocessing completed and files saved!")


@st.cache_data(show_spinner="Loading Yelp datasets...")
def load_data(data_dir=r"c:\Users\HP\OneDrive\Desktop\Noman`s Project\data"):
    """
    Loads preprocessed datasets. If they do not exist, runs the
    preprocessing pipeline first.
    """
    cleaned_biz_path = os.path.join(data_dir, "cleaned_businesses.csv")
    cleaned_ts_path = os.path.join(data_dir, "cleaned_time_series.csv")
    
    if not os.path.exists(cleaned_biz_path) or not os.path.exists(cleaned_ts_path):
        run_preprocessing(data_dir)
        
    df_biz = pd.read_csv(cleaned_biz_path)
    df_ts = pd.read_csv(cleaned_ts_path)
    
    # Ensure datatypes
    df_biz["categories"] = df_biz["categories"].fillna("")
    df_biz["primary_category"] = df_biz["primary_category"].fillna("Other")
    df_biz["city"] = df_biz["city"].fillna("Unknown")
    df_biz["state"] = df_biz["state"].fillna("Unknown")
    
    df_ts["city"] = df_ts["city"].fillna("Unknown")
    df_ts["state"] = df_ts["state"].fillna("Unknown")
    df_ts["category"] = df_ts["category"].fillna("Other")
    df_ts["year_month"] = pd.to_datetime(df_ts["year_month"] + "-01")
    
    return df_biz, df_ts


def filter_businesses(df, states=None, cities=None, categories=None, stars_range=None, review_count_range=None, search_query=None):
    """
    Filters the business dataset based on widget parameters.
    """
    filtered_df = df.copy()
    
    if states:
        filtered_df = filtered_df[filtered_df["state"].isin(states)]
        
    if cities:
        filtered_df = filtered_df[filtered_df["city"].isin(cities)]
        
    if categories:
        filtered_df = filtered_df[filtered_df["primary_category"].isin(categories)]
        
    if stars_range:
        filtered_df = filtered_df[(filtered_df["stars"] >= stars_range[0]) & (filtered_df["stars"] <= stars_range[1])]
        
    if review_count_range:
        filtered_df = filtered_df[(filtered_df["review_count"] >= review_count_range[0]) & (filtered_df["review_count"] <= review_count_range[1])]
        
    if search_query:
        query = search_query.strip().lower()
        if query:
            filtered_df = filtered_df[
                filtered_df["name"].str.lower().str.contains(query, na=False) |
                filtered_df["categories"].str.lower().str.contains(query, na=False)
            ]
            
    return filtered_df


def filter_time_series(df_ts, states=None, cities=None, categories=None, date_range=None):
    """
    Filters the time-series dataset based on state, city, category, and date range.
    """
    filtered_df = df_ts.copy()
    
    if states:
        filtered_df = filtered_df[filtered_df["state"].isin(states)]
        
    if cities:
        filtered_df = filtered_df[filtered_df["city"].isin(cities)]
        
    if categories:
        filtered_df = filtered_df[filtered_df["category"].isin(categories)]
        
    if date_range:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_df = filtered_df[(filtered_df["year_month"] >= start_date) & (filtered_df["year_month"] <= end_date)]
        
    return filtered_df
