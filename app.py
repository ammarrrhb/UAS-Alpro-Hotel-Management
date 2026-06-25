import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

from modules import storage
from modules.auth import login
from modules.models import Kamar, Tamu
from modules import services

# ─── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="Hotel Telkoms",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Initialize Storage ───────────────────────────────────
storage.init_storage()

# ─── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #f5f6ff;
    font-family: 'Poppins', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #6366f1  0%, #818cf8  100%) !important;
    border-right: none !important;
    font-family: 'Poppins', sans-serif !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
    font-family: 'Poppins', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio > label {
    color: #94a3b8 !important;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.5rem 0 0.25rem;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.65rem 1rem;
    border-radius: 10px;
    margin: 2px 0;
    transition: all 0.2s;
    cursor: pointer;
    font-size: 0.9rem !important;
    color: #cbd5e1 !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #fff !important;
}

/* ── Metric Cards ── */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.04);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.10);
}
.metric-icon {
    font-size: 1.8rem;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #1a1f36;
    line-height: 1;
    margin: 0.2rem 0;
}
.metric-label {
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.metric-sub {
    color: #94a3b8;
    font-size: 0.75rem;
    margin-top: 0.4rem;
}

/* ── Section Header ── */
.section-header {
    font-family: 'Poppins', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a1f36;
    margin-bottom: 0.25rem;
}
.section-sub {
    color: #64748b;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* ── Cards ── */
.card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}

/* ── Status Badges ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-tersedia { background: #dcfce7; color: #16a34a; }
.badge-terisi   { background: #fef9c3; color: #ca8a04; }
.badge-maint    { background: #fee2e2; color: #dc2626; }
.badge-reservasi{ background: #dbeafe; color: #2563eb; }
.badge-checkin  { background: #fef9c3; color: #ca8a04; }
.badge-checkout { background: #f0fdf4; color: #16a34a; }
.badge-batal    { background: #f1f5f9; color: #64748b; }

/* ── Login Screen ── */
.login-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #6366f1  0%, #818cf8  50%, #1e3a5f 100%);
}
.login-card {
    background: rgba(255,255,255,0.97);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    width: 420px;
    box-shadow: 0 40px 80px rgba(0,0,0,0.3);
}
.login-logo {
    font-family: 'Poppins', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #1a1f36;
    text-align: center;
    margin-bottom: 0.2rem;
}
.login-sub {
    color: #64748b;
    text-align: center;
    font-size: 0.85rem;
    margin-bottom: 2rem;
}

/* ── Streamlit Overrides ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Poppins', sans-serif !important;
    transition: all 0.2s !important;
}
/* ── Logout Button (red) ── */
[data-testid="stSidebar"] .stButton > button {
    background-color: #dc2626 !important;
    color: white !important;
    border: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #b91c1c !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(220,38,38,0.4) !important;
}
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-family: 'Poppins', sans-serif !important;
}
div[data-testid="stForm"] {
    background: white;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.04);
}
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
}
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 12px !important;
    font-family: 'Poppins', sans-serif !important;
}

