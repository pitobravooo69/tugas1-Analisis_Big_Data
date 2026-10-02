# Dokumentasi Dataset

## Sumber
- **Penyedia:** BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)
- **Dataset:** Data Prakiraan Cuaca Terbuka BMKG
- **Link:** https://data.bmkg.go.id/prakiraan-cuaca/
- **API Endpoint:** `https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=<kode>`
- **Jenis data:** PRAKIRAAN cuaca (bukan pengamatan), per kelurahan/desa, 3 hari ke depan, 8 data per hari (per 3 jam)
- **Tanggal pengambilan:** 2026-10-02 (WIB / UTC+7)

## Ukuran
- Jumlah baris: ± 3.360 baris (20 desa × 3 hari × 8 slot per hari = 480 minimum; lebih besar bila ada multi-lokasi)
- Ukuran file: < 1 MB (per batch 20 desa); skala ke ~50–100 MB untuk satu provinsi penuh
- Cakupan wilayah: Jawa Timur (kode provinsi 35) — tes awal 20 desa/kelurahan

## Cara Mengunduh

### Dengan Docker (direkomendasikan)
```bash
# Bangun image terlebih dahulu
docker compose build

# Tes kecil: 20 desa Jawa Timur
docker compose run --rm downloader --provinsi 35 --limit 20

# Unduh satu provinsi penuh (Jawa Timur)
docker compose run --rm downloader --provinsi 35

# Unduh provinsi lain (mis. DKI Jakarta = 31)
docker compose run --rm downloader --provinsi 31
```

### Tanpa Docker
```bash
pip install -r requirements.txt

# Tes kecil
python src/download_bmkg.py --provinsi 35 --limit 20

# Penuh Jawa Timur
python src/download_bmkg.py --provinsi 35
```

Hasil disimpan di `data/raw/` (format Parquet, tidak di-commit ke Git).

## Kamus Kolom
| Kolom | Tipe | Arti |
|---|---|---|
| `kode_adm4` | String | Kode wilayah kelurahan/desa (format: `prov.kotkab.kec.desa`) |
| `provinsi` | String | Nama provinsi |
| `kotkab` | String | Nama kota/kabupaten |
| `kecamatan` | String | Nama kecamatan |
| `desa` | String | Nama kelurahan/desa |
| `lat` | Float | Koordinat lintang |
| `lon` | Float | Koordinat bujur |
| `t` | Float | Suhu udara (°C) |
| `hu` | Float | Kelembapan relatif (%) |
| `ws` | Float | Kecepatan angin (km/jam atau knot — cek respons API) |
| `wd` | String/Float | Arah angin |
| `tcc` | Float | Total cloud cover / tutupan awan (%) |
| `tp` | Float | Total precipitation / curah hujan (mm) |
| `weather_desc` | String | Deskripsi kondisi cuaca dalam Bahasa Indonesia |
| `utc_datetime` | String | Waktu prakiraan dalam UTC |
| `local_datetime` | String | Waktu prakiraan dalam WIB (UTC+7) |
| `fetched_at` | String | Timestamp saat data diambil (ISO 8601 UTC) |

> **Catatan:** Nama kolom dan satuan bisa berbeda tergantung respons aktual API BMKG.
> Selalu verifikasi dengan `lf.collect_schema()` setelah download.

## Catatan
- Data bersumber dari BMKG. **Wajib mencantumkan BMKG sebagai sumber** dalam setiap publikasi.
- Data ini prakiraan (forecast), bukan observasi; kualitasnya bergantung model BMKG.
- File Parquet di `data/raw/` di-ignore oleh Git (lihat `.gitignore`).
- Gunakan `pl.scan_parquet('../data/raw/*.parquet')` untuk membaca lazy di Polars.
