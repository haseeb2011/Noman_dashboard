# Yelp Business Intelligence Dashboard

A professional-grade, interactive data visualization dashboard designed to analyze and profile the Yelp Academic Dataset (containing over 150,000 businesses, 13 million check-ins, and 900,000 tips).

The dashboard is built using **Python**, **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn**.

---

## 📁 Project Folder Structure

```text
/Noman's Project/
├── data/
│   ├── yelp_academic_dataset_business.json (Raw)
│   ├── yelp_academic_dataset_checkin.json  (Raw)
│   ├── yelp_academic_dataset_tip.json      (Raw)
│   ├── cleaned_businesses.csv              (Preprocessed - Consolidated metadata)
│   └── cleaned_time_series.csv             (Preprocessed - Aggregated temporal metrics)
├── notebooks/
│   └── analysis.ipynb                      (Exploratory Data Analysis)
├── app.py                                  (Main Streamlit dashboard entry point)
├── charts.py                               (Matplotlib & Seaborn plotting functions)
├── filters.py                              (Data loading, caching, and filtering logic)
├── requirements.txt                        (Required Python dependencies)
└── README.md                               (Project documentation & Insights)
```

---

## ⚡ Features & Visualizations

The dashboard contains **11 chart types** and **6 interactive filters** connected dynamically:

### Interactive Filters (Sidebar):
1. **State Selector:** Multi-select to filter by one or more States.
2. **City Selector:** Dynamically updated multi-select based on the selected states.
3. **Category Selector:** Select one or more primary industries (e.g. Restaurants, Food, Shopping).
4. **Stars Rating Slider:** Range selector from 1.0 to 5.0 stars.
5. **Review Count Slider:** Filter by business popularity.
6. **Date Range Slider:** Filter temporal check-in and tip records by month.
7. **Name Search:** Text input to filter businesses by name or keyword.
8. **Reset Button:** Instantly clears all filters back to defaults.

### KPI Summary Cards (Top Panel):
- **Total Businesses** (Matching active filters)
- **Average Rating** (Out of 5 stars)
- **Total Review Count** (Popularity aggregate)
- **Total Check-ins** (Visit count aggregate)
- **Total Tips Left** (Feedback aggregate)

### Visualization Tabs:
- **📍 Geospatial & Business Distribution:**
  1. *Geospatial Map (Bubble Chart):* Longitude vs. Latitude (Size: Review Count | Color: Stars).
  2. *Business Count by State (Count Plot):* Vertical count bar chart of top 10 states.
  3. *Ratings Density across States (Violin Plot):* Shows distribution shape and median ratings.
- **⭐ Review & Rating Profile:**
  4. *Rating Frequency (Histogram):* Distribution profile of ratings in 0.5-star bins.
  5. *Status Ratio (Pie Chart):* Proportional distribution of Open vs. Closed businesses.
  6. *Rating Popularity (Scatter Plot):* Jittered stars vs. review count with trendline.
  7. *Spread of Reviews (Box Plot):* Whisker/median spread of reviews across rating stars.
  8. *Feature Correlation (Heatmap):* Correlation coefficients matrix between numerical attributes.
- **📈 Temporal Activity Trends:**
  9. *Engagement Trends (Line Chart):* Double-axis timeline tracking monthly check-ins and tips.
  10. *Cumulative Growth (Area Chart):* Stacked area plotting cumulative user engagements over time.

---

## 🚀 Setup & Run Instructions

### 1. Install Dependencies
Ensure you have Python 3.x installed. Run the following command in your terminal/command prompt to install all required packages:
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
Run the following command to start the local Streamlit web server:
```bash
streamlit run app.py
```
This will automatically launch the dashboard in your default web browser (usually at `http://localhost:8501`).

---

## 📊 Key Analytical Insights

1. **Ratings Skewness:** Ratings are highly skewed towards positive scores, peaking at **4.0 stars**. This indicates a general positive customer bias on Yelp or highlights that lower-rated businesses fail and close sooner.
2. **Open vs. Closed Status:** Approximately **79.6%** of all businesses in the dataset are currently active (Open), while **20.4%** are inactive (Closed).
3. **Geographical Densities:** Pennsylvania (PA) and Florida (FL) are the highest represented states in the dataset, with Philadelphia, Tucson, and Tampa being the most dense cities.
4. **Dominant Categories:** **Restaurants**, **Food**, and **Shopping** represent the overwhelming majority of businesses. They also account for the highest volume of user check-ins and tips.
5. **Popularity Outliers:** Popularity (Review Count) has a long-tail distribution. A few businesses have over 5,000 reviews, while the median business has only 15 reviews. The box plot shows that businesses with **3.5 to 4.5 stars** tend to accumulate the highest median review counts.
6. **Correlation Insights:** Latitude and Longitude have zero correlation with rating stars, confirming that location coordinates alone do not influence business quality. However, a strong positive correlation is observed between check-in counts and tip counts, suggesting that foot traffic is directly proportional to active tip writing.
