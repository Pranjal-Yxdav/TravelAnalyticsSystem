import streamlit as st
import pandas as pd

from database import create_database
from auth import register_user, login_user
from analytics import (
    import_csv,
    generate_places,
    dashboard_data,
    user_history
)
from export_csv import export_results
from visualization import (
    generate_chart,
    generate_pie_chart,
    generate_line_chart,
    generate_horizontal_chart
)
from map_generator import generate_map
from streamlit_folium import st_folium


create_database()

st.set_page_config(
    page_title="Travel Analytics Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

.block-container{
padding-top:1rem;
}

/* Sidebar */

section[data-testid="stSidebar"]{
background:linear-gradient(
180deg,
#2563EB,
#1D4ED8
);
}

/* Dashboard Cards */

.metric-card{
background:linear-gradient(
135deg,
#2563EB,
#06B6D4
);
padding:25px;
border-radius:20px;
text-align:center;
transition:all 0.3s ease;
box-shadow:0px 8px 20px rgba(37,99,235,0.25);
}

.metric-card:hover{
transform:translateY(-8px);
box-shadow:0px 15px 35px rgba(6,182,212,0.45);
}

.metric-title{
font-size:16px;
color:white;
opacity:0.9;
}

.metric-value{
font-size:34px;
font-weight:bold;
color:white;
}

/* Buttons */

.stButton > button{
width:100%;
border-radius:12px;
font-weight:bold;
transition:0.3s;
background:linear-gradient(
90deg,
#2563EB,
#06B6D4
);
color:white;
border:none;
}

.stButton > button:hover{
transform:scale(1.03);
box-shadow:0px 0px 18px rgba(6,182,212,0.5);
}

/* DataFrame */

[data-testid="stDataFrame"]{
border-radius:15px;
overflow:hidden;
}

/* Metrics */

[data-testid="metric-container"]{
background:#1E293B;
padding:10px;
border-radius:15px;
}

/* Tabs */

.stTabs [data-baseweb="tab"]{
font-size:16px;
font-weight:bold;
padding:10px 20px;
border-radius:10px;
}

.stTabs [aria-selected="true"]{
background:#2563EB;
color:white;
}

/* Upload Area */

[data-testid="stFileUploader"]{
background:#1E293B;
padding:15px;
border-radius:15px;
}

/* Success Messages */

.stAlert{
border-radius:15px;
}

/* Smooth Animation */

html{
scroll-behavior:smooth;
}

</style>
""", unsafe_allow_html=True)



if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "menu" not in st.session_state: 
    st.session_state.menu = "📝 Register"

st.markdown(f"""
<div style="
padding:20px;
border-radius:15px;
background:linear-gradient(90deg,#8B5CF6,#EC4899);
color:white;
text-align:center;
margin-bottom:20px;
">
<h2>Welcome, {st.session_state.user_name} 👋</h2>
<p>Explore your travel insights and analytics.</p>
</div>
""", unsafe_allow_html=True)


st.sidebar.title("Navigation")

if st.session_state.user_id is None:
    if st.sidebar.button(
        "📝 Register",
        use_container_width=True
    ):
        st.session_state.menu = "📝 Register"
    if st.sidebar.button(
        "🔐 Login",
        use_container_width=True
    ):
        st.session_state.menu = "🔐 Login"

else:
    st.sidebar.success(
        f"👤 {st.session_state.user_name}"
    )
    if st.sidebar.button(
        "📊 Dashboard",
        use_container_width=True
    ):
        st.session_state.menu = "📊 Dashboard"
    if st.sidebar.button(
        "📁 Import CSV",
        use_container_width=True
    ):
        st.session_state.menu = "📁 Import CSV"
    if st.sidebar.button(
        "📈 Charts",
        use_container_width=True
    ):
        st.session_state.menu = "📈 Charts"
    if st.sidebar.button(
        "🗺️ Map",
        use_container_width=True
    ):
        st.session_state.menu = "🗺️ Map"
    if st.sidebar.button(
        "📥 Export CSV",
        use_container_width=True
    ):
        st.session_state.menu = "📥 Export CSV"
    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.menu = "🚪 Logout"
menu = st.session_state.menu

if menu == "📝 Register":

    st.subheader("Create Account")

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        name = st.text_input("Name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Register",
            use_container_width=True
        ):

            success = register_user(
                name,
                email,
                password
            )

            if success:

                st.success(
                    "Registration Successful"
                )

            else:

                st.error(
                    "User Already Exists"
                )

elif menu == "🔐 Login":

    st.subheader("Login")

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.user_id = user[0]
                st.session_state.user_name = user[1]
                st.session_state.menu = "📊 Dashboard"


                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )

elif menu == "📊 Dashboard":

    data = dashboard_data(
        st.session_state.user_id
    )

    st.markdown(f"""
    <div style="
    padding:20px;
    border-radius:15px;
    background:linear-gradient(90deg,#2563EB,#1D4ED8);
    color:white;
    text-align:center;
    margin-bottom:20px;
    ">
    <h2>Welcome, {st.session_state.user_name} 👋</h2>
    <p>Explore your travel insights and analytics.</p>
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">
        Records
        </div>
        <div class="metric-value">
        {data["records"]}
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">
        Places
        </div>
        <div class="metric-value">
        {data["places"]}
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">
        Distance KM
        </div>
        <div class="metric-value">
        {data["distance"]}
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-title">
        Visits
        </div>
        <div class="metric-value">
        {data["visits"]}
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📍 Most Visited Place")

    st.info(
        data["most_visited"]
    )

    st.markdown("---")

    st.subheader("🧭 Travel History")

    history = user_history(
        st.session_state.user_id
    )

    df = pd.DataFrame(
        history,
        columns=[
            "Timestamp",
            "Latitude",
            "Longitude"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

elif menu == "📁 Import CSV":

    uploaded_file = st.file_uploader(
        "Upload Travel Data",
        type=["csv"]
    )

    if uploaded_file:

        with st.spinner("Processing Travel Data..."):

            import_csv(
                uploaded_file,
                st.session_state.user_id
            )

            generate_places(
                st.session_state.user_id
            )

            st.success(
                "Data Imported Successfully"
            )

            st.balloons()

elif menu == "📈 Charts":

    tab1, tab2, tab3 = st.tabs(
        [
            "Bar Chart",
            "Pie Chart",
            "Line Chart"
        ]
    )

    with tab1:

        fig = generate_chart(
            st.session_state.user_id
        )

        if fig:
            st.pyplot(fig)

    with tab2:

        fig = generate_pie_chart(
            st.session_state.user_id
        )

        if fig:
            st.pyplot(fig)

    with tab3:

        fig = generate_line_chart(
            st.session_state.user_id
        )

        if fig:
            st.pyplot(fig)

elif menu == "🗺️ Map":

    travel_map = generate_map(
        st.session_state.user_id
    )

    if travel_map:

        st_folium(
            travel_map,
            width=1200,
            height=650
        )


elif menu == "📥 Export CSV":

    file = export_results(
        st.session_state.user_id,
        st.session_state.user_name
    )

    with open(
        file,
        "rb"
    ) as f:

        st.download_button(
            label="Download Analytics CSV",
            data=f,
            file_name="analytics_export.csv",
            mime="text/csv",
            use_container_width=True
        )

elif menu == "🚪 Logout":

    st.session_state.user_id = None
    st.session_state.user_name = None

    st.rerun()

st.markdown("""
<hr>
<center>
🌍 Travel Analytics Dashboard • Built with Python, Streamlit, Folium & SQLite
</center>
""", unsafe_allow_html=True)