"""
Unduh Prakiraan Cuaca Terbuka BMKG per kelurahan/desa -> Parquet.

Sumber : BMKG (Badan Meteorologi, Klimatologi, dan Geofisika), https://data.bmkg.go.id/prakiraan-cuaca/
Catatan: WAJIB mencantumkan BMKG sebagai sumber data.

PENTING: BASE_URL dan struktur JSON di bawah ini adalah dugaan awal.
Cocokkan dengan dokumentasi resmi di data.bmkg.go.id/prakiraan-cuaca,
lalu sesuaikan BASE_URL dan fungsi flatten() bila berbeda.

Contoh pakai:
    python src/download_bmkg.py --kode-csv data/kode_wilayah.csv --provinsi 35 --limit 20
"""
from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

import polars as pl
import requests

BASE_URL = "https://api.bmkg.go.id/publik/prakiraan-cuaca"  # <- cek di dokumentasi BMKG
OUT_DIR = Path("data/raw")


def fetch(kode: str, session: requests.Session, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            r = session.get(BASE_URL, params={"adm4": kode}, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 503):  # kena batas akses -> tunggu lebih lama
                time.sleep(5 * (attempt + 1))
                continue
            return None  # kode tidak ada / error lain
        except requests.RequestException:
            time.sleep(2 * (attempt + 1))
    return None


def flatten(payload: dict, kode: str, fetched_at: str) -> list[dict]:
    """Ratakan JSON jadi satu baris per (desa, waktu prakiraan)."""
    rows: list[dict] = []
    lokasi = payload.get("lokasi", {}) or {}
    for blok in payload.get("data", []) or []:
        lok = {**lokasi, **(blok.get("lokasi", {}) or {})}
        for hari in blok.get("cuaca", []) or []:
            entries = hari if isinstance(hari, list) else [hari]
            for e in entries:
                if not isinstance(e, dict):
                    continue
                rows.append(
                    {
                        "kode_adm4": kode,
                        "provinsi": lok.get("provinsi"),
                        "kotkab": lok.get("kotkab"),
                        "kecamatan": lok.get("kecamatan"),
                        "desa": lok.get("desa"),
                        "lat": lok.get("lat"),
                        "lon": lok.get("lon"),
                        "fetched_at": fetched_at,
                        **e,  # t, hu, ws, wd, tcc, tp, weather_desc, utc_datetime, ...
                    }
                )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kode-csv", default="data/kode_wilayah.csv")
    ap.add_argument("--provinsi", help="awalan kode, mis. 35 untuk Jawa Timur")
    ap.add_argument("--limit", type=int, help="batasi jumlah desa (untuk tes)")
    ap.add_argument("--batch", type=int, default=500, help="simpan Parquet tiap N desa")
    ap.add_argument("--sleep", type=float, default=0.5, help="jeda antar permintaan (detik)")
    args = ap.parse_args()

    kode_df = pl.read_csv(args.kode_csv, schema_overrides={"kode_adm4": pl.Utf8})
    kodes = kode_df["kode_adm4"].to_list()
    if args.provinsi:
        kodes = [k for k in kodes if k.startswith(args.provinsi + ".")]
    if args.limit:
        kodes = kodes[: args.limit]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    prov = args.provinsi or "all"
    session = requests.Session()
    buffer: list[dict] = []
    part = 0

    def flush() -> None:
        nonlocal buffer, part
        if buffer:
            path = OUT_DIR / f"bmkg_{prov}_{stamp}_part{part:04d}.parquet"
            pl.DataFrame(buffer, infer_schema_length=None).write_parquet(path)
            print(f"  simpan {len(buffer):,} baris -> {path}")
            buffer, part = [], part + 1

    for i, kode in enumerate(kodes, 1):
        payload = fetch(kode, session)
        if payload:
            buffer.extend(flatten(payload, kode, datetime.now(timezone.utc).isoformat()))
        if i % args.batch == 0:
            print(f"{i}/{len(kodes)} desa diproses")
            flush()
        time.sleep(args.sleep)
    flush()
    print("selesai.")


if __name__ == "__main__":
    main()
