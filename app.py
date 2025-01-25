import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Golfinho Network Monitor", layout="wide")
st.title("📡 Real Time Network Monitoring")

API_URL = #DEPLOYED API URL

def get_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException:
        st.error("Network error: Unable to reach the API.")
    except ValueError:
        st.error("Error: Received invalid data format.")
    return pd.DataFrame()

def show_metrics(df):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latency (ms)", df["latency"].iloc[-1])
    col2.metric("Download Speed (Mbps)", df["download_speed"].iloc[-1])
    col3.metric("Upload Speed (Mbps)", df["upload_speed"].iloc[-1])
    col4.metric("Packet Loss (%)", df["packet_loss"].iloc[-1])

def show_graphics(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig_latency = px.line(df, x="timestamp", y="latency", title="📊 Latency (ms)", markers=True)
    fig_latency.update_layout(yaxis_title="Latency (ms)", xaxis_title="Time", template="plotly_dark")

    fig_speed = px.line(df, x="timestamp", y=["download_speed", "upload_speed"], 
                        title="🚀 Internet Speed (Mbps)", markers=True)
    fig_speed.update_layout(yaxis_title="Speed (Mbps)", xaxis_title="Time", template="plotly_dark")

    fig_loss = px.line(df, x="timestamp", y="packet_loss", title="🔻 Packet Loss (%)", markers=True)
    fig_loss.update_layout(yaxis_title="Packet Loss (%)", xaxis_title="Time", template="plotly_dark")

    st.plotly_chart(fig_latency, use_container_width=True)
    st.plotly_chart(fig_speed, use_container_width=True)
    st.plotly_chart(fig_loss, use_container_width=True)

if st.sidebar.button("Refresh Data"):
    df = get_data()
    if not df.empty and "latency" in df.columns:
        show_metrics(df)
        show_graphics(df)
    else:
        st.warning("Data could not be obtained or is incomplete.")
else:
    st.info("Press 'Refresh Data' to get the latest information.")

# Optional auto-refresh every 30 seconds
if st.sidebar.checkbox("Auto-refresh every 30 seconds", value=False):
    st.experimental_rerun()

