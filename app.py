import streamlit as st
import requests

# Konfigurasi Halaman
st.set_page_config(page_title="Ringkas.in - Prototipe API", page_icon="📝")

# --- KONFIGURASI API ---
API_URL = "https://api-inference.huggingface.co/models/cahya/bert2bert-indonesian-summarization"

# PERUBAHAN: Cara ambil token khusus untuk Streamlit Cloud
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    HF_TOKEN = None

# PERUBAHAN: Fungsi ini diperkuat biar nggak crash kalau server HF error
def query_hf_api(payload):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    try:
        return response.json()
    except Exception:
        # Kalau balasan HF bukan JSON, tangkap pesan aslinya
        return {"error": f"HTTP {response.status_code}: {response.text}"}

# --- TAMPILAN UTAMA ---
st.title("📝 Ringkas.in")
st.subheader("Prototipe Peringkas Teks Otomatis (Microservices API)")
st.markdown("---")

# Input Teks
article_input = st.text_area("Tempelkan Artikel Berita di Sini:", height=300, 
                             placeholder="Masukkan teks berita bahasa Indonesia yang ingin diringkas...")

if st.button("Generate Ringkasan"):
    if not HF_TOKEN:
        st.error("Token Hugging Face belum terbaca oleh Streamlit Cloud!")
    elif article_input.strip() == "":
        st.warning("Teksnya masih kosong, Wan!")
    elif len(article_input.split()) < 20:
        st.warning("Teks terlalu pendek untuk diringkas secara efektif.")
    else:
        with st.spinner("Mengirim data ke otak AI di awan... ☁️"):
            payload = {
                "inputs": article_input,
                "parameters": {
                    "min_length": 40,
                    "max_length": 150,
                }
            }
            
            output = query_hf_api(payload)
            
            # Cek kalau ada pesan error dari server HF
            if isinstance(output, dict) and "error" in output:
                st.error(f"Sistem API membalas: {output['error']}")
                if "estimated_time" in output:
                    st.info(f"Server AI sedang dipanaskan (Cold Start). Silakan tunggu {int(output['estimated_time'])} detik, lalu klik tombol Generate lagi.")
            else:
                try:
                    summary = output[0]['summary_text']
                    st.success("Ringkasan Berhasil Dibuat!")
                    st.markdown("### Hasil Ringkasan:")
                    st.info(summary)
                except KeyError:
                    st.error("Balasan dari server tidak sesuai format yang diharapkan.")

st.sidebar.markdown("---")
st.sidebar.info("Arsitektur: Microservices + Inference API.\nBerat Aplikasi: < 5 MB.")
