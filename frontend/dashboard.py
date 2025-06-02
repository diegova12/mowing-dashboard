# frontend/dashboard.py

import os
from datetime import datetime, timedelta

import json
import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly
from streamlit_calendar_semver import calendar as st_calendar

# Page config and styling
st.set_page_config(
    page_title="Landscaping Dashboard",
    layout="wide"
)
st.markdown(
    """
    <style>
      /* hide header & footer */
      header, footer { visibility: hidden; }
      /* tighten top/bottom padding */
      .css-18e3th9 { padding-top: 1rem; padding-bottom: 1rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# Job fetching and processing
API_URL = "http://127.0.0.1:8000/jobs/"
jobs = requests.get(API_URL).json()
df = pd.json_normalize(jobs)
df["scheduled"] = pd.to_datetime(df["scheduled"])
df["end_date"]  = df["scheduled"] + pd.Timedelta(days=1)
df["month"]     = df["scheduled"].dt.to_period("M").dt.to_timestamp()

# Revenue aggregation
rev = (
    df.groupby("month")
      .agg(total_revenue=("price","sum"))
      .reset_index()
)

# Streamlit app title and metrics
st.title("Landscaping Dashboard")
today = pd.Timestamp.today().normalize()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Jobs Today", df[df["scheduled"] == today].shape[0])
c2.metric("Revenue Today", f"${df[df['scheduled']==today]['price'].sum():,.2f}")
c3.metric("Revenue This Month",
          f"${df[df['scheduled'].dt.to_period('M')==today.to_period('M')]['price'].sum():,.2f}")
c4.metric("Unique Clients", df["client_id"].nunique())

# Weather Sidebar
with st.sidebar.expander("🌦 Weather Alerts", expanded=True):
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    lat, lon = df.iloc[0][["latitude","longitude"]]
    now = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
    ).json()
    desc = now["weather"][0]["description"].title()
    temp = now["main"]["temp"]
    st.markdown(f"**Now:** {desc}, {temp:.1f}°F")

    fc = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
    ).json()
    tomorrow = (datetime.utcnow() + timedelta(days=1)).date()
    rain   = any(
        e.get("rain",{}).get("3h",0)>0
        for e in fc["list"]
        if datetime.utcfromtimestamp(e["dt"]).date()==tomorrow
    )
    freeze = any(
        e["main"]["temp"]<=32
        for e in fc["list"]
        if datetime.utcfromtimestamp(e["dt"]).date()==tomorrow
    )

    if rain:   st.warning(f"🌧 Rain tomorrow ({tomorrow})")
    else:      st.success(f"☀️ No rain tomorrow ({tomorrow})")
    if freeze: st.error(  f"❄️ Freeze risk tomorrow ({tomorrow})")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📅 Calendar",
    "🗺️ Map View",
    "💰 Financials",
    "📈 Forecast"
])

# Calendar Tab
with tab1:
    st.header("Job Schedule")

    orig_events = [
        {
            "id":    str(int(r.id)),
            "title": r.service,
            "start": r.scheduled.strftime("%Y-%m-%d"),
            "end":   r.end_date.strftime("%Y-%m-%d"),
        }
        for _, r in df.iterrows()
    ]

    options = {
        "initialView":   "dayGridMonth",
        "editable":      True,
        "headerToolbar": {"left":"prev,next today","center":"title","right":""},
    }
    raw = st_calendar(events=orig_events, options=options, key="job_calendar")

    updated_events = []
    if raw:
        candidates = raw if isinstance(raw, list) else [raw]
        for item in candidates:
            if isinstance(item, str):
                try:
                    obj = json.loads(item)
                except json.JSONDecodeError:
                    continue
            else:
                obj = item

            if isinstance(obj, dict):
                updated_events.append(obj)
            elif isinstance(obj, list):
                updated_events.extend([sub for sub in obj if isinstance(sub, dict)])

    updated_events = [e for e in updated_events if e.get("id")]

    if updated_events and updated_events != orig_events:
        for new_evt in updated_events:
            evt_id = new_evt.get("id")
            if not evt_id:
                continue

            old_evt = next((e for e in orig_events if e.get("id") == evt_id), None)
            if not old_evt:
                continue

            old_start = old_evt.get("start", "")
            new_start = new_evt.get("start", "")[:10]  
            if new_start and new_start != old_start:
                res = requests.patch(
                    f"http://127.0.0.1:8000/jobs/{evt_id}/reschedule",
                    json={"scheduled": new_start},
                )
                if res.ok:
                    st.success(f"Job {evt_id} moved to {new_start}")
                else:
                    st.error(f"Failed to move Job {evt_id}")

        st.experimental_rerun()



# Map Tab
with tab2:
    st.header("Job Locations")
    st.map(df.rename(columns={"latitude":"lat","longitude":"lon"})[["lat","lon"]])
    if st.button("Optimize Today's Route"):
        td = df[df["scheduled"]==today]
        coords = td[["latitude","longitude"]].to_dict("records")
        route = requests.post("http://127.0.0.1:8000/optimize/", json={"coords":coords}).json()["route"]
        rd = td.iloc[route].reset_index(drop=True)
        fig = go.Figure(go.Scattermapbox(
            lat=rd.latitude, lon=rd.longitude,
            mode="lines+markers",
            marker=go.scattermapbox.Marker(size=8,color="red"),
            line=go.scattermapbox.Line(width=3,color="red"),
            text=rd.service
        ))
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_center={"lat":rd.latitude.mean(),"lon":rd.longitude.mean()},
            mapbox_zoom=12,
            template="plotly_dark",
            margin={"l":0,"r":0,"t":40,"b":0},
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# Financials
with tab3:
    st.header("Monthly Revenue by Service")
    rev_svc = (
        df.groupby(["month","service"])
          .price
          .sum()
          .reset_index(name="total_revenue")
    )
    rev_svc["month"] = rev_svc["month"].dt.to_period("M").dt.to_timestamp()
    fig = px.bar(
        rev_svc,
        x="month",
        y="total_revenue",
        color="service",
        labels={"total_revenue":"Revenue ($)","month":"Month"}
    )
    fig.update_xaxes(tickformat="%b %Y", dtick="M1", tickangle=-45)
    fig.update_layout(template="plotly_dark", margin={"l":40,"r":20,"t":50,"b":40})
    st.plotly_chart(fig, use_container_width=True)

# Prophet Forecast
with tab4:
    st.header("Revenue Forecast (Next 12 Months)")
    dfp = rev.rename(columns={"month":"ds","total_revenue":"y"})
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(dfp)
    future  = m.make_future_dataframe(periods=12, freq="M")
    forecast = m.predict(future)
    fig = plot_plotly(m, forecast)
    fig.update_layout(template="plotly_dark", margin={"l":40,"r":20,"t":50,"b":40})
    st.plotly_chart(fig, use_container_width=True)