/* ── Welcome Header ── */
.welcome-header {
    background: linear-gradient(135deg, #6366f1  0%, #818cf8  100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    color: white;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.welcome-header::after {
    content: '🏨';
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 4rem;
    
}
.welcome-greeting {
    font-size: 0.85rem;
    font-weight: 500;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.welcome-name {
    font-family: 'Poppins', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: white;
    margin: 0.2rem 0;
}
.welcome-info {
    color: #94a3b8;
    font-size: 0.875rem;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: #e2e8f0;
    margin: 1.5rem 0;
}

/* ── Room Card Grid ── */
.room-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
}
.room-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem;
    border: 2px solid #e2e8f0;
    transition: all 0.2s;
}
.room-card:hover { border-color: #2d3561; transform: translateY(-2px); }
.room-number { font-size: 1.5rem; font-weight: 700; color: #1a1f36; }
.room-type { color: #64748b; font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.room-price { color: #2d3561; font-size: 0.95rem; font-weight: 600; margin-top: 0.5rem; }

/* ── Sidebar Logo ── */
.sidebar-logo {
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1rem;
}
.logo-text {
    font-family: 'Poppins', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
}
.logo-sub {
    font-size: 0.7rem;
    color: #94a3b8;
    font-weight: 400;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Bill Card ── */
.bill-card {
    background: linear-gradient(135deg, #6366f1  0%, #818cf8  100%);
    border-radius: 20px;
    padding: 2rem;
    color: white;
}
.bill-title { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; }
.bill-total { font-family: 'Poppins', sans-serif; font-size: 2.5rem; font-weight: 700; }
.bill-row { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 0.875rem; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "admin_name" not in st.session_state:
    st.session_state.admin_name = ""
if "username" not in st.session_state:
    st.session_state.username = ""

# ─── Helper: Status Badge HTML ─────────────────────────────
def badge(status: str) -> str:
    cls_map = {
        "Tersedia": "badge-tersedia",
        "Terisi": "badge-terisi",
        "Maintenance": "badge-maint",
        "Reservasi": "badge-reservasi",
        "Check-In": "badge-checkin",
        "Check-Out": "badge-checkout",
        "Batal": "badge-batal",
    }
    cls = cls_map.get(status, "badge-reservasi")
    return f'<span class="badge {cls}">{status}</span>'


def fmt_rupiah(amount: float) -> str:
    return f"Rp {amount:,.0f}"


# ══════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════
def halaman_login():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; margin-bottom: 2rem;">
            <div style="font-size: 3rem;">🏨</div>
            <div style="font-family:'Poppins',sans-serif; font-size:2rem; font-weight:700; color:#1a1f36;">Hotel Telkoms</div>
            <div style="color:#64748b; font-size:0.85rem; margin-top:0.25rem;">Admin Management System</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("#### Masuk ke Dashboard")
            username = st.text_input("👤 Username", placeholder="Masukkan username")
            password = st.text_input("🔒 Password", type="password", placeholder="Masukkan password")
            col_a, col_b = st.columns([1, 1])
            with col_b:
                submitted = st.form_submit_button("Masuk →", use_container_width=True, type="primary")

            if submitted:
                if not username or not password:
                    st.error("Username dan password tidak boleh kosong.")
                else:
                    success, msg = login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.admin_name = msg
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

        st.markdown("""
        <div style="text-align:center; margin-top:1.5rem; color:#94a3b8; font-size:0.78rem;">
            Demo: <b>admin</b> / <b>hotel123</b> &nbsp;|&nbsp; <b>manager</b> / <b>manager456</b>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-logo">
            <div class="logo-text">🏨 Hotel Telkoms</div>
            <div class="logo-sub">Admin Dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="padding: 0.75rem 1rem; background: rgba(255,255,255,0.06); border-radius:10px; margin-bottom:1rem;">
            <div style="font-family: 'Poppins'; font-size:0.7rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.08em;">Logged in as</div>
            <div style="font-family: 'Poppins'; font-size:0.95rem; font-weight:600; color:white; margin-top:0.15rem;">👤 {st.session_state.admin_name}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p style="color:#c7d2fe; font-size:0.72rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; padding: 0.5rem 0 0.25rem; margin:0;">MENU NAVIGASI</p>', unsafe_allow_html=True)
        menu = st.radio(
            "MENU NAVIGASI",
            [
                "🏠 Dashboard",
                "🛏️ Kelola Kamar",
                "👤 Kelola Tamu",
                "📋 Reservasi Baru",
                "✅ Check-In",
                "🔑 Check-Out",
                "📊 Riwayat & Laporan",
            ],
            label_visibility="collapsed",
        )

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="padding: 0 1rem; color:#64748b; font-size:0.72rem;">
            📅 {datetime.now().strftime('%A, %d %B %Y')}<br>
            🕐 {datetime.now().strftime('%H:%M WIB')}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.admin_name = ""
            st.rerun()

    return menu


# ══════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════
def halaman_dashboard():
    stats = services.get_statistik()

    st.markdown(f"""
    <div class="welcome-header">
        <div class="welcome-greeting" style="color: white;">Selamat Datang</div>
        <div class="welcome-name">{st.session_state.admin_name}</div>
        <div class="welcome-info" style="color: white;">📅 {datetime.now().strftime('%A, %d %B %Y  ·  %H:%M WIB')} &nbsp;·&nbsp; Hotel Telkoms, DI Pandjaitan</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric Cards ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🛏️</div>
            <div class="metric-value">{stats['kamar_tersedia']}<span style="font-size:1rem;color:#94a3b8;">/{stats['total_kamar']}</span></div>
            <div class="metric-label">Kamar Tersedia</div>
            <div class="metric-sub">Occupancy: {stats['occupancy_rate']:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-value">{stats['total_tamu']}</div>
            <div class="metric-label">Total Tamu</div>
            <div class="metric-sub">Terdaftar di sistem</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-value">{stats['reservasi_aktif']}</div>
            <div class="metric-label">Reservasi Aktif</div>
            <div class="metric-sub">Check-in hari ini: {stats['checkin_hari_ini']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        pendapatan = stats['total_pendapatan']
        if pendapatan >= 1_000_000:
            val_str = f"{pendapatan/1_000_000:.1f}Jt"
        else:
            val_str = f"{pendapatan/1_000:.0f}Rb"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-value" style="font-size:1.8rem;">Rp {val_str}</div>
            <div class="metric-label">Total Pendapatan</div>
            <div class="metric-sub">Dari {stats['total_reservasi']} reservasi</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="section-header">📈 Aktivitas Reservasi (7 Hari Terakhir)</div>', unsafe_allow_html=True)
        res_list = storage.baca_semua_reservasi()
        if res_list:
            df_res = pd.DataFrame([r.to_dict() for r in res_list])
            df_res["tanggal_reservasi"] = pd.to_datetime(df_res["tanggal_reservasi"], errors="coerce")
            last7 = datetime.now() - timedelta(days=7)
            df_week = df_res[df_res["tanggal_reservasi"] >= last7].copy()
            if not df_week.empty:
                df_week["hari"] = df_week["tanggal_reservasi"].dt.strftime("%d %b")
                daily = df_week.groupby("hari").size().reset_index(name="count")
                fig = px.area(
                    daily, x="hari", y="count",
                    color_discrete_sequence=["#2d3561"],
                    labels={"hari": "Tanggal", "count": "Jumlah Reservasi"},
                )
                fig.update_layout(
                    plot_bgcolor="white", paper_bgcolor="white",
                    margin=dict(l=10, r=10, t=10, b=10),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                    font=dict(family="Inter"),
                )
                fig.update_traces(fill="tozeroy", line_color="#2d3561", fillcolor="rgba(45,53,97,0.08)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Belum ada reservasi dalam 7 hari terakhir.")
        else:
            st.info("Belum ada data reservasi.")

    with col_right:
        st.markdown('<div class="section-header">🔑 Booking Terbaru</div>', unsafe_allow_html=True)
        res_list = storage.baca_semua_reservasi()
        res_aktif = [r for r in res_list if r.status in ("Reservasi", "Check-In")]
        res_aktif.sort(key=lambda x: x.tanggal_reservasi, reverse=True)

        if res_aktif:
            for r in res_aktif[:5]:
                status_color = {"Reservasi": "#2563eb", "Check-In": "#ca8a04"}.get(r.status, "#64748b")
                st.markdown(f"""
                <div style="background:white; border-radius:12px; padding:0.9rem 1rem; margin-bottom:0.6rem; border-left:3px solid {status_color}; box-shadow:0 1px 6px rgba(0,0,0,0.06);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-weight:600; font-size:0.9rem; color:#1a1f36;">{r.nama_tamu}</div>
                            <div style="color:#64748b; font-size:0.75rem;">Kamar {r.nomor_kamar} · {r.tipe_kamar}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:0.7rem; font-weight:600; color:{status_color}; background:{'#dbeafe' if r.status=='Reservasi' else '#fef9c3'}; padding:0.15rem 0.5rem; border-radius:6px;">{r.status}</div>
                        </div>
                    </div>
                    <div style="margin-top:0.4rem; color:#94a3b8; font-size:0.72rem;">📅 {r.tanggal_checkin} → {r.tanggal_checkout}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:white; border-radius:12px; padding:2rem; text-align:center; color:#94a3b8;">
                <div style="font-size:2rem;">📋</div>
                <div>Belum ada reservasi aktif</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Occupancy Donut ──
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">🛏️ Status Kamar</div>', unsafe_allow_html=True)
        kamar_list = storage.baca_semua_kamar()
        if kamar_list:
            status_counts = pd.Series([k.status for k in kamar_list]).value_counts()
            fig2 = go.Figure(data=[go.Pie(
                labels=status_counts.index.tolist(),
                values=status_counts.values.tolist(),
                hole=0.55,
                marker_colors=["#16a34a", "#ca8a04", "#dc2626"],
            )])
            fig2.update_layout(
                showlegend=True, paper_bgcolor="white",
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(family="Inter"),
                legend=dict(orientation="h", y=-0.1),
            )
            fig2.update_traces(textinfo="percent+label")
            st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">💰 Pendapatan per Tipe Kamar</div>', unsafe_allow_html=True)
        res_list = storage.baca_semua_reservasi()
        checkout_res = [r for r in res_list if r.status == "Check-Out"]
        if checkout_res:
            df_p = pd.DataFrame([{"tipe": r.tipe_kamar, "total": r.total_biaya} for r in checkout_res])
            df_p = df_p.groupby("tipe")["total"].sum().reset_index()
            fig3 = px.bar(
                df_p, x="tipe", y="total",
                color_discrete_sequence=["#2d3561", "#4f6af5", "#94a3b8"],
                labels={"tipe": "Tipe Kamar", "total": "Total (Rp)"},
                color="tipe",
            )
            fig3.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                font=dict(family="Inter"),
                showlegend=False,
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Belum ada data pendapatan.")


# ══════════════════════════════════════════════════════════
#  PAGE: KELOLA KAMAR
# ══════════════════════════════════════════════════════════
def halaman_kamar():
    st.markdown('<div class="section-header">🛏️ Manajemen Kamar</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Kelola data kamar hotel — tambah, ubah, dan hapus kamar</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Daftar Kamar", "➕ Tambah Kamar", "✏️ Edit / Hapus Kamar"])

    with tab1:
        kamar_list = storage.baca_semua_kamar()
        if kamar_list:
            # Filter
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                filter_tipe = st.selectbox("Filter Tipe", ["Semua", "Standard", "Deluxe", "Suite"])
            with col_f2:
                filter_status = st.selectbox("Filter Status", ["Semua", "Tersedia", "Terisi", "Maintenance"])

            filtered = kamar_list
            if filter_tipe != "Semua":
                filtered = [k for k in filtered if k.tipe == filter_tipe]
            if filter_status != "Semua":
                filtered = [k for k in filtered if k.status == filter_status]

            df = pd.DataFrame([k.to_dict() for k in filtered])
            df.columns = ["No. Kamar", "Tipe", "Harga/Malam", "Kapasitas", "Fasilitas", "Status"]
            df["Harga/Malam"] = df["Harga/Malam"].apply(lambda x: fmt_rupiah(float(x)))
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown(f"""
            <div style="display:flex; gap:1rem; margin-top:0.5rem; flex-wrap:wrap;">
                <div style="background:#dcfce7; color:#16a34a; padding:0.4rem 1rem; border-radius:8px; font-size:0.8rem; font-weight:600;">
                    ✅ Tersedia: {sum(1 for k in kamar_list if k.status=='Tersedia')}
                </div>
                <div style="background:#fef9c3; color:#ca8a04; padding:0.4rem 1rem; border-radius:8px; font-size:0.8rem; font-weight:600;">
                    🏃 Terisi: {sum(1 for k in kamar_list if k.status=='Terisi')}
                </div>
                <div style="background:#fee2e2; color:#dc2626; padding:0.4rem 1rem; border-radius:8px; font-size:0.8rem; font-weight:600;">
                    🔧 Maintenance: {sum(1 for k in kamar_list if k.status=='Maintenance')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Belum ada data kamar.")

    with tab2:
        with st.form("form_tambah_kamar"):
            st.markdown("#### Tambah Kamar Baru")
            col1, col2 = st.columns(2)
            with col1:
                nomor = st.text_input("Nomor Kamar*", placeholder="cth: 401")
                tipe = st.selectbox("Tipe Kamar*", ["Standard", "Deluxe", "Suite"])
                harga = st.number_input("Harga per Malam (Rp)*", min_value=0, step=50000, value=350000)
            with col2:
                kapasitas = st.number_input("Kapasitas Tamu*", min_value=1, max_value=10, value=2)
                status = st.selectbox("Status Awal", ["Tersedia", "Maintenance"])
                fasilitas = st.text_area("Fasilitas", placeholder="cth: AC, TV, WiFi, Kamar Mandi")

            submitted = st.form_submit_button("💾 Simpan Kamar", type="primary", use_container_width=True)
            if submitted:
                if not nomor or not fasilitas:
                    st.error("Nomor kamar dan fasilitas wajib diisi.")
                elif storage.cari_kamar(nomor):
                    st.error(f"Kamar dengan nomor '{nomor}' sudah ada.")
                else:
                    kamar = Kamar(nomor, tipe, float(harga), kapasitas, fasilitas, status)
                    storage.simpan_kamar(kamar)
                    st.success(f"✅ Kamar {nomor} ({tipe}) berhasil ditambahkan!")
                    st.rerun()

    with tab3:
        kamar_list = storage.baca_semua_kamar()
        if not kamar_list:
            st.info("Belum ada data kamar.")
        else:
            nomor_pilih = st.selectbox(
                "Pilih Kamar",
                [f"{k.nomor_kamar} — {k.tipe} ({k.status})" for k in kamar_list]
            )
            nomor_sel = nomor_pilih.split(" — ")[0]
            kamar_sel = storage.cari_kamar(nomor_sel)

            if kamar_sel:
                with st.form("form_edit_kamar"):
                    st.markdown(f"#### Edit Kamar {kamar_sel.nomor_kamar}")
                    col1, col2 = st.columns(2)
                    with col1:
                        new_tipe = st.selectbox("Tipe", ["Standard", "Deluxe", "Suite"],
                                                index=["Standard", "Deluxe", "Suite"].index(kamar_sel.tipe))
                        new_harga = st.number_input("Harga/Malam", value=int(kamar_sel.harga_per_malam), step=50000)
                    with col2:
                        new_kapasitas = st.number_input("Kapasitas", value=kamar_sel.kapasitas, min_value=1, max_value=10)
                        new_status = st.selectbox("Status", ["Tersedia", "Terisi", "Maintenance"],
                                                  index=["Tersedia", "Terisi", "Maintenance"].index(kamar_sel.status))
                    new_fasilitas = st.text_area("Fasilitas", value=kamar_sel.fasilitas)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        save = st.form_submit_button("💾 Simpan Perubahan", type="primary", use_container_width=True)
                    with col_b:
                        delete = st.form_submit_button("🗑️ Hapus Kamar", use_container_width=True)

                    if save:
                        aktif = storage.reservasi_aktif_kamar(nomor_sel)
                        if aktif and new_status == "Tersedia":
                            st.error(f"Kamar masih memiliki reservasi aktif (ID: {aktif.id_reservasi}). Selesaikan dulu sebelum mengubah status.")
                        else:
                            updated = Kamar(nomor_sel, new_tipe, float(new_harga), new_kapasitas, new_fasilitas, new_status)
                            storage.simpan_kamar(updated)
                            st.success("✅ Data kamar berhasil diperbarui!")
                            st.rerun()
                    if delete:
                        aktif = storage.reservasi_aktif_kamar(nomor_sel)
                        if aktif:
                            st.error(f"Tidak dapat menghapus kamar yang memiliki reservasi aktif.")
                        else:
                            storage.hapus_kamar(nomor_sel)
                            st.success(f"🗑️ Kamar {nomor_sel} berhasil dihapus.")
                            st.rerun()


# ══════════════════════════════════════════════════════════
#  PAGE: KELOLA TAMU
# ══════════════════════════════════════════════════════════
def halaman_tamu():
    st.markdown('<div class="section-header">👤 Manajemen Tamu</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Daftarkan dan kelola data tamu hotel</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 Daftar Tamu", "➕ Tambah Tamu", "✏️ Edit / Hapus Tamu"])

    with tab1:
        tamu_list = storage.baca_semua_tamu()
        if tamu_list:
            search = st.text_input("🔍 Cari tamu (nama / ID / NIK)", placeholder="Ketik untuk mencari...")
            filtered = tamu_list
            if search:
                s = search.lower()
                filtered = [t for t in tamu_list if s in t.nama.lower() or s in t.id_tamu.lower() or s in t.nik.lower()]

            df = pd.DataFrame([t.to_dict() for t in filtered])
            df.columns = ["ID Tamu", "Nama", "NIK", "Telepon", "Email", "Alamat", "Tgl Daftar"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Menampilkan {len(filtered)} dari {len(tamu_list)} tamu")
        else:
            st.info("Belum ada data tamu. Silakan tambah tamu terlebih dahulu.")

    with tab2:
        with st.form("form_tambah_tamu"):
            st.markdown("#### Daftarkan Tamu Baru")
            col1, col2 = st.columns(2)
            with col1:
                nama = st.text_input("Nama Lengkap*", placeholder="cth: Budi Santoso")
                nik = st.text_input("NIK (KTP)*", placeholder="16 digit NIK")
                telepon = st.text_input("No. Telepon*", placeholder="cth: 081234567890")
            with col2:
                email = st.text_input("Email", placeholder="cth: budi@email.com")
                alamat = st.text_area("Alamat*", placeholder="Alamat lengkap")

            submitted = st.form_submit_button("💾 Daftarkan Tamu", type="primary", use_container_width=True)
            if submitted:
                if not nama or not nik or not telepon or not alamat:
                    st.error("Nama, NIK, Telepon, dan Alamat wajib diisi.")
                elif len(nik) != 16 or not nik.isdigit():
                    st.error("NIK harus berupa 16 digit angka.")
                else:
                    # Check duplicate NIK
                    tamu_list = storage.baca_semua_tamu()
                    if any(t.nik == nik for t in tamu_list):
                        st.error(f"Tamu dengan NIK {nik} sudah terdaftar.")
                    else:
                        id_tamu = storage.generate_id_tamu()
                        tamu = Tamu(id_tamu, nama, nik, telepon, email, alamat)
                        storage.simpan_tamu(tamu)
                        st.success(f"✅ Tamu **{nama}** berhasil didaftarkan! ID: **{id_tamu}**")
                        st.rerun()

    with tab3:
        tamu_list = storage.baca_semua_tamu()
        if not tamu_list:
            st.info("Belum ada data tamu.")
        else:
            tamu_options = [f"{t.id_tamu} — {t.nama}" for t in tamu_list]
            tamu_pilih = st.selectbox("Pilih Tamu", tamu_options)
            id_sel = tamu_pilih.split(" — ")[0]
            tamu_sel = storage.cari_tamu(id_sel)

            if tamu_sel:
                with st.form("form_edit_tamu"):
                    st.markdown(f"#### Edit Tamu: {tamu_sel.nama}")
                    col1, col2 = st.columns(2)
                    with col1:
                        new_nama = st.text_input("Nama Lengkap", value=tamu_sel.nama)
                        new_nik = st.text_input("NIK", value=tamu_sel.nik)
                        new_telp = st.text_input("Telepon", value=tamu_sel.telepon)
                    with col2:
                        new_email = st.text_input("Email", value=tamu_sel.email)
                        new_alamat = st.text_area("Alamat", value=tamu_sel.alamat)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        save = st.form_submit_button("💾 Simpan", type="primary", use_container_width=True)
                    with col_b:
                        delete = st.form_submit_button("🗑️ Hapus Tamu", use_container_width=True)

                    if save:
                        updated = Tamu(tamu_sel.id_tamu, new_nama, new_nik, new_telp, new_email, new_alamat, tamu_sel.tanggal_daftar)
                        storage.simpan_tamu(updated)
                        st.success("✅ Data tamu berhasil diperbarui!")
                        st.rerun()
                    if delete:
                        storage.hapus_tamu(id_sel)
                        st.success(f"🗑️ Tamu {tamu_sel.nama} berhasil dihapus.")
                        st.rerun()


# ══════════════════════════════════════════════════════════
#  PAGE: RESERVASI BARU
# ══════════════════════════════════════════════════════════
def halaman_reservasi():
    st.markdown('<div class="section-header">📋 Reservasi Kamar</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Buat pemesanan kamar untuk tamu</div>', unsafe_allow_html=True)

    tamu_list = storage.baca_semua_tamu()
    semua_kamar = storage.baca_semua_kamar()

    if not tamu_list:
        st.warning("⚠️ Belum ada tamu terdaftar. Silakan daftarkan tamu terlebih dahulu di menu **Kelola Tamu**.")
        return

    col_form, col_preview = st.columns([3, 2])

    with col_form:
        with st.form("form_reservasi"):
            st.markdown("#### Informasi Pemesanan")

            tamu_options = {f"{t.id_tamu} — {t.nama}": t for t in tamu_list}
            tamu_pilih = st.selectbox("👤 Tamu*", list(tamu_options.keys()))

            # Room filter by type (dependent dropdown)
            tipe_filter = st.selectbox("🏷️ Filter Tipe Kamar", ["Semua", "Standard", "Deluxe", "Suite"])

            # Filter rooms by selected type (but keep full data for checking availability)
            if tipe_filter == "Semua":
                filtered_by_type = semua_kamar
            else:
                filtered_by_type = [k for k in semua_kamar if k.tipe == tipe_filter]

            # From that subset, only keep rooms that are EXACTLY 'Tersedia'
            available_kamar = [k for k in filtered_by_type if k.status == "Tersedia"]

            # If no available room for the selected type, show clear warning and disable submit
            submit_disabled = False
            if tipe_filter != "Semua" and not available_kamar:
                st.warning("⚠️ No rooms available for this type! Please choose another room type.")
                submit_disabled = True

            # Only show the room selectbox when there are available rooms
            kamar_pilih = None
            kamar_options = {}
            if available_kamar:
                kamar_options = {f"Kamar {k.nomor_kamar} — {k.tipe} ({fmt_rupiah(k.harga_per_malam)}/malam)": k for k in available_kamar}
                kamar_pilih = st.selectbox("🛏️ Kamar*", list(kamar_options.keys()))

            col1, col2 = st.columns(2)
            with col1:
                checkin = st.date_input("📅 Check-In*", value=date.today() + timedelta(days=1), min_value=date.today())
            with col2:
                checkout = st.date_input("📅 Check-Out*", value=date.today() + timedelta(days=2), min_value=date.today() + timedelta(days=1))

            catatan = st.text_area("📝 Catatan Khusus", placeholder="Permintaan kamar, kebutuhan khusus, dsb.")

            submitted = st.form_submit_button("📋 Buat Reservasi", type="primary", use_container_width=True, disabled=submit_disabled)

            # Prevent submission if no valid room selected
            if submitted:
                if not kamar_pilih or kamar_pilih not in kamar_options:
                    st.error("⚠️ Tidak ada kamar yang dipilih atau kamar tidak tersedia. Pilih tipe kamar lain atau refresh daftar.")
                else:
                    tamu_sel = tamu_options[tamu_pilih]
                    kamar_sel = kamar_options[kamar_pilih]
                    success, msg, res = services.buat_reservasi(
                        tamu_sel.id_tamu, kamar_sel.nomor_kamar,
                        checkin, checkout, catatan
                    )
                    if success:
                        st.success(f"✅ {msg}")
                        st.balloons()
                    else:
                        st.error(f"❌ {msg}")

    with col_preview:
        st.markdown("#### 💡 Info Kamar")
        kamar_list_all = storage.baca_semua_kamar()
        tersedia = [k for k in kamar_list_all if k.status == "Tersedia"]
        for k in tersedia[:4]:
            color = {"Standard": "#2563eb", "Deluxe": "#7c3aed", "Suite": "#ca8a04"}.get(k.tipe, "#64748b")
            st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:1rem; margin-bottom:0.6rem; border-left:3px solid {color}; box-shadow:0 1px 6px rgba(0,0,0,0.05);">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <span style="font-size:1.1rem; font-weight:700; color:#1a1f36;">Kamar {k.nomor_kamar}</span>
                        <span style="margin-left:0.5rem; font-size:0.75rem; font-weight:600; color:{color}; background:{'#dbeafe' if k.tipe=='Standard' else '#ede9fe' if k.tipe=='Deluxe' else '#fef9c3'}; padding:0.1rem 0.5rem; border-radius:6px;">{k.tipe}</span>
                    </div>
                    <div style="font-size:0.75rem; color:#16a34a; font-weight:600;">● Tersedia</div>
                </div>
                <div style="color:#2d3561; font-weight:600; margin-top:0.3rem;">{fmt_rupiah(k.harga_per_malam)}<span style="color:#94a3b8; font-weight:400;">/malam</span></div>
                <div style="color:#94a3b8; font-size:0.75rem; margin-top:0.2rem;">👥 {k.kapasitas} tamu · {k.fasilitas[:40]}{'...' if len(k.fasilitas)>40 else ''}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE: CHECK-IN
# ══════════════════════════════════════════════════════════
def halaman_checkin():
    st.markdown('<div class="section-header">✅ Proses Check-In</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Konfirmasi kedatangan tamu dan mulai masa menginap</div>', unsafe_allow_html=True)

    res_list = [r for r in storage.baca_semua_reservasi() if r.status == "Reservasi"]

    if not res_list:
        st.info("📭 Tidak ada reservasi yang menunggu check-in saat ini.")
        return

    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("form_checkin"):
            st.markdown("#### Pilih Reservasi untuk Check-In")
            res_options = {
                f"{r.id_reservasi} — {r.nama_tamu} (Kamar {r.nomor_kamar}, {r.tanggal_checkin})": r
                for r in sorted(res_list, key=lambda x: x.tanggal_checkin)
            }
            res_pilih = st.selectbox("📋 Reservasi*", list(res_options.keys()))
            res_sel = res_options[res_pilih]

            # Show detail card
            st.markdown(f"""
            <div style="background:#f8fafc; border-radius:12px; padding:1rem; margin:0.5rem 0; border:1px solid #e2e8f0;">
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                    <div><span style="color:#64748b; font-size:0.75rem;">ID Reservasi</span><br><b>{res_sel.id_reservasi}</b></div>
                    <div><span style="color:#64748b; font-size:0.75rem;">Tamu</span><br><b>{res_sel.nama_tamu}</b></div>
                    <div><span style="color:#64748b; font-size:0.75rem;">Kamar</span><br><b>{res_sel.nomor_kamar} — {res_sel.tipe_kamar}</b></div>
                    <div><span style="color:#64748b; font-size:0.75rem;">Lama Menginap</span><br><b>{res_sel.jumlah_malam} malam</b></div>
                    <div><span style="color:#64748b; font-size:0.75rem;">Check-In</span><br><b>{res_sel.tanggal_checkin}</b></div>
                    <div><span style="color:#64748b; font-size:0.75rem;">Check-Out</span><br><b>{res_sel.tanggal_checkout}</b></div>
                </div>
                <div style="margin-top:0.75rem; padding-top:0.75rem; border-top:1px solid #e2e8f0;">
                    <span style="color:#64748b; font-size:0.75rem;">Total Biaya</span><br>
                    <span style="font-size:1.2rem; font-weight:700; color:#1a1f36;">{fmt_rupiah(res_sel.total_biaya)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            submitted = st.form_submit_button("✅ Konfirmasi Check-In", type="primary", use_container_width=True)
            if submitted:
                success, msg = services.proses_checkin(res_sel.id_reservasi)
                if success:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    with col2:
        st.markdown("#### 📊 Statistik")
        stats = services.get_statistik()
        for label, val, color in [
            ("Menunggu Check-In", len(res_list), "#2563eb"),
            ("Kamar Tersedia", stats["kamar_tersedia"], "#16a34a"),
            ("Sudah Check-In Hari Ini", stats["checkin_hari_ini"], "#ca8a04"),
        ]:
            st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:1rem; margin-bottom:0.6rem; text-align:center; box-shadow:0 1px 6px rgba(0,0,0,0.05);">
                <div style="font-size:1.8rem; font-weight:700; color:{color};">{val}</div>
                <div style="color:#64748b; font-size:0.8rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE: CHECK-OUT
# ══════════════════════════════════════════════════════════
def halaman_checkout():
    st.markdown('<div class="section-header">🔑 Proses Check-Out</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Proses kepulangan tamu dan cetak tagihan akhir</div>', unsafe_allow_html=True)

    res_list = [r for r in storage.baca_semua_reservasi() if r.status == "Check-In"]

    if not res_list:
        st.info("📭 Tidak ada tamu yang sedang check-in saat ini.")
        return

    col1, col2 = st.columns([3, 2])

    with col1:
        with st.form("form_checkout"):
            st.markdown("#### Pilih Tamu untuk Check-Out")
            res_options = {
                f"{r.id_reservasi} — {r.nama_tamu} (Kamar {r.nomor_kamar})": r
                for r in res_list
            }
            res_pilih = st.selectbox("📋 Reservasi*", list(res_options.keys()))
            res_sel = res_options[res_pilih]

            submitted = st.form_submit_button("🔑 Proses Check-Out & Cetak Tagihan", type="primary", use_container_width=True)
            if submitted:
                success, msg, res_done = services.proses_checkout(res_sel.id_reservasi)
                if success:
                    st.success(f"✅ {msg}")
                    # Show bill
                    if res_done:
                        st.markdown(f"""
                        <div class="bill-card" style="margin-top:1rem;">
                            <div class="bill-title">🧾 INVOICE CHECK-OUT</div>
                            <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:1rem;">{res_done.id_reservasi} · {datetime.now().strftime('%d %b %Y %H:%M')}</div>
                            <div class="bill-row"><span>Tamu</span><span>{res_done.nama_tamu}</span></div>
                            <div class="bill-row"><span>Kamar</span><span>{res_done.nomor_kamar} ({res_done.tipe_kamar})</span></div>
                            <div class="bill-row"><span>Check-In</span><span>{res_done.tanggal_checkin}</span></div>
                            <div class="bill-row"><span>Check-Out</span><span>{res_done.tanggal_checkout}</span></div>
                            <div class="bill-row"><span>Lama Menginap</span><span>{res_done.jumlah_malam} malam</span></div>
                            <div class="bill-row"><span>Harga/Malam</span><span>{fmt_rupiah(res_done.harga_per_malam)}</span></div>
                            <div style="margin-top:1rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,0.2);">
                                <div class="bill-title">TOTAL TAGIHAN</div>
                                <div class="bill-total">{fmt_rupiah(res_done.total_biaya)}</div>
                            </div>
                            <div style="text-align:center; margin-top:1rem; font-size:0.75rem; color:#64748b;">
                                Terima kasih telah menginap di Hotel Switz 🏨
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    with col2:
        st.markdown("#### 🛏️ Tamu yang Sedang Menginap")
        for r in res_list:
            checkin_dt = datetime.strptime(r.tanggal_checkin, "%Y-%m-%d").date()
            lama = (date.today() - checkin_dt).days
            st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:1rem; margin-bottom:0.6rem; box-shadow:0 1px 6px rgba(0,0,0,0.05);">
                <div style="font-weight:700; color:#1a1f36;">{r.nama_tamu}</div>
                <div style="color:#64748b; font-size:0.8rem;">Kamar {r.nomor_kamar} · {r.tipe_kamar}</div>
                <div style="color:#94a3b8; font-size:0.75rem; margin-top:0.3rem;">🗓️ Menginap {lama} hari · Checkout: {r.tanggal_checkout}</div>
                <div style="color:#2d3561; font-weight:600; font-size:0.85rem; margin-top:0.3rem;">{fmt_rupiah(r.total_biaya)}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE: RIWAYAT & LAPORAN
# ══════════════════════════════════════════════════════════
def halaman_riwayat():
    st.markdown('<div class="section-header">📊 Riwayat & Laporan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Histori seluruh transaksi reservasi hotel</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Riwayat Reservasi", "📉 Batalkan Reservasi"])

    with tab1:
        res_list = storage.baca_semua_reservasi()
        if not res_list:
            st.info("Belum ada riwayat reservasi.")
            return

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_status = st.selectbox("Filter Status", ["Semua", "Reservasi", "Check-In", "Check-Out", "Batal"])
        with col_f2:
            filter_tipe = st.selectbox("Filter Tipe Kamar", ["Semua", "Standard", "Deluxe", "Suite"])
        with col_f3:
            search_nama = st.text_input("🔍 Cari nama tamu")

        filtered = res_list
        if filter_status != "Semua":
            filtered = [r for r in filtered if r.status == filter_status]
        if filter_tipe != "Semua":
            filtered = [r for r in filtered if r.tipe_kamar == filter_tipe]
        if search_nama:
            filtered = [r for r in filtered if search_nama.lower() in r.nama_tamu.lower()]

        if filtered:
            df = pd.DataFrame([r.to_dict() for r in filtered])
            df = df[["id_reservasi", "nama_tamu", "nomor_kamar", "tipe_kamar",
                      "tanggal_checkin", "tanggal_checkout", "jumlah_malam",
                      "total_biaya", "status", "tanggal_reservasi"]]
            df.columns = ["ID", "Tamu", "Kamar", "Tipe", "Check-In", "Check-Out",
                          "Malam", "Total Biaya", "Status", "Dibuat"]
            df["Total Biaya"] = df["Total Biaya"].apply(lambda x: fmt_rupiah(float(x)))
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Summary metrics
            total_pendapatan = sum(r.total_biaya for r in filtered if r.status == "Check-Out")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Transaksi", len(filtered))
            col2.metric("Sudah Check-Out", sum(1 for r in filtered if r.status == "Check-Out"))
            col3.metric("Sedang Menginap", sum(1 for r in filtered if r.status == "Check-In"))
            col4.metric("Pendapatan (Filter)", fmt_rupiah(total_pendapatan))
        else:
            st.info("Tidak ada data yang sesuai filter.")

    with tab2:
        res_list_batal = [r for r in storage.baca_semua_reservasi() if r.status == "Reservasi"]
        if not res_list_batal:
            st.info("Tidak ada reservasi yang dapat dibatalkan (hanya yang berstatus 'Reservasi').")
        else:
            with st.form("form_batal"):
                st.markdown("#### Batalkan Reservasi")
                res_options = {
                    f"{r.id_reservasi} — {r.nama_tamu} (Kamar {r.nomor_kamar}, {r.tanggal_checkin})": r
                    for r in res_list_batal
                }
                res_pilih = st.selectbox("Pilih Reservasi", list(res_options.keys()))
                alasan = st.text_area("Alasan Pembatalan", placeholder="Masukkan alasan pembatalan...")
                submitted = st.form_submit_button("❌ Batalkan Reservasi", type="primary", use_container_width=True)
                if submitted:
                    res_sel = res_options[res_pilih]
                    success, msg = services.batalkan_reservasi(res_sel.id_reservasi)
                    if success:
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")


# ══════════════════════════════════════════════════════════
#  MAIN APP ROUTER
# ══════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        halaman_login()
        return

    menu = render_sidebar()

    if "Dashboard" in menu:
        halaman_dashboard()
    elif "Kelola Kamar" in menu:
        halaman_kamar()
    elif "Kelola Tamu" in menu:
        halaman_tamu()
    elif "Reservasi Baru" in menu:
        halaman_reservasi()
    elif "Check-In" in menu:
        halaman_checkin()
    elif "Check-Out" in menu:
        halaman_checkout()
    elif "Riwayat" in menu:
        halaman_riwayat()


if __name__ == "__main__":
    main()
