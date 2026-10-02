# Tugas 1 - Analisis Big Data: Prakiraan Cuaca Indonesia (BMKG)

- **Nama:** Alfito Afdhan Nugraha
- **NIM:** 202310370311415
- **Dataset:** Prakiraan Cuaca Terbuka BMKG (lihat `data/README.md`)

## Struktur
```
data/README.md      cara unduh & kamus kolom
data/raw/           data mentah (di-ignore Git)
notebooks/          01_data_profiling.ipynb
src/                skrip (download_bmkg.py)
output/figures/     gambar/visualisasi
Dockerfile          image Python + JupyterLab
docker-compose.yml  orkestrasi layanan
```

## Cara Menjalankan (Docker — Direkomendasikan)

```bash
# 1. Build & jalankan JupyterLab
docker compose up --build jupyter

# 2. Buka browser → http://localhost:8888

# 3. Download data BMKG (contoh: Jawa Timur, 20 desa)
docker compose run --rm downloader --provinsi 35 --limit 20

# 4. Download penuh Jawa Timur
docker compose run --rm downloader --provinsi 35
```

## Cara Menjalankan (Lokal — Tanpa Docker)

```bash
pip install -r requirements.txt

# Tes kecil (20 desa Jawa Timur)
python src/download_bmkg.py --provinsi 35 --limit 20

# Penuh
python src/download_bmkg.py --provinsi 35
```

## Progres
- [x] Milestone 1 (Pertemuan 3): dataset + data/README.md + 01_data_profiling.ipynb
- [ ] Milestone 2 (Pertemuan 5)
- [ ] Milestone 3 (Pertemuan 8)
- [ ] Final (Pertemuan 10)

## AI Disclosure Statement
Dalam pengerjaan Milestone 1 ini, saya menggunakan asisten AI (Antigravity/Claude) untuk:
- Membantu membuat struktur proyek Docker (Dockerfile dan docker-compose.yml)
- Membantu melengkapi template notebook `01_data_profiling.ipynb` dengan cell analisis tambahan
- Membantu menyempurnakan komentar dan dokumentasi pada `src/download_bmkg.py`

Bagian yang saya kerjakan dan verifikasi sendiri:
- Memahami dan menguji API BMKG (`data.bmkg.go.id/prakiraan-cuaca`)
- Memilih cakupan wilayah yang relevan untuk analisis
- Menginterpretasikan hasil data profiling dan mencatat temuan di notebook
- Memastikan semua kode berjalan dengan benar di lingkungan lokal maupun Docker
