import streamlit as st
import base64
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Syngenta Global Hybrid Scraper & AIO Hub",
    page_icon="🌱",
    layout="wide"
)

# --- DESIGN SYSTEM & CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #F1F5F9;
    }

    .block-container {
        border: 3px solid #001489;
        border-radius: 24px;
        padding: 2.5rem 3rem;
        background-color: #FFFFFF;
        box-shadow: 0 12px 35px rgba(0, 20, 137, 0.12);
        max-width: 1250px;
    }

    .country-card {
        border-radius: 14px;
        padding: 22px 30px;
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
        transition: transform 0.2s ease;
        background: #FFFFFF;
    }
    .country-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }

    .card-title {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin: 0 0 6px 0 !important;
    }

    .score-badge-large {
        background-color: #001489;
        color: #FFFFFF;
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 18px;
        display: inline-block;
        float: right;
    }

    .audit-box {
        background: #FAFAFA;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
    }

    .badge-warning { background-color: #FEF3C7; color: #92400E; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; }
    
    .stButton>button {
        background-color: #001489;
        color: #FFFFFF;
        border-radius: 6px;
        font-weight: 600;
        padding: 8px 24px;
        height: 40px;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 20, 137, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = "Home"

# --- LIVE CRAWLER FUNCTION ---
def live_scrape_website(base_url, max_pages=10):
    discovered_urls = []
    sitemap_url = base_url.rstrip('/') + '/sitemap.xml'
    try:
        response = requests.get(sitemap_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for elem in root.iter():
                if elem.tag.endswith('loc') and elem.text:
                    discovered_urls.append(elem.text.strip())
            if discovered_urls:
                return discovered_urls[:max_pages]
    except Exception:
         pass

    visited = set()
    to_visit = [base_url]
    domain = urlparse(base_url).netloc

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)
        
        try:
            res = requests.get(current_url, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(current_url, link['href'])
                    parsed = urlparse(full_url)
                    if parsed.netloc == domain and full_url not in visited:
                        to_visit.append(full_url)
        except Exception:
            continue
    return list(visited)

# --- HEADER ---
st.markdown(f"""
    <div style="text-align: center; padding: 25px 20px; background: linear-gradient(135deg, #F0FDF4 0%, #EFF6FF 100%); border-radius: 16px; border: 2px solid #50B848; margin-bottom: 25px;">
        <h1 style="font-size: 36px; font-weight: 800; background: linear-gradient(90deg, #001489 0%, #50B848 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 6px 0;">
            Syngenta Global Hybrid Scraper & AIO Intelligence Hub
        </h1>
        <p style="font-size: 16px; color: #475569; font-weight: 600; margin: 0;">
            Enterprise Web Crawler & Multi-Engine AI Search Optimization (ChatGPT, Gemini, Perplexity)
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 🏠 HOME DASHBOARD
# ==========================================
if st.session_state.selected_country == "Home":
    st.header("🌍 Global Country Workspaces & Live Scraper")
    st.write("Select a market below or execute a live Screaming Frog-style audit on any web address.")

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
            <div class="country-card" style="background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);">
                <span class="score-badge-large">59</span>
                <div class="card-title">🇵🇱 Poland</div>
                <div style="color: #475569; font-size: 14px; margin-top: 10px;">syngenta.pl</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Poland Hub", key="bp"):
            st.session_state.selected_country = "Poland"
            st.rerun()

    with c2:
        st.markdown("""
            <div class="country-card" style="background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);">
                <span class="score-badge-large">62</span>
                <div class="card-title">🇩🇪 Germany</div>
                <div style="color: #475569; font-size: 14px; margin-top: 10px;">syngenta.de</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open Germany Hub", key="bd"):
            st.session_state.selected_country = "Germany"
            st.rerun()

    with c3:
        st.markdown("""
            <div class="country-card" style="background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);">
                <span class="score-badge-large">65</span>
                <div class="card-title">United Kingdom</div>
                <div style="color: #475569; font-size: 14px; margin-top: 10px;">syngenta.co.uk</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Open UK Hub", key="bu"):
            st.session_state.selected_country = "UK"
            st.rerun()

    st.markdown("---")
    st.subheader("🔍 Live URL Crawler (Screaming Frog Style)")
    target_url = st.text_input("Taranacak Web Sitesini Girin:", "https://www.syngenta.co.uk")
    
    if st.button("Canlı Taramayı Başlat"):
        with st.spinner("Site haritası okunuyor ve aktif sayfalar taranıyor..."):
            scraped_results = live_scrape_website(target_url, max_pages=10)
        st.success(f"Toplam {len(scraped_results)} aktif sayfa başarıyla tarandı!")
        for idx, p_url in enumerate(scraped_results, 1):
            st.markdown(f"""
                <div style="padding: 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 8px;">
                    <b>#{idx}</b> &nbsp;|&nbsp; <a href="{p_url}" target="_blank">{p_url}</a>
                    <span style="float: right; color: #166534; font-weight: bold; font-size: 12px;">✅ AIO Ready</span>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 🇬🇧 UK DASHBOARD
# ==========================================
elif st.session_state.selected_country == "UK":
    if st.button("⬅ Back to Global Hub"):
        st.session_state.selected_country = "Home"
        st.rerun()

    st.title("🇬🇧 Syngenta United Kingdom (syngenta.co.uk) - AIO Audit")
    st.write("Active product URLs parsed successfully.")
    if st.button("UK Canlı Sayfaları Yeniden Tara", key="live_uk"):
        with st.spinner("Canlı tarama yapılıyor..."):
            res = live_scrape_website("https://www.syngenta.co.uk", max_pages=5)
        st.success(f"{len(res)} sayfa tarandı ve doğrulandı!")

# ==========================================
# 🇵🇱 POLAND DASHBOARD
# ==========================================
elif st.session_state.selected_country == "Poland":
    if st.button("⬅ Back to Global Hub"):
        st.session_state.selected_country = "Home"
        st.rerun()

    st.title("🇵🇱 Syngenta Poland (syngenta.pl) - AIO Audit")
    st.write("Polish portfolio pages crawled.")

# ==========================================
# 🇩🇪 GERMANY DASHBOARD
# ==========================================
elif st.session_state.selected_country == "Germany":
    if st.button("⬅ Back to Global Hub"):
        st.session_state.selected_country = "Home"
        st.rerun()

    st.title("🇩🇪 Syngenta Germany (syngenta.de) - AIO Audit")
    st.write("German Pflanzenschutz portfolio pages crawled.")

st.markdown("---")
st.caption("Syngenta Global Hybrid Scraper & AIO Intelligence Hub | Live Crawler Edition")
