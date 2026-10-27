"""
Lab Manajemen Investasi dan Pasar Modal
Universitas Muhammadiyah Metro — Program Studi Sarjana Kewirausahaan
FEB24019 — Semester Genap
"""
import streamlit as st

st.set_page_config(
    page_title="Lab Investasi & Pasar Modal",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Lab Manajemen Investasi dan Pasar Modal")
st.caption("FEB24019 — Program Studi Sarjana Kewirausahaan, Universitas Muhammadiyah Metro")

st.markdown("---")

st.markdown("""
### Selamat datang!

Aplikasi ini adalah **laboratorium hitung interaktif** untuk mata kuliah
Manajemen Investasi dan Pasar Modal. Gunakan menu di sebelah kiri untuk
memilih pertemuan.

| Pertemuan | Sub-CPMK | Topik |
|:---------:|:--------:|-------|
| 4 | Sub-CPMK4 | Imbal Hasil dan Risiko Aset Tunggal |
| 5 | Sub-CPMK5 | Penilaian Obligasi |

Setiap halaman memiliki dua tab:
- **📖 Materi** — rangkuman teori dan rumus
- **🧮 Hitung** — kalkulator interaktif untuk latihan
""")

st.markdown("---")

with st.expander("📚 Pustaka Utama"):
    st.markdown("""
1. Tim Pengampu, 2026, *Modul Manajemen Investasi dan Pasar Modal*, Metro: Universitas Muhammadiyah Metro
2. Bodie, Z., Kane, A., dan Marcus, A. J., 2021, *Investments*, New York: McGraw-Hill
3. Tandelilin, E., 2020, *Portofolio dan Investasi: Teori dan Aplikasi*, Yogyakarta: Kanisius
4. Hartono, J., 2022, *Teori Portofolio dan Analisis Investasi*, Yogyakarta: BPFE
""")

with st.expander("🕌 Integrasi Nilai Profetik"):
    st.markdown("""
Mata kuliah ini mengintegrasikan empat nilai profetik:
**Shiddiq** (jujur), **Amanah** (dapat dipercaya), **Fathonah** (cerdas), dan **Tabligh** (menyampaikan).

> *"Tiada seorang pun yang dapat mengetahui apa yang akan diusahakannya besok"*
> — QS Luqman: 34

Setiap investasi mengandung ketidakpastian. Pengukuran risiko yang tepat
adalah wujud **Fathonah** dalam mengambil keputusan.
""")
