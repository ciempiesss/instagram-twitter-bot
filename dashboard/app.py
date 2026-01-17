# -*- coding: utf-8 -*-
"""
Social Media Crossposting Dashboard
Entry point para el dashboard de Streamlit

Ejecutar con: streamlit run dashboard/app.py
"""
import streamlit as st
import sys
from pathlib import Path

# Agregar parent directory al path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configuración de la página
st.set_page_config(
    page_title="Social Media Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/ciempiesss/instagram-twitter-bot',
        'Report a bug': 'https://github.com/ciempiesss/instagram-twitter-bot/issues',
        'About': """
        # Social Media Crossposting Dashboard

        Automated bot to cross-post content between:
        - Instagram → Twitter
        - Instagram → Facebook (coming soon)

        Built with Streamlit + Plotly + SQLite
        """
    }
)

# CSS personalizado
st.markdown("""
<style>
    /* Tema general */
    .main {
        padding: 2rem;
    }

    /* Métricas más grandes */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
    }

    /* Cards */
    .stCard {
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }

    /* Botones */
    .stButton>button {
        border-radius: 5px;
        font-weight: 500;
    }

    /* Ocultar made with streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/4CAF50/FFFFFF?text=Social+Media+Bot", use_container_width=True)

    st.markdown("---")

    st.markdown("## 📊 Quick Stats")

    # Quick stats (dummy data por ahora)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Posts", "156", delta="12")
    with col2:
        st.metric("Success", "98%", delta="2%")

    st.markdown("---")

    st.markdown("## 🌐 Platforms")
    st.markdown("✅ **Instagram** - Connected")
    st.markdown("✅ **Twitter** - Connected")
    st.markdown("⏳ **Facebook** - Coming Soon")

    st.markdown("---")

    st.markdown("## 📖 Navigation")
    st.info("""
    Use the pages in the sidebar to:
    - 🏠 **Home** - Overview
    - 📊 **Analytics** - Metrics
    - 🤖 **Bot Control** - Start/Stop
    - 📸 **Posts** - Gallery
    - ⚙️ **Settings** - Configure
    """)

# Main content
st.title("🤖 Social Media Crossposting Dashboard")
st.markdown("### Welcome to your automated social media management system")

st.markdown("---")

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🚀 Quick Actions", "ℹ️ Info"])

with tab1:
    st.subheader("Dashboard Overview")

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Posts",
            value="156",
            delta="+23 this week",
            delta_color="normal"
        )

    with col2:
        st.metric(
            label="Avg. Engagement",
            value="12.5K",
            delta="+15%",
            delta_color="normal"
        )

    with col3:
        st.metric(
            label="Success Rate",
            value="98.2%",
            delta="+1.2%",
            delta_color="normal"
        )

    with col4:
        st.metric(
            label="Bot Status",
            value="Active",
            delta="2h uptime",
            delta_color="off"
        )

    st.markdown("---")

    # Gráfica placeholder
    st.subheader("📈 Posts Over Time (Last 7 Days)")
    st.info("📊 Analytics page will show interactive charts here. Navigate to **Analytics** page for full stats.")

    # Actividad reciente
    st.subheader("🕒 Recent Activity")

    activities = [
        {"time": "2 min ago", "action": "Post published on Twitter", "status": "success"},
        {"time": "15 min ago", "action": "New post downloaded from Instagram", "status": "success"},
        {"time": "1 hour ago", "action": "Bot started automatically", "status": "info"},
        {"time": "2 hours ago", "action": "Post published on Twitter", "status": "success"},
    ]

    for activity in activities:
        icon = "✅" if activity["status"] == "success" else "ℹ️"
        st.markdown(f"{icon} **{activity['time']}** - {activity['action']}")

with tab2:
    st.subheader("🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶️ Start Bot", use_container_width=True):
            st.success("Bot started! Go to **Bot Control** page for details.")

    with col2:
        if st.button("⏸️ Pause Bot", use_container_width=True):
            st.warning("Bot paused. Click **Start** to resume.")

    with col3:
        if st.button("🔄 Run Once", use_container_width=True):
            st.info("Running bot once... Check logs in **Bot Control** page.")

    st.markdown("---")

    st.subheader("⚙️ Quick Settings")

    col1, col2 = st.columns(2)

    with col1:
        check_interval = st.slider("Check Interval (minutes)", 5, 60, 15)
        st.caption("How often the bot checks for new posts")

    with col2:
        max_posts = st.number_input("Max Posts to Check", 1, 20, 5)
        st.caption("Number of recent posts to check each time")

    if st.button("💾 Save Settings"):
        st.success("Settings saved!")

with tab3:
    st.subheader("ℹ️ About This Dashboard")

    st.markdown("""
    This dashboard provides a visual interface to manage your social media crossposting bot.

    **Features:**
    - 📊 **Analytics** - Comprehensive metrics and charts
    - 🤖 **Bot Control** - Start, stop, and monitor the bot
    - 📸 **Posts Gallery** - View all published posts
    - ⚙️ **Settings** - Configure platforms and behavior
    - 📱 **Multi-platform** - Instagram, Twitter, Facebook (coming soon)

    **Tech Stack:**
    - **Frontend:** Streamlit + Plotly
    - **Backend:** Python + SQLite
    - **APIs:** Instagram (Instaloader), Twitter (Tweepy), Facebook (coming soon)

    **GitHub:** [ciempiesss/instagram-twitter-bot](https://github.com/ciempiesss/instagram-twitter-bot)
    """)

    st.markdown("---")

    st.success("✅ Bot is operational and ready to use!")

    st.markdown("**Next Steps:**")
    st.markdown("1. Navigate to **Analytics** to see detailed metrics")
    st.markdown("2. Use **Bot Control** to start/stop the bot")
    st.markdown("3. Configure settings in **Settings** page")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Made with ❤️ using Streamlit | "
    "<a href='https://github.com/ciempiesss/instagram-twitter-bot' target='_blank'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)
