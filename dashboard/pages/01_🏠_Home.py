# -*- coding: utf-8 -*-
"""
Home Page - Dashboard Principal
Muestra overview general y quick stats
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Agregar parent directory al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Home - Dashboard", page_icon="🏠", layout="wide")

st.title("🏠 Dashboard Home")
st.markdown("### Overview of your social media bot")

# Sidebar con info adicional
with st.sidebar:
    st.header("Quick Info")

    st.markdown("**Bot Status**")
    # TODO: Obtener status real del bot
    st.success("🟢 Active")

    st.markdown("**Last Sync**")
    st.info("2 minutes ago")

    st.markdown("**Uptime**")
    st.metric("", "2h 34m")

st.markdown("---")

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total Posts",
        value="156",
        delta="+12 today"
    )

with col2:
    st.metric(
        label="💚 Engagement",
        value="24.5K",
        delta="+18%"
    )

with col3:
    st.metric(
        label="✅ Success Rate",
        value="98.7%",
        delta="+2.3%"
    )

with col4:
    st.metric(
        label="⏱️ Avg Time",
        value="2.3 min",
        delta="-0.5 min"
    )

st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["📈 Trends", "🕒 Activity Log"])

with tab1:
    st.subheader("Posts Trend (Last 7 Days)")

    # Placeholder para gráfica
    st.info("📊 Full analytics available in the **Analytics** page")

    # Stats rápidas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**This Week**")
        st.markdown("🐦 Twitter: 23 posts")
        st.markdown("📷 Instagram: 25 posts")

    with col2:
        st.markdown("**Best Day**")
        st.markdown("📅 Monday - 8 posts")
        st.markdown("⏰ Best hour: 3 PM")

    with col3:
        st.markdown("**Top Post**")
        st.markdown("💚 52K likes")
        st.markdown("🔄 1.2K retweets")

with tab2:
    st.subheader("Recent Activity")

    # Activity log (dummy data)
    activities = [
        {"time": "2 min ago", "type": "success", "message": "Post published on Twitter (ID: xyz123)"},
        {"time": "15 min ago", "type": "info", "message": "New post detected on Instagram"},
        {"time": "15 min ago", "type": "success", "message": "Image downloaded successfully"},
        {"time": "30 min ago", "type": "success", "message": "Post published on Twitter (ID: abc456)"},
        {"time": "45 min ago", "type": "info", "message": "Bot check completed - 0 new posts"},
        {"time": "1 hour ago", "type": "info", "message": "Bot started"},
        {"time": "2 hours ago", "type": "success", "message": "Post published on Twitter (ID: def789)"},
    ]

    for activity in activities:
        icon = "✅" if activity["type"] == "success" else "ℹ️" if activity["type"] == "info" else "⚠️"
        color = "green" if activity["type"] == "success" else "blue" if activity["type"] == "info" else "orange"

        st.markdown(f":{color}[{icon}] **{activity['time']}** - {activity['message']}")

st.markdown("---")

# Cards informativos
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown("### 🤖 Bot Status")
        st.success("Running")
        st.caption("PID: 12345")
        st.caption("Uptime: 2h 34m")

        if st.button("⏸️ Pause Bot", key="pause"):
            st.warning("Bot paused")

with col2:
    with st.container():
        st.markdown("### 📱 Connected Platforms")
        st.markdown("✅ Instagram - Active")
        st.markdown("✅ Twitter - Active")
        st.markdown("⏳ Facebook - Coming Soon")

with col3:
    with st.container():
        st.markdown("### ⚙️ Quick Settings")
        st.markdown(f"Check interval: **15 min**")
        st.markdown(f"Max posts: **5**")

        if st.button("Edit Settings", key="settings"):
            st.info("Navigate to Settings page")

# Footer
st.markdown("---")
st.caption("💡 Tip: Use the sidebar to navigate to other pages like Analytics, Bot Control, and Posts Gallery")
