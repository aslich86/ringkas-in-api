import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Konfigurasi Halaman
st.set_page_config(page_title="Ringkas.in - Prototipe Capstone", page_icon="📝")

# --- LOAD MODEL (DI-CACHE) ---
@st.cache_resource
def load_model():
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

# --- TAMPILAN UTAMA ---
st.title("📝 Ringkas.in")
st.subheader("Prototipe Peringkas Teks Otomatis (mT5)")
st.markdown("---")

# Load mesinnya
with st.spinner("Sedang memuat model AI... (Mohon tunggu)"):
    tokenizer, model = load_model()

# Sidebar untuk Parameter (Bahan Eksperimen)
st.sidebar.header("Pengaturan Model")
max_len = st.sidebar.slider("Max Summary Length", 50, 300, 150)
min_len = st.sidebar.slider("Min Summary Length", 20, 100, 40)
num_beams = st.sidebar.slider("Beam Search (Precision)", 1, 10, 4)

# Input Teks
article_input = st.text_area("Tempelkan Artikel Berita di Sini:", height=300, 
                             placeholder="Masukkan teks berita bahasa Indonesia yang ingin diringkas...")

if st.button("Generate Ringkasan"):
    if article_input.strip() == "":
        st.error("Waduh, teksnya masih kosong, Wan!")
    elif len(article_input.split()) < 20:
        st.warning("Teks terlalu pendek untuk diringkas secara efektif.")
    else:
        with st.spinner("AI sedang membaca dan meringkas..."):
            # Tokenisasi
            inputs = tokenizer(article_input, return_tensors="pt", max_length=512, truncation=True)
            
            # Generate
            summary_ids = model.generate(
                inputs["input_ids"], 
                max_length=max_len, 
                min_length=min_len, 
                num_beams=num_beams,
                early_stopping=True
            )
            
            # Decode
            result = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            st.success("Ringkasan Berhasil Dibuat!")
            st.markdown("### Hasil Ringkasan:")
            st.write(result)
            
            st.markdown("---")
            st.caption(f"Model: mT5 | Beams: {num_beams} | Length: {min_len}-{max_len} tokens")

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi ini adalah prototipe Capstone menggunakan Streamlit.")
