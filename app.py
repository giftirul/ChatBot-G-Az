import streamlit as st
import google.generativeai as genai

# Konfigurasi halaman
st.set_page_config(
    page_title="Chat G-Az",
    page_icon="gaz.png",
    layout="centered"
)

# --- Sidebar dengan Navigasi dan Info ---
with st.sidebar:
    st.markdown("---")
    menu = st.radio("Pilih Menu:", ["About Us","Chat", "PDF","Contact Us"], index=1)
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>Copyright © 2025 Giftirul Aziz. All Rights Reserved.</p>", unsafe_allow_html=True)

# --- Header Utama ---
st.markdown("<h1 style='text-align: center;color: blue'>🤖<br> Chat G-Az</h1>", unsafe_allow_html=True)

# --- Konfigurasi API Gemini ---
try:
    genai.configure(api_key=st.secrets["gemini_api_key"])
except KeyError:
    st.error("Kunci API Gemini tidak ditemukan. Pastikan sudah diatur di .streamlit/secrets.toml")
    st.stop()

# Inisialisasi model
model = genai.GenerativeModel('gemini-2.0-flash')

# --- Inisialisasi Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_history" not in st.session_state:
    st.session_state.pdf_history = []

# ===========================
# ✨ MENU: ABOUT US
# ===========================
if menu == "About Us":
    st.markdown("## ✨ Tentang Chat G-Az")
    st.markdown(
        """
        Chat G-Az adalah aplikasi chatbot berbasis AI yang dirancang untuk membantu pengguna dalam menganalisis dokumen, menjawab pertanyaan, dan berinteraksi secara cerdas dan ramah.

        Dibangun menggunakan **Streamlit** dan **Google Gemini**, aplikasi ini menggabungkan kekuatan teknologi dengan sentuhan desain yang hangat dan intuitif. Tujuannya bukan hanya memberikan jawaban, tapi juga menciptakan pengalaman yang menyenangkan dan bermanfaat.

        **Filosofi kami:**  
        > *"AI bukan sekadar alat, tapi sahabat belajar yang bisa dipercaya."*

        Aplikasi ini dikembangkan oleh **Giftirul Aziz**, seorang kreator yang memadukan logika teknis dengan kepekaan visual dan etika. Setiap fitur dirancang dengan perhatian terhadap detail, kenyamanan pengguna, dan nilai-nilai transparansi.

        Versi saat ini masih dalam tahap eksplorasi dan pengembangan. Kami terbuka untuk masukan, kolaborasi, dan ide-ide baru!
        """
    )


# ===========================
# ✨ MENU: CHAT
# ===========================
elif menu == "Chat":
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Apa yang bisa saya bantu?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = model.generate_content(prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# ===========================
# ✨ MENU: PDF
# ===========================
elif menu == "PDF":
    st.subheader("📄 Analisis Dokumen PDF")
    uploaded_file = st.file_uploader("Unggah file PDF untuk dianalisis", type=["pdf"])

    if uploaded_file:
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()

            st.success("✅ File berhasil dibaca.")
            st.text_area("Isi PDF:", value=text, height=300)

            if st.button("Analisis PDF"):
                response = model.generate_content(f"Berikan ringkasan dan insight dari dokumen berikut:\n{text}")
                st.markdown("### 💡 Insight dari Gemini")
                st.markdown(response.text)

                # Simpan ke histori PDF
                st.session_state.pdf_history.append({
                    "filename": uploaded_file.name,
                    "content": text,
                    "analysis": response.text
                })

        except ImportError:
            st.error("Modul PyMuPDF belum terinstal. Jalankan `pip install PyMuPDF` di terminal.")
        except Exception as e:
            st.error(f"Gagal membaca PDF: {e}")

    # Tampilkan histori PDF sebelumnya
    if st.session_state.pdf_history:
        st.markdown("## 📚 Histori Analisis PDF Sebelumnya")
        for i, item in enumerate(st.session_state.pdf_history):
            with st.expander(f"{i+1}. {item['filename']}"):
                st.markdown("**Isi Dokumen:**")
                st.text_area("Teks", value=item["content"], height=150)
                st.markdown("**Hasil Analisis:**")
                st.markdown(item["analysis"])

# ===========================
# ✨ MENU: CONTACT US
# ===========================
elif menu == "Contact Us":
    st.markdown("## 📬 Hubungi Kami")
    st.markdown(
        """
        Kami senang mendengar dari Anda! Jika ada pertanyaan, saran, atau ingin berkolaborasi, silakan hubungi kami melalui salah satu cara berikut:

        - 📧 **Email:** giftirul.aziz@gmail.com  
        - 🌐 **Website:** [www.chatgaz.id](https://www.chatgaz.id)  
        - 🐦 **Twitter/X:** [@giftirulaziz](https://twitter.com/giftirulaziz)  
        - 💼 **LinkedIn:** [Giftirul Aziz](https://www.linkedin.com/in/giftirul-aziz-st-b176135b/)

        Atau, kirim pesan langsung melalui formulir di bawah ini:
        """
    )

    # Formulir sederhana
    with st.form("contact_form"):
        name = st.text_input("Nama")
        email = st.text_input("Email")
        message = st.text_area("Pesan Anda")
        submitted = st.form_submit_button("Kirim")

        if submitted:
            st.success("✅ Terima kasih! Pesan Anda telah dikirim.")
