import streamlit as st
import requests
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Ringkas.in - Prototipe API", page_icon="📝")

# --- KONFIGURASI API ---
# URL ini menunjuk langsung ke model mT5 di cloud Hugging Face
API_URL = "https://api-inference.huggingface.co/models/csebuetnlp/mT5_multilingual_XLSum"

# Mengambil token rahasia dari setting environment Hugging Face
HF_TOKEN = os.environ.get("HF_TOKEN") 
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf_api(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# --- TAMPILAN UTAMA ---
st.title("📝 Ringkas.in (Versi Ringan)")
st.subheader("Prototipe Peringkas Teks Otomatis (Microservices API)")
st.markdown("---")

# Input Teks
article_input = st.text_area("Tempelkan Artikel Berita di Sini:", height=300, 
                             placeholder="Masukkan teks berita bahasa Indonesia yang ingin diringkas...")

if st.button("Generate Ringkasan"):
    if not HF_TOKEN:
        st.error("Token Hugging Face belum dipasang di pengaturan server!")
    elif article_input.strip() == "":
        st.warning("Teksnya masih kosong, Wan!")
    elif len(article_input.split()) < 20:
        st.warning("Teks terlalu pendek untuk diringkas secara efektif.")
    else:
        with st.spinner("Mengirim data ke otak AI di awan... ☁️"):
            try:
                # Parameter untuk dikirim ke API
                payload = {
                    "inputs": article_input,
                    "parameters": {
                        "min_length": 40,
                        "max_length": 150,
                    }
                }
                
                # Tembak API-nya
                output = query_hf_api(payload)
                
                # Cek kalau ada error dari server HF (misal: modelnya lagi tidur)
                if isinstance(output, dict) and "error" in output:
                    st.error(f"Sistem API membalas: {output['error']}")
                    if "estimated_time" in output:
                        st.info(f"Server AI sedang dipanaskan (Cold Start). Silakan tunggu sekitar {int(output['estimated_time'])} detik, lalu klik tombol Generate lagi.")
                else:
                    # Ambil hasil ringkasan
                    summary = output[0]['summary_text']
                    
                    st.success("Ringkasan Berhasil Dibuat dalam Hitungan Detik!")
                    st.markdown("### Hasil Ringkasan:")
                    st.info(summary)
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan koneksi jaringan: {e}")

st.sidebar.markdown("---")
st.sidebar.info("Arsitektur: Microservices + Inference API.\nBerat Aplikasi: < 5 MB.")