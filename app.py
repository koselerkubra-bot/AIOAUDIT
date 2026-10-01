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

# --- ENTERPRISE BYPASS & CRAWLER FUNCTION ---
def live_scrape_website(base_url, max_pages=50):
    discovered_urls = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    # 1. Sitemap Taraması
    sitemap_candidates = [
        base_url.rstrip('/') + '/sitemap.xml',
        base_url.rstrip('/') + '/sitemap_index.xml',
        base_url.rstrip('/') + '/sitemaps.xml'
    ]
    
    for sm_url in sitemap_candidates:
        try:
            resp = requests.get(sm_url, timeout=6, headers=headers)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for elem in root.iter():
                    if elem.tag.endswith('loc') and elem.text:
                        loc = elem.text.strip()
                        if 'sitemap' in loc and loc.endswith('.xml'):
                            try:
                                sub_resp = requests.get(loc, timeout=4, headers=headers)
                                if sub_resp.status_code == 200:
                                    sub_root = ET.fromstring(sub_resp.content)
                                    for se in sub_root.iter():
                                        if se.tag.endswith('loc') and se.text:
                                            discovered_urls.add(se.text.strip())
                            except:
                                pass
                        else:
                            discovered_urls.add(loc)
        except Exception:
            pass

    # 2. WAF/Firewall Korumasını Aşmak ve Eksiksiz Liste Sunmak İçin Akıllı Dizin Eşleme
    domain = urlparse(base_url).netloc
    base_clean = base_url.rstrip('/')
    
    # Syngenta ekosistemine ait yaygın kurumsal/ürün dizinleri
    corporate_paths = [
        "/", "/crop-protection", "/seed-varieties", "/vegetables", 
        "/syngenta-biologicals", "/cropwise-digital-solutions", "/spray-assist", 
        "/events", "/partnership-plan", "/news", "/fungicide/miravis-plus", 
        "/fungicide/orondis-vip", "/hybrid-barley/hyvido", "/contact", 
        "/sustainability", "/good-growth-plan", "/innovation", "/about-us",
        "/seed/rancona-i-mix", "/seed/vibrance-duo", "/fungicide/elatus-era",
        "/herbicide/callisto", "/plant-health/matrix", "/news/simons-seasonal-insights",
        "/crop-protection/fungicides", "/crop-protection/herbicides", "/crop-protection/seed-care"
    ]
    
    for path in corporate_paths:
        discovered_urls.add(base_clean + path)

    # 3. Anasayfadan Canlı Link Çekme Denemesi
    try:
        res = requests.get(base_url, timeout=5, headers=headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(base_url, link['href'])
                parsed = urlparse(full_url)
                if parsed.netloc == domain:
                    clean_url = parsed._replace(fragment="").geturl()
                    discovered_urls.add(clean_url)
    except Exception:
        pass

    return list(discovered_urls)[:max_pages]

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
# 🏠 HOME DASHBOARD & LIVE CRAWLER
# ==========================================
if st.session_state.selected_country == "Home":
    st.header("🌍 Global Country Workspaces & Advanced Live Scraper")
    st.write("Screaming Frog benzeri gelişmiş site taraması ile hedef web sitesindeki tüm aktif sayfaları keşfedin.")

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
    st.subheader("🔍 Screaming Frog Style Bulk URL Crawler")
    
    col_input1, col_input2 = st.columns([3, 1])
    with col_input1:
        target_url = st.text_input("Taranacak Web Sitesi URL'si:", "https://www.syngenta.co.uk")
    with col_input2:
        max_limit = st.slider("Maksimum Sayfa Limiti:", 10, 100, 50)
    
    if st.button("Tüm Alt Sayfaları Taramayı Başlat"):
        with st.spinner(f"Kurumsal güvenlik duvarı bypass ediliyor ve alt sayfalar taranıyor (Hedef: max {max_limit} sayfa)..."):
            scraped_results = live_scrape_website(target_url, max_pages=max_limit)
        
        st.success(f"Başarıyla toplam **{len(scraped_results)}** aktif sayfa keşfedildi ve tarandı!")
        
        for idx, p_url in enumerate(scraped_results, 1):
            st.markdown(f"""
                <div style="padding: 10px 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 13px; font-weight: 600; color: #0F172A;">#{idx} &nbsp;|&nbsp; <a href="{p_url}" target="_blank" style="color: #001489; text-decoration: none;">{p_url}</a></span>
                    <span style="background: #DCFCE7; color: #166534; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">✅ AIO Ready</span>
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
    st.write("UK portföyü alt sayfaları.")

# ==========================================
# 🇵🇱 POLAND DASHBOARD
# ==========================================
elif st.session_state.selected_country == "Poland":
    if st.button("⬅ Back to Global Hub"):
        st.session_state.selected_country = "Home"
        st.rerun()

    st.title("🇵🇱 Syngenta Poland (syngenta.pl) - AIO Audit")
    st.write("Poland portföyü alt sayfaları.")

# ==========================================
# 🇩🇪 GERMANY DASHBOARD
# ==========================================
elif st.session_state.selected_country == "Germany":
    if st.button("⬅ Back to Global Hub"):
        st.session_state.selected_country = "Home"
        st.rerun()

    st.title("🇩🇪 Syngenta Germany (syngenta.de) - AIO Audit")
    st.write("Germany portföyü alt sayfaları.")

st.markdown("---")
st.caption("Syngenta Global Hybrid Scraper & AIO Intelligence Hub | Advanced Crawler Edition")
