### 1. Value Proposition
Di dunia yang serba cepat, kita sering mengalami Information Overload. Setiap hari kita dibombardir oleh ribuan kata dari berita, dokumen teknis, hingga laporan riset. Masalah utamanya adalah pemborosan waktu operasional; membaca 2.000 kata hanya untuk mencari inti sari adalah inefisiensi besar.
Ringkas.in hadir sebagai painkiller yang mengubah cara kita mengonsumsi informasi:
- Meningkatkan Fokus: Memangkas kebisingan informasi dan langsung menyajikan fakta inti.
- Kecepatan Akselerasi: Memungkinkan pengambilan keputusan dilakukan dalam hitungan detik, bukan jam.
- Efisiensi Kognitif: Mengurangi beban mental pengguna dalam memproses dokumen yang panjang dan bertele-tele.

### 2. Tech Stack
Aplikasi ini dibangun dengan kombinasi teknologi yang mengutamakan performa lokal dan akurasi linguistik:
- mT5 Multilingual XLSum: Menggunakan model Transformer berbasis Encoder-Decoder yang telah dilatih pada dataset XLSum (berita dari 45 bahasa, termasuk Indonesia). Model ini dipilih karena kemampuannya dalam memahami struktur kalimat bahasa Indonesia yang kompleks.
- Streamlit: Digunakan sebagai frontend dan web server karena kemampuannya untuk melakukan rapid prototyping aplikasi data dengan Python murni.
- PyTorch & Transformers: Framework utama untuk menangani komputasi tensor dan manajemen weights model AI.
- Implementasi: Kita melakukan optimasi pada tahap Inference menggunakan Beam Search (num_beams=4). Ini memungkinkan AI mencari jalur kata yang paling logis dan koheren, bukan sekadar kata yang paling sering muncul (Greedy Search), sehingga hasilnya jauh lebih manusiawi.

### 3. Architecture
Alur kerja data dalam Ringkas.in dirancang secara linier dan efisien:
- Input Layer: Pengguna memasukkan teks mentah melalui antarmuka Streamlit.
- Tokenization: Teks dipecah menjadi unit-unit kecil (tokens) menggunakan SentencePiece tokenizer agar bisa diproses secara numerik oleh model.
- Context Windowing: Sistem membatasi input hingga 512 token untuk menjaga stabilitas memori (RAM) tanpa kehilangan konteks utama artikel.
- Transformation (The Brain): Model mT5 melakukan proses encoding (memahami makna) dan decoding (menyusun kembali kalimat baru) secara otomatis.
- Output Layer: Hasil ringkasan yang telah di-decode dikembalikan dalam bentuk teks bahasa manusia dan ditampilkan di layar.

### 4. Cara Penggunaan (Offline)
#### Buat Virtual Environment :
```
python -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
```
#### Install Dependensi :
```
pip install streamlit transformers torch sentencepiece
```

#### Jalankan Aplikasi :
```
streamlit run app.py
```
Buka aplikasi di : http://localhost:8501 

<img width="607" height="567" alt="image" src="https://github.com/user-attachments/assets/4f6ca1a5-d420-4082-a512-5664e842edba" />
