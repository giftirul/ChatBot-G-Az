import streamlit as st
import google.generativeai as genai

# Konfigurasi halaman dan judul
st.set_page_config(
    page_title="Chat G-Az", 
    page_icon="gaz.png", 
    layout="centered"
)

# --- Tambahkan Sidebar ---
with st.sidebar:
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Tentang Aplikasi</h3>", unsafe_allow_html=True)
    st.markdown(
    """
    <div style='text-align: center; color: #000000; background-color: #E8F7FF; border: 1px solid #BEE5EB; padding: 10px; border-radius: 5px;'>
    Aplikasi chatbot ini dibuat menggunakan Streamlit dan Google Gemini. Ini adalah contoh sederhana untuk demonstrasi.
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>Copyright © 2025 Giftirul Aziz. All Rights Reserved.</p>", unsafe_allow_html=True)

# --------------------------

st.markdown("<h1 style='text-align: center;color: blue'>🤖<br> Chat G-Az</h1>", unsafe_allow_html=True)


# Dapatkan kunci API dari file secrets
try:
    genai.configure(api_key=st.secrets["gemini_api_key"])
except KeyError:
    st.error("Kunci API Gemini tidak ditemukan. Pastikan sudah diatur di .streamlit/secrets.toml")
    st.stop()

# Inisialisasi model
model = genai.GenerativeModel('gemini-2.0-flash')

# Gunakan st.session_state untuk menyimpan riwayat chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tampilkan riwayat chat dari sesi
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Tangani input dari pengguna
if prompt := st.chat_input("Apa yang bisa saya bantu?"):
    # Tambahkan pesan pengguna ke riwayat
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kirim prompt ke Gemini dan dapatkan respons
    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        # Tambahkan respons asisten ke riwayat
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

   