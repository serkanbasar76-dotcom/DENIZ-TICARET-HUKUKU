import streamlit as st
import random
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Deniz Ticaret Hukuku Sınavı", page_icon="⚖️", layout="centered")

# --- GELİŞMİŞ CSS (PROFESYONEL UI) ---
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem; padding-bottom: 0rem; max-width: 800px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    .main-header { font-size: 24px !important; font-weight: 800; color: #FFFFFF; text-align: center; margin-bottom: 0px; }
    .serkan-hoca { font-size: 16px !important; font-weight: 600; color: #58a6ff; text-align: center; margin-top: -5px; margin-bottom: 10px; }
    
    /* ANALİZ SAYFASI ÖZEL TASARIM */
    .result-container {
        text-align: center;
        padding: 20px 0;
        margin-top: 10px;
    }
    .big-result {
        font-size: 85px !important; 
        font-weight: 900;
        color: #58a6ff;
        text-transform: uppercase;
        line-height: 1.1;
    }
    .stats-container {
        text-align: center;
        font-size: 22px;
        color: #ffffff;
        margin: 20px auto;
        background: #161B22;
        padding: 15px;
        border-radius: 12px;
        max-width: 500px;
    }
    .stat-correct { color: #238636; font-weight: bold; }
    .stat-wrong { color: #da3633; font-weight: bold; }

    .question-box {
        background-color: #161B22;
        padding: 12px 18px;
        border-radius: 8px;
        border-left: 5px solid #58a6ff;
        font-size: 15px;
        line-height: 1.4;
        margin-bottom: 10px;
    }

    /* Şık Butonları */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        border: 1px solid #3060d0;
        background-color: #1c2128;
        color: #FFFFFF;
        padding: 7px 12px;
        font-size: 14px;
        text-align: left;
        margin-bottom: -12px;
    }
    .stButton>button:hover { background-color: #3060d0; border-color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- YENİ VERİ SETİ (DENİZ TİCARET HUKUKU) ---
RAW_DATA = [
    {"q": "Yolcu, bilette belirtilen geminin kalkmasından önce veya yolculuk sırasında ölürse yahut yolculuğa devam etmesine engel olan bir hastalık veya diğer bir zorunlayıcı sebep ortaya çıkarsa bilet ücretinin yarısı ödenir. Bu hükme göre hangisi yanlıştır? [cite: 339, 340]", "a": "Bu hüküm sadece yolcu gemileri için geçerlidir [cite: 342, 343]", "options": ["Bilet ücretinin tamamı ödenmişse yarısı iade edilir [cite: 341]", "Bilet ücreti hiç ödenmemişse yarısı talep edilir [cite: 341]", "Bu hüküm sadece yolcu gemileri için geçerlidir [cite: 342]", "Zorunlayıcı sebep objektif bir imkansızlık olmalıdır [cite: 342]"]},
    {"q": "Gemi kira sözleşmesinde aksi kararlaştırılmamışsa, geminin sigorta ettirilmesi yükümlülüğü kime aittir? [cite: 346]", "a": "Gemi malikine [cite: 347, 348]", "options": ["Kiracıya [cite: 347]", "Gemi malikine [cite: 347]", "Gemi işletme müteahhidine [cite: 347]", "Kaptana [cite: 347]"]},
    {"q": "Konişmento neyi temsil eder? [cite: 350]", "a": "Eşyanın gemiye alındığını veya yüklendiğini [cite: 351, 352]", "options": ["Sadece bir taşıma sözleşmesini [cite: 351]", "Eşyanın gemiye alındığını veya yüklendiğini [cite: 351]", "Geminin denize elverişli olduğunu [cite: 351]", "Navlun miktarının ödendiğini [cite: 351]"]},
    {"q": "Aşağıdakilerden hangisi navlun sözleşmesinin türlerinden biri değildir? [cite: 354]", "a": "Gemi kira sözleşmesi [cite: 355, 356]", "options": ["Zaman üzerine navlun sözleşmesi [cite: 355]", "Yol üzerine navlun sözleşmesi [cite: 355]", "Miktar üzerine navlun sözleşmesi [cite: 355]", "Gemi kira sözleşmesi [cite: 355]"]},
    {"q": "Türk Ticaret Kanunu’na göre, kaptanın gemideki temsil yetkisi ne zaman başlar? [cite: 359]", "a": "Göreve başladığı andan itibaren [cite: 360, 361]", "options": ["Gemi sefere çıktığında [cite: 360]", "Donatan ile sözleşme imzaladığında [cite: 360]", "Göreve başladığı andan itibaren [cite: 360]", "Gemi limandan ayrıldığında [cite: 360]"]},
    {"q": "Müşterek avarya nedir? [cite: 363]", "a": "Gemiyi ve yükü ortak bir tehlikeden kurtarmak için yapılan olağanüstü fedakarlıktır [cite: 366, 368]", "options": ["Geminin tek taraflı uğradığı zarardır [cite: 364]", "Deniz kazası sonrası oluşan tüm zararların donatan tarafından karşılanmasıdır [cite: 365]", "Gemiyi ve yükü ortak bir tehlikeden kurtarmak için yapılan olağanüstü fedakarlıktır [cite: 366]", "Navlun ücretinin ödenmemesidir [cite: 367]"]},
    {"q": "Kaptanın deniz raporunu (Sea Protest) sunması için yasal süre nedir? [cite: 370]", "a": "Varıştan itibaren 24 saat [cite: 371, 375]", "options": ["Varıştan itibaren 24 saat [cite: 371]", "Varıştan itibaren 48 saat [cite: 372]", "Varıştan itibaren 1 hafta [cite: 373]", "Olay anından itibaren 24 saat [cite: 374]"]},
    {"q": "Aşağıdakilerden hangisi geminin sicilden silinmesini gerektiren hallerden biri değildir? [cite: 377]", "a": "Geminin adının değiştirilmesi [cite: 380, 382]", "options": ["Geminin tamir kabul etmez hale gelmesi [cite: 378]", "Geminin Türk bayrağı çekme hakkını kaybetmesi [cite: 379]", "Geminin adının değiştirilmesi [cite: 380]", "Geminin kurtarılamayacak şekilde batması [cite: 381]"]},
    {"q": "Çatışma (Kaza) durumunda zaman aşımı süresi ne kadardır? [cite: 384]", "a": "2 yıl [cite: 386, 389]", "options": ["1 yıl [cite: 385]", "2 yıl [cite: 386]", "5 yıl [cite: 387]", "10 yıl [cite: 388]"]},
    {"q": "Free In and Out (FIO) terimi neyi ifade eder? [cite: 391]", "a": "Navluna yükleme ve boşaltma giderlerinin dahil olmadığını [cite: 392, 396]", "options": ["Navluna yükleme ve boşaltma giderlerinin dahil olmadığını [cite: 392]", "Navluna her şeyin dahil olduğunu [cite: 393]", "Geminin yakıt giderlerini [cite: 394]", "Liman vergilerini [cite: 395]"]},
    {"q": "Kaptanın donatanın talimatı dışında yaptığı işlemlerden dolayı kim sorumludur? [cite: 398]", "a": "Sadece kaptan [cite: 399, 403]", "options": ["Sadece kaptan [cite: 399]", "Sadece donatan [cite: 400]", "Kaptan ve donatan müteselsilen [cite: 401]", "Gemi işletme müteahhidi [cite: 402]"]},
    {"q": "Donatanın sınırlı sorumluluğu hangi durumlarda söz konusudur? [cite: 405]", "a": "Kaptanın kusurunda [cite: 406, 410]", "options": ["Kaptanın kusurunda [cite: 406]", "Donatanın kendi kusurunda [cite: 407]", "Geminin denize elverişsizliğinde [cite: 408]", "Yakıt borçlarında [cite: 409]"]},
    {"q": "Kırkambar sözleşmesi nedir? [cite: 412]", "a": "Belirli bir malın taşınması için geminin bir kısmının tahsis edildiği sözleşmedir [cite: 414, 417]", "options": ["Geminin tamamının tahsis edildiği sözleşmedir [cite: 413]", "Belirli bir malın taşınması için geminin bir kısmının tahsis edildiği sözleşmedir [cite: 414]", "Geminin zaman esaslı kiralanmasıdır [cite: 415]", "Sadece dökme yük taşıma sözleşmesidir [cite: 416]"]},
    {"q": "Dispeççi kimdir? [cite: 419]", "a": "Müşterek avarya hesaplarını yapan uzmandır [cite: 422, 424]", "options": ["Gemi acentesidir [cite: 420]", "Navlun hesaplayan kişidir [cite: 421]", "Müşterek avarya hesaplarını yapan uzmandır [cite: 422]", "Liman başkanı [cite: 423]"]},
    {"q": "Donatanın yük üzerindeki hapis hakkı ne zaman sona erer? [cite: 426]", "a": "Yük alıcıya teslim edildiğinde [cite: 428, 431]", "options": ["Yük gemiye yüklendiğinde [cite: 427]", "Yük alıcıya teslim edildiğinde [cite: 428]", "Konişmento düzenlendiğinde [cite: 429]", "Gemi kalktığında [cite: 430]"]},
    {"q": "Zaman çarteri sözleşmesinde yakıt giderleri kime aittir? [cite: 433]", "a": "Tahsis olunana (Kiracıya) [cite: 437, 438]", "options": ["Donatana [cite: 434]", "Kaptana [cite: 435]", "Tahsis edene [cite: 436]", "Tahsis olunana (Kiracıya) [cite: 437]"]},
    {"q": "Teyitli konişmento neyi ifade eder? [cite: 440]", "a": "Malların gemiye yüklendiğini [cite: 441, 445]", "options": ["Malların gemiye yüklendiğini [cite: 441]", "Malların sadece teslim alındığını [cite: 442]", "Navlunun ödendiğini [cite: 443]", "Geminin yola çıktığını [cite: 444]"]},
    {"q": "Aşağıdakilerden hangisi gemi adamı değildir? [cite: 447]", "a": "Kılavuz kaptan [cite: 451, 452]", "options": ["Kaptan [cite: 448]", "Çarkçıbaşı [cite: 449]", "Stajyer [cite: 450]", "Kılavuz kaptan [cite: 451]"]},
    {"q": "Navlun borçlusu kimdir? [cite: 454]", "a": "Kural olarak taşıtan, ancak konişmentoya göre gönderilen de olabilir [cite: 457, 459]", "options": ["Sadece taşıtan [cite: 455]", "Sadece gönderilen [cite: 456]", "Kural olarak taşıtan, ancak konişmentoya göre gönderilen de olabilir [cite: 457]", "Gemi acentesi [cite: 458]"]},
    {"q": "Geminin 'denize elverişli' olması ne demektir? [cite: 461]", "a": "Geminin teknik, personel ve donanım olarak yolculuğu tamamlayabilecek durumda olması [cite: 463, 466]", "options": ["Geminin sadece yüzebilmesi [cite: 462]", "Geminin teknik, personel ve donanım olarak yolculuğu tamamlayabilecek durumda olması [cite: 463]", "Geminin temiz olması [cite: 464]", "Geminin sigortalı olması [cite: 465]"]}
]

# --- SİSTEM BAŞLATMA ---
def init_quiz():
    # Soruları karıştırıyoruz
    shuffled = random.sample(RAW_DATA, len(RAW_DATA))
    quiz = []
    for item in shuffled:
        correct = item["a"]
        options = item["options"]
        random.shuffle(options) # Şıkları karıştırıyoruz
        item_copy = item.copy()
        item_copy["options"] = options
        quiz.append(item_copy)
    return quiz

if 'quiz' not in st.session_state:
    st.session_state.quiz = init_quiz()
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

    st.divider()
    if st.button("🏠 Sınavı Sıfırla"):
        st.session_state.clear()
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

    st.markdown(f"""
    <div class="result-container">
        <div class="big-result">%{score:.1f} <span style="color:{status_color};">{status_text}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="stats-container">
        ⏱ {m} dk {s} sn &nbsp; | &nbsp; 
        <span class="stat-correct">DOĞRU: {corrects}</span> &nbsp; | &nbsp; 
        <span class="stat-wrong">YANLIŞ: {wrongs}</span>
    </div>
    """, unsafe_allow_html=True)
    
    if score >= 80: st.balloons()

    st.subheader("Hatalı Sorular")
    has_errors = False
    for r in st.session_state.results:
        if r["u"] != r["c"]:
            has_errors = True
            with st.expander(f"Soru {r['n']} - İncele"):
                st.write(f"**Soru:** {r['q']}")
                st.error(f"Senin Cevabın: {r['u']}")
                st.success(f"Doğru Cevap: {r['c']}")
    
    if not has_errors:
        st.success("Tebrikler! Hiç hata yapmadınız.")
                
    if st.button("Sınava Yeniden Başla", use_container_width=True):
        st.session_state.clear()
        st.rerun()