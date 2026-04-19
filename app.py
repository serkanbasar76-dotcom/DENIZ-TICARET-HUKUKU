import streamlit as st
import random
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Deniz Ticaret Hukuku Sınavı", page_icon="⚖️", layout="centered")

# --- GELİŞMİŞ CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem; padding-bottom: 0rem; max-width: 800px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    .main-header { font-size: 24px !important; font-weight: 800; color: #FFFFFF; text-align: center; margin-bottom: 0px; }
    .serkan-hoca { font-size: 16px !important; font-weight: 600; color: #58a6ff; text-align: center; margin-top: -5px; margin-bottom: 10px; }
    
    .result-container { text-align: center; padding: 20px 0; margin-top: 10px; }
    .big-result { font-size: 85px !important; font-weight: 900; color: #58a6ff; text-transform: uppercase; line-height: 1.1; }
    
    .stats-container {
        text-align: center; font-size: 22px; color: #ffffff; margin: 20px auto;
        background: #161B22; padding: 15px; border-radius: 12px; max-width: 500px;
    }
    .stat-correct { color: #238636; font-weight: bold; }
    .stat-wrong { color: #da3633; font-weight: bold; }

    .question-box {
        background-color: #161B22; padding: 12px 18px; border-radius: 8px;
        border-left: 5px solid #58a6ff; font-size: 15px; line-height: 1.4; margin-bottom: 10px;
    }

    .stButton>button {
        width: 100%; border-radius: 5px; border: 1px solid #3060d0;
        background-color: #1c2128; color: #FFFFFF; padding: 7px 12px;
        font-size: 14px; text-align: left; margin-bottom: -12px;
    }
    .stButton>button:hover { background-color: #3060d0; border-color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ (BELGEDEKİ TÜM SORULAR) ---
RAW_DATA = [
    {"q": "Yolcu, bilette belirtilen geminin kalkmasından önce veya yolculuk sırasında ölürse yahut yolculuğa devam etmesine engel olan bir hastalık veya diğer bir zorunlayıcı sebep ortaya çıkarsa bilet ücretinin yarısı ödenir. Bu hükme göre hangisi yanlıştır?", "a": "Bu hüküm sadece yolcu gemileri için geçerlidir", "options": ["Bilet ücretinin tamamı ödenmişse yarısı iade edilir", "Bilet ücreti hiç ödenmemişse yarısı talep edilir", "Bu hüküm sadece yolcu gemileri için geçerlidir", "Zorunlayıcı sebep objektif bir imkansızlık olmalıdır"]},
    {"q": "Gemi kira sözleşmesinde aksi kararlaştırılmamışsa, geminin sigorta ettirilmesi yükümlülüğü kime aittir?", "a": "Gemi malikine", "options": ["Kiracıya", "Gemi malikine", "Gemi işletme müteahhidine", "Kaptana"]},
    {"q": "Konişmento neyi temsil eder?", "a": "Eşyanın gemiye alındığını veya yüklendiğini", "options": ["Sadece bir taşıma sözleşmesini", "Eşyanın gemiye alındığını veya yüklendiğini", "Geminin denize elverişli olduğunu", "Navlun miktarının ödendiğini"]},
    {"q": "Aşağıdakilerden hangisi navlun sözleşmesinin türlerinden biri değildir?", "a": "Gemi kira sözleşmesi", "options": ["Zaman üzerine navlun sözleşmesi", "Yol üzerine navlun sözleşmesi", "Miktar üzerine navlun sözleşmesi", "Gemi kira sözleşmesi"]},
    {"q": "Türk Ticaret Kanunu’na göre, kaptanın gemideki temsil yetkisi ne zaman başlar?", "a": "Göreve başladığı andan itibaren", "options": ["Gemi sefere çıktığında", "Donatan ile sözleşme imzaladığında", "Göreve başladığı andan itibaren", "Gemi limandan ayrıldığında"]},
    {"q": "Müşterek avarya nedir?", "a": "Gemiyi ve yükü ortak bir tehlikeden kurtarmak için yapılan olağanüstü fedakarlıktır", "options": ["Geminin tek taraflı uğradığı zarardır", "Deniz kazası sonrası oluşan tüm zararların donatan tarafından karşılanmasıdır", "Gemiyi ve yükü ortak bir tehlikeden kurtarmak için yapılan olağanüstü fedakarlıktır", "Navlun ücretinin ödenmemesidir"]},
    {"q": "Kaptanın deniz raporunu (Sea Protest) sunması için yasal süre nedir?", "a": "Varıştan itibaren 24 saat", "options": ["Varıştan itibaren 24 saat", "Varıştan itibaren 48 saat", "Varıştan itibaren 1 hafta", "Olay anından itibaren 24 saat"]},
    {"q": "Aşağıdakilerden hangisi geminin sicilden silinmesini gerektiren hallerden biri değildir?", "a": "Geminin adının değiştirilmesi", "options": ["Geminin tamir kabul etmez hale gelmesi", "Geminin Türk bayrağı çekme hakkını kaybetmesi", "Geminin adının değiştirilmesi", "Geminin kurtarılamayacak şekilde batması"]},
    {"q": "Çatışma (Kaza) durumunda zaman aşımı süresi ne kadardır?", "a": "2 yıl", "options": ["1 yıl", "2 yıl", "5 yıl", "10 yıl"]},
    {"q": "Free In and Out (FIO) terimi neyi ifade eder?", "a": "Navluna yükleme ve boşaltma giderlerinin dahil olmadığını", "options": ["Navluna yükleme ve boşaltma giderlerinin dahil olmadığını", "Navluna her şeyin dahil olduğunu", "Geminin yakıt giderlerini", "Liman vergilerini"]},
    {"q": "Kaptanın donatanın talimatı dışında yaptığı işlemlerden dolayı kim sorumludur?", "a": "Sadece kaptan", "options": ["Sadece kaptan", "Sadece donatan", "Kaptan ve donatan müteselsilen", "Gemi işletme müteahhidi"]},
    {"q": "Donatanın sınırlı sorumluluğu hangi durumlarda söz konusudur?", "a": "Kaptanın kusurunda", "options": ["Kaptanın kusurunda", "Donatanın kendi kusurunda", "Geminin denize elverişsizliğinde", "Yakıt borçlarında"]},
    {"q": "Kırkambar sözleşmesi nedir?", "a": "Belirli bir malın taşınması için geminin bir kısmının tahsis edildiği sözleşmedir", "options": ["Geminin tamamının tahsis edildiği sözleşmedir", "Belirli bir malın taşınması için geminin bir kısmının tahsis edildiği sözleşmedir", "Geminin zaman esaslı kiralanmasıdır", "Sadece dökme yük taşıma sözleşmesidir"]},
    {"q": "Dispeççi kimdir?", "a": "Müşterek avarya hesaplarını yapan uzmandır", "options": ["Gemi acentesidir", "Navlun hesaplayan kişidir", "Müşterek avarya hesaplarını yapan uzmandır", "Liman başkanı"]},
    {"q": "Donatanın yük üzerindeki hapis hakkı ne zaman sona erer?", "a": "Yük alıcıya teslim edildiğinde", "options": ["Yük gemiye yüklendiğinde", "Yük alıcıya teslim edildiğinde", "Konişmento düzenlendiğinde", "Gemi kalktığında"]},
    {"q": "Zaman çarteri sözleşmesinde yakıt giderleri kime aittir?", "a": "Tahsis olunana (Kiracıya)", "options": ["Donatana", "Kaptana", "Tahsis edene", "Tahsis olunana (Kiracıya)"]},
    {"q": "Teyitli konişmento neyi ifade eder?", "a": "Malların gemiye yüklendiğini", "options": ["Malların gemiye yüklendiğini", "Malların sadece teslim alındığını", "Navlunun ödendiğini", "Geminin yola çıktığını"]},
    {"q": "Aşağıdakilerden hangisi gemi adamı değildir?", "a": "Kılavuz kaptan", "options": ["Kaptan", "Çarkçıbaşı", "Stajyer", "Kılavuz kaptan"]},
    {"q": "Navlun borçlusu kimdir?", "a": "Kural olarak taşıtan, ancak konişmentoya göre gönderilen de olabilir", "options": ["Sadece taşıtan", "Sadece gönderilen", "Kural olarak taşıtan, ancak konişmentoya göre gönderilen de olabilir", "Gemi acentesi"]},
    {"q": "Geminin 'denize elverişli' olması ne demektir?", "a": "Geminin teknik, personel ve donanım olarak yolculuğu tamamlayabilecek durumda olması", "options": ["Geminin sadece yüzebilmesi", "Geminin teknik, personel ve donanım olarak yolculuğu tamamlayabilecek durumda olması", "Geminin temiz olması", "Geminin sigortalı olması"]}
]

# --- SİSTEM BAŞLATMA ---
if 'quiz' not in st.session_state:
    shuffled = random.sample(RAW_DATA, len(RAW_DATA))
    st.session_state.quiz = shuffled
    st.session_state.idx = 0
    st.session_state.results = []
    st.session_state.done = False
    st.session_state.start_time = time.time()

# --- ARA YÜZ ---
st.markdown('<p class="main-header">DENİZ TİCARET HUKUKU SORULARI</p>', unsafe_allow_html=True)
st.markdown('<p class="serkan-hoca">⚓ SERKAN HOCA İLE</p>', unsafe_allow_html=True)

if not st.session_state.done:
    st.markdown(f'<p style="text-align:center; color:#8b949e; font-size:14px;">SORU {st.session_state.idx + 1} / {len(st.session_state.quiz)}</p>', unsafe_allow_html=True)
    curr = st.session_state.quiz[st.session_state.idx]
    st.markdown(f'<div class="question-box">{curr["q"]}</div>', unsafe_allow_html=True)

    letters = ["A", "B", "C", "D"]
    for i, opt in enumerate(curr["options"]):
        if st.button(f"{letters[i]}) {opt}", key=f"q_{st.session_state.idx}_{i}"):
            st.session_state.results.append({"n": st.session_state.idx + 1, "q": curr["q"], "u": opt, "c": curr["a"]})
            if st.session_state.idx + 1 < len(st.session_state.quiz):
                st.session_state.idx += 1
                st.rerun()
            else:
                st.session_state.end_time = time.time()
                st.session_state.done = True
                st.rerun()
else:
    # --- ANALİZ SAYFASI ---
    elapsed = st.session_state.end_time - st.session_state.start_time
    m, s = int(elapsed // 60), int(elapsed % 60)
    corrects = sum(1 for r in st.session_state.results if r["u"] == r["c"])
    wrongs = len(st.session_state.quiz) - corrects
    score = (corrects / len(st.session_state.quiz)) * 100
    
    status_text = "BAŞARILI" if score >= 80 else "GELİŞTİRİLMELİ"
    status_color = "#238636" if score >= 80 else "#da3633"

    st.markdown(f'<div class="result-container"><div class="big-result">%{score:.1f} <span style="color:{status_color};">{status_text}</span></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stats-container">⏱ {m} dk {s} sn &nbsp; | &nbsp; <span class="stat-correct">DOĞRU: {corrects}</span> &nbsp; | &nbsp; <span class="stat-wrong">YANLIŞ: {wrongs}</span></div>', unsafe_allow_html=True)
    
    if score >= 80: st.balloons()
    st.subheader("Hatalı Sorular")
    for r in st.session_state.results:
        if r["u"] != r["c"]:
            with st.expander(f"Soru {r['n']} - Hata"):
                st.write(f"**Soru:** {r['q']}")
                st.error(f"Senin Cevabın: {r['u']}")
                st.success(f"Doğru Cevap: {r['c']}")
                
    if st.button("Sınava Yeniden Başla", use_container_width=True):
        st.session_state.clear()
        st.rerun()
