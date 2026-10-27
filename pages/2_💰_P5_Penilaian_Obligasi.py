"""
Sub-CPMK5: Mampu menilai harga wajar obligasi
Pertemuan 5 — Penilaian Obligasi
Integrasi Profetik: Amanah — QS Al Baqarah: 282
"""
import streamlit as st
import numpy as np
from scipy.optimize import brentq
import plotly.graph_objects as go

st.set_page_config(page_title="P5 — Penilaian Obligasi", page_icon="💰", layout="wide")
st.title("💰 Pertemuan 5: Penilaian Obligasi")
st.caption("Sub-CPMK5 · Amanah · QS Al Baqarah: 282")

tab_materi, tab_hitung = st.tabs(["📖 Materi", "🧮 Hitung"])

# ──────────────────────────────────────────────
# TAB MATERI
# ──────────────────────────────────────────────
with tab_materi:
    st.header("1. Ciri-ciri Obligasi")
    st.markdown("""
Obligasi (*bond*) adalah surat utang jangka panjang yang diterbitkan oleh
pemerintah atau perusahaan.

| Ciri | Keterangan |
|------|------------|
| **Nilai Nominal (Face Value / Par)** | Nilai pokok yang dibayar saat jatuh tempo, umumnya Rp1.000.000 atau $1.000 |
| **Kupon (Coupon Rate)** | Tingkat bunga tahunan yang dibayarkan secara periodik |
| **Jatuh Tempo (Maturity)** | Tanggal obligasi harus dilunasi |
| **Penerbit (Issuer)** | Pemerintah, BUMN, atau perusahaan swasta |
| **Frekuensi Kupon** | Tahunan atau semi-annual (setiap 6 bulan) |
""")

    st.header("2. Nilai Sekarang Arus Kupon dan Nilai Nominal")
    st.markdown(r"""
Harga wajar obligasi = **nilai sekarang (PV)** dari seluruh arus kas masa depan:

$$
P_0 = \sum_{t=1}^{n} \frac{C}{(1+r)^t} + \frac{F}{(1+r)^n}
$$

| Simbol | Arti |
|--------|------|
| $P_0$ | Harga wajar obligasi saat ini |
| $C$ | Pembayaran kupon per periode = Kupon Rate × Nominal / frekuensi |
| $F$ | Nilai nominal (*face value*) |
| $r$ | Tingkat diskonto per periode (*required yield*) |
| $n$ | Jumlah total periode pembayaran kupon |

Dapat juga ditulis menggunakan rumus anuitas:

$$
P_0 = C \times \frac{1 - (1+r)^{-n}}{r} + \frac{F}{(1+r)^n}
$$

**Hubungan harga dan yield:**
- Jika kupon rate = yield → harga = nilai nominal (*at par*)
- Jika kupon rate > yield → harga > nominal (*premium*)
- Jika kupon rate < yield → harga < nominal (*discount*)
""")

    st.header("3. Imbal Hasil Sampai Jatuh Tempo (*Yield to Maturity / YTM*)")
    st.markdown(r"""
YTM adalah tingkat diskonto yang menyamakan harga pasar obligasi dengan
nilai sekarang seluruh arus kasnya.

$$
P_{market} = \sum_{t=1}^{n} \frac{C}{(1+YTM)^t} + \frac{F}{(1+YTM)^n}
$$

YTM tidak bisa dihitung secara langsung (closed-form), sehingga harus
diselesaikan secara **numerik** (trial-and-error atau metode *root-finding*).

**Aproksimasi YTM:**

$$
YTM \approx \frac{C + \frac{F - P_0}{n}}{\frac{F + P_0}{2}}
$$

Kalkulator di tab Hitung menggunakan metode **Brent** dari `scipy` untuk
menghitung YTM secara akurat.
""")

    st.header("4. Peringkat Obligasi dan Risiko Gagal Bayar")
    st.markdown("""
Peringkat obligasi menunjukkan **kemampuan penerbit membayar kewajiban**
(kupon dan pokok).

| Peringkat | Moody's | S&P / Fitch | Kategori |
|-----------|---------|-------------|----------|
| Tertinggi | Aaa | AAA | *Investment Grade* |
| Tinggi | Aa1–Aa3 | AA+, AA, AA− | *Investment Grade* |
| Menengah Atas | A1–A3 | A+, A, A− | *Investment Grade* |
| Menengah | Baa1–Baa3 | BBB+, BBB, BBB− | *Investment Grade* |
| Spekulatif | Ba1–Ba3 | BB+, BB, BB− | *High Yield / Junk* |
| Sangat Spekulatif | B1–B3 | B+, B, B− | *High Yield / Junk* |
| Risiko Tinggi | Caa–C | CCC–C | *High Yield / Junk* |
| Gagal Bayar | — | D | *Default* |

**Hubungan peringkat dan yield:**
- Peringkat **lebih rendah** → risiko gagal bayar **lebih tinggi** →
  investor minta yield **lebih tinggi** → harga obligasi **lebih rendah**
- Selisih yield antara obligasi korporasi dan obligasi pemerintah disebut
  **credit spread** atau **default spread**
""")

    st.info("""
🕌 **Amanah — QS Al Baqarah: 282**

*"Hai orang-orang yang beriman, apabila kamu bermuamalah tidak secara tunai
untuk waktu yang ditentukan, hendaklah kamu menuliskannya."*

Obligasi adalah bentuk muamalah utang-piutang tertulis. Prinsip **Amanah**
menuntut penerbit obligasi untuk memenuhi janji pembayaran kupon dan pokok
tepat waktu — inilah esensi dari peringkat obligasi.
""")


# ──────────────────────────────────────────────
# TAB HITUNG
# ──────────────────────────────────────────────
with tab_hitung:
    mode = st.radio(
        "Pilih jenis perhitungan:",
        ["💵 Harga Wajar Obligasi",
         "📊 Yield to Maturity (YTM)",
         "📈 Kurva Harga vs Yield"],
        horizontal=True,
    )

    # ─── MODE 1: BOND PRICING ───
    if mode == "💵 Harga Wajar Obligasi":
        st.subheader("Menghitung Harga Wajar Obligasi")

        c1, c2 = st.columns(2)
        with c1:
            face = st.number_input("Nilai Nominal (F)", value=1_000_000, min_value=1, step=100_000)
            coupon_rate = st.number_input("Kupon Rate (% per tahun)", value=8.0,
                                         min_value=0.0, max_value=100.0, step=0.25) / 100
            freq = st.selectbox("Frekuensi Kupon", [1, 2, 4],
                                format_func=lambda x: {1: "Tahunan", 2: "Semi-annual", 4: "Kuartalan"}[x])
        with c2:
            years = st.number_input("Jatuh Tempo (tahun)", value=5, min_value=1, max_value=100)
            req_yield = st.number_input("Required Yield (% per tahun)", value=10.0,
                                        min_value=0.01, max_value=100.0, step=0.25) / 100

        if st.button("Hitung Harga Obligasi", type="primary"):
            n = years * freq
            c = face * coupon_rate / freq
            r = req_yield / freq

            pv_coupons = c * (1 - (1 + r)**(-n)) / r
            pv_face = face / (1 + r)**n
            price = pv_coupons + pv_face

            st.markdown("### Hasil Perhitungan")

            col1, col2, col3 = st.columns(3)
            col1.metric("PV Arus Kupon", f"Rp{pv_coupons:,.0f}")
            col2.metric("PV Nilai Nominal", f"Rp{pv_face:,.0f}")
            col3.metric("Harga Wajar (P₀)", f"Rp{price:,.0f}")

            if price > face * 1.001:
                st.success(f"📈 Obligasi dijual **premium** (harga > nominal) karena kupon rate ({coupon_rate:.2%}) > yield ({req_yield:.2%})")
            elif price < face * 0.999:
                st.warning(f"📉 Obligasi dijual **discount** (harga < nominal) karena kupon rate ({coupon_rate:.2%}) < yield ({req_yield:.2%})")
            else:
                st.info("⚖️ Obligasi dijual **at par** (harga ≈ nominal)")

            with st.expander("📝 Langkah Perhitungan"):
                st.markdown(f"**Parameter:**")
                st.markdown(f"- Kupon per periode: C = {face:,.0f} × {coupon_rate:.2%} / {freq} = **Rp{c:,.0f}**")
                st.markdown(f"- Yield per periode: r = {req_yield:.2%} / {freq} = **{r:.4%}**")
                st.markdown(f"- Jumlah periode: n = {years} × {freq} = **{n}**")
                st.latex(rf"PV_{{kupon}} = {c:,.0f} \times \frac{{1 - (1+{r:.4f})^{{-{n}}}}}{{{r:.4f}}} = {pv_coupons:,.0f}")
                st.latex(rf"PV_{{nominal}} = \frac{{{face:,.0f}}}{{(1+{r:.4f})^{{{n}}}}} = {pv_face:,.0f}")
                st.latex(rf"P_0 = {pv_coupons:,.0f} + {pv_face:,.0f} = \mathbf{{{price:,.0f}}}")

            # Cash flow timeline
            st.markdown("### Arus Kas Obligasi")
            periods = list(range(1, n + 1))
            cfs = [c] * n
            cfs[-1] += face
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[f"t={t}" for t in periods],
                y=cfs,
                marker_color=['#3b82f6'] * (n - 1) + ['#22c55e'],
                text=[f"Rp{cf:,.0f}" for cf in cfs],
                textposition='outside',
            ))
            fig.update_layout(
                title="Arus Kas Obligasi per Periode",
                yaxis_title="Arus Kas (Rp)",
                xaxis_title="Periode",
                height=400,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)


    # ─── MODE 2: YTM ───
    elif mode == "📊 Yield to Maturity (YTM)":
        st.subheader("Menghitung Yield to Maturity")

        c1, c2 = st.columns(2)
        with c1:
            face_ytm = st.number_input("Nilai Nominal (F)", value=1_000_000, min_value=1,
                                       step=100_000, key="f_ytm")
            coupon_rate_ytm = st.number_input("Kupon Rate (% per tahun)", value=8.0,
                                             min_value=0.0, max_value=100.0, step=0.25,
                                             key="cr_ytm") / 100
            freq_ytm = st.selectbox("Frekuensi Kupon", [1, 2, 4], key="freq_ytm",
                                    format_func=lambda x: {1: "Tahunan", 2: "Semi-annual", 4: "Kuartalan"}[x])
        with c2:
            years_ytm = st.number_input("Jatuh Tempo (tahun)", value=5, min_value=1,
                                        max_value=100, key="y_ytm")
            market_price = st.number_input("Harga Pasar Obligasi (Rp)", value=950_000,
                                          min_value=1, step=10_000)

        if st.button("Hitung YTM", type="primary"):
            n_ytm = years_ytm * freq_ytm
            c_ytm = face_ytm * coupon_rate_ytm / freq_ytm

            def bond_price_diff(r_period):
                if r_period <= 0:
                    return 1e10
                pv_c = c_ytm * (1 - (1 + r_period)**(-n_ytm)) / r_period
                pv_f = face_ytm / (1 + r_period)**n_ytm
                return pv_c + pv_f - market_price

            try:
                ytm_period = brentq(bond_price_diff, 1e-8, 2.0)
                ytm_annual = ytm_period * freq_ytm

                # Approximation
                ytm_approx = (c_ytm * freq_ytm + (face_ytm - market_price) / years_ytm) / \
                             ((face_ytm + market_price) / 2)

                st.markdown("### Hasil Perhitungan")

                col1, col2, col3 = st.columns(3)
                col1.metric("YTM per Periode", f"{ytm_period:.4%}")
                col2.metric("YTM Tahunan", f"{ytm_annual:.4%}")
                col3.metric("YTM Aproksimasi", f"{ytm_approx:.4%}")

                # Verify
                pv_c_check = c_ytm * (1 - (1 + ytm_period)**(-n_ytm)) / ytm_period
                pv_f_check = face_ytm / (1 + ytm_period)**n_ytm
                price_check = pv_c_check + pv_f_check

                st.markdown(f"**Verifikasi:** Dengan YTM = {ytm_annual:.4%}, "
                            f"harga obligasi = Rp{price_check:,.0f} ≈ Rp{market_price:,.0f} ✅")

                with st.expander("📝 Langkah Perhitungan"):
                    st.markdown("**Aproksimasi YTM:**")
                    st.latex(
                        rf"YTM \approx \frac{{{c_ytm * freq_ytm:,.0f} + \frac{{{face_ytm:,.0f} - {market_price:,.0f}}}{{{years_ytm}}}}}"
                        rf"{{\frac{{{face_ytm:,.0f} + {market_price:,.0f}}}{{2}}}} = {ytm_approx:.4%}"
                    )
                    st.markdown("**YTM Eksak (metode Brent):**")
                    st.latex(rf"YTM_{{periode}} = {ytm_period:.6f}")
                    st.latex(rf"YTM_{{tahunan}} = {ytm_period:.6f} \times {freq_ytm} = {ytm_annual:.6f} = {ytm_annual:.4%}")

            except ValueError:
                st.error("❌ Tidak dapat menghitung YTM. Periksa kembali input Anda.")


    # ─── MODE 3: PRICE-YIELD CURVE ───
    else:
        st.subheader("Kurva Harga vs Yield")
        st.markdown("Grafik hubungan **terbalik** antara yield dan harga obligasi.")

        c1, c2 = st.columns(2)
        with c1:
            face_curve = st.number_input("Nilai Nominal (F)", value=1_000_000, min_value=1,
                                         step=100_000, key="f_curve")
            coupon_rate_curve = st.number_input("Kupon Rate (% per tahun)", value=8.0,
                                               min_value=0.0, max_value=100.0, step=0.25,
                                               key="cr_curve") / 100
        with c2:
            years_curve = st.number_input("Jatuh Tempo (tahun)", value=10, min_value=1,
                                          max_value=100, key="y_curve")
            freq_curve = st.selectbox("Frekuensi Kupon", [1, 2], key="freq_curve",
                                      format_func=lambda x: {1: "Tahunan", 2: "Semi-annual"}[x])

        if st.button("Tampilkan Kurva", type="primary"):
            yields = np.linspace(0.01, 0.20, 100)
            prices = []
            n_c = years_curve * freq_curve
            c_c = face_curve * coupon_rate_curve / freq_curve

            for y in yields:
                r_c = y / freq_curve
                pv = c_c * (1 - (1 + r_c)**(-n_c)) / r_c + face_curve / (1 + r_c)**n_c
                prices.append(pv)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=yields * 100, y=prices,
                mode='lines',
                line=dict(color='#3b82f6', width=3),
                name='Harga Obligasi',
            ))
            fig.add_hline(y=face_curve, line_dash="dash", line_color="gray",
                          annotation_text=f"Par Value = Rp{face_curve:,.0f}")
            fig.add_vline(x=coupon_rate_curve * 100, line_dash="dash", line_color="orange",
                          annotation_text=f"Coupon Rate = {coupon_rate_curve:.1%}")
            fig.update_layout(
                title="Kurva Harga–Yield Obligasi",
                xaxis_title="Yield to Maturity (%)",
                yaxis_title="Harga Obligasi (Rp)",
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
**Pengamatan:**
- Kurva **menurun** → yield naik, harga turun (*inverse relationship*)
- Kurva **cembung** (*convex*) → penurunan harga melambat saat yield semakin tinggi
- Saat yield = coupon rate → harga = nilai nominal
""")
