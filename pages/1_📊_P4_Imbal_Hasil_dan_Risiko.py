"""
Sub-CPMK4: Mampu menghitung imbal hasil dan risiko aset tunggal
Pertemuan 4 — Imbal Hasil dan Risiko Aset Tunggal
Integrasi Profetik: Fathonah — QS Luqman: 34
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="P4 — Imbal Hasil & Risiko", page_icon="📊", layout="wide")
st.title("📊 Pertemuan 4: Imbal Hasil dan Risiko Aset Tunggal")
st.caption("Sub-CPMK4 · Fathonah · QS Luqman: 34")

tab_materi, tab_hitung = st.tabs(["📖 Materi", "🧮 Hitung"])

# ──────────────────────────────────────────────
# TAB MATERI
# ──────────────────────────────────────────────
with tab_materi:
    st.header("1. Imbal Hasil Terwujud (*Realized Return*)")
    st.markdown(r"""
Imbal hasil terwujud adalah imbal hasil yang **sudah terjadi**,
dihitung dari data harga historis.

$$
R_t = \frac{P_t - P_{t-1} + D_t}{P_{t-1}}
$$

| Simbol | Arti |
|--------|------|
| $R_t$ | Imbal hasil periode $t$ |
| $P_t$ | Harga akhir periode $t$ |
| $P_{t-1}$ | Harga awal periode $t$ |
| $D_t$ | Dividen (atau kupon) yang diterima pada periode $t$ |

**Contoh:** Saham dibeli Rp1.000, dijual Rp1.150, dividen Rp50.

$$R = \frac{1.150 - 1.000 + 50}{1.000} = 0{,}20 = 20\%$$
""")

    st.header("2. Imbal Hasil Harapan (*Expected Return*)")
    st.markdown(r"""
Imbal hasil harapan adalah rata-rata tertimbang dari imbal hasil
pada setiap kondisi ekonomi menurut probabilitasnya.

$$
E(R) = \sum_{i=1}^{n} p_i \cdot R_i
$$

| Simbol | Arti |
|--------|------|
| $E(R)$ | Imbal hasil harapan |
| $p_i$ | Probabilitas kondisi $i$ |
| $R_i$ | Imbal hasil pada kondisi $i$ |
| $n$ | Jumlah kondisi ekonomi |

Jika menggunakan data historis (semua kondisi berpeluang sama):

$$
E(R) = \bar{R} = \frac{1}{n}\sum_{i=1}^{n} R_i
$$
""")

    st.header("3. Ragam dan Simpangan Baku sebagai Ukuran Risiko")
    st.markdown(r"""
**Ragam (Variance)** mengukur penyebaran imbal hasil terhadap rata-ratanya.

$$
\sigma^2 = \sum_{i=1}^{n} p_i \cdot (R_i - E(R))^2
$$

Untuk data historis (sampel):

$$
s^2 = \frac{1}{n-1}\sum_{i=1}^{n} (R_i - \bar{R})^2
$$

**Simpangan Baku (Standard Deviation)**:

$$
\sigma = \sqrt{\sigma^2}
$$

Semakin besar $\sigma$, semakin besar **risiko** investasi tersebut.
""")

    st.header("4. Hubungan Risiko dan Imbal Hasil")
    st.markdown(r"""
Prinsip dasar investasi:

> **Semakin tinggi risiko, semakin tinggi imbal hasil yang disyaratkan**
> (*high risk, high return*)

Hubungan ini digambarkan dalam grafik **Risk–Return Tradeoff**:
- Sumbu X: Risiko (simpangan baku, $\sigma$)
- Sumbu Y: Imbal hasil harapan, $E(R)$

Investor rasional memilih aset yang memberikan **imbal hasil tertinggi
pada tingkat risiko tertentu**, atau **risiko terendah pada tingkat
imbal hasil tertentu**.

**Koefisien Variasi (CV)** mengukur risiko per unit imbal hasil:

$$
CV = \frac{\sigma}{E(R)}
$$

CV yang lebih kecil berarti aset tersebut lebih efisien secara
risiko-imbal hasil.
""")

    st.info("""
🕌 **Fathonah — QS Luqman: 34**

*"Tiada seorang pun yang dapat mengetahui apa yang akan diusahakannya besok."*

Ayat ini mengingatkan bahwa masa depan mengandung ketidakpastian.
Pengukuran risiko (ragam dan simpangan baku) adalah ikhtiar cerdas
(*fathonah*) untuk memahami besarnya ketidakpastian itu sebelum
mengambil keputusan investasi.
""")


# ──────────────────────────────────────────────
# TAB HITUNG
# ──────────────────────────────────────────────
with tab_hitung:
    mode = st.radio(
        "Pilih jenis perhitungan:",
        ["📈 Imbal Hasil Terwujud (Data Historis)",
         "🎲 Imbal Hasil Harapan (Probabilitas)",
         "⚖️ Perbandingan Risiko-Imbal Hasil"],
        horizontal=True,
    )

    # ─── MODE 1: REALIZED RETURN ───
    if mode == "📈 Imbal Hasil Terwujud (Data Historis)":
        st.subheader("Imbal Hasil Terwujud dari Data Harga Historis")
        st.markdown("Masukkan data harga penutupan dan dividen per periode.")

        n_period = st.slider("Jumlah periode", 2, 20, 5)

        cols_head = st.columns([1, 1, 1])
        cols_head[0].markdown("**Periode**")
        cols_head[1].markdown("**Harga (Rp)**")
        cols_head[2].markdown("**Dividen (Rp)**")

        default_prices = [1000, 1050, 980, 1100, 1150, 1200, 1180, 1250, 1300, 1280,
                          1350, 1400, 1380, 1450, 1500, 1480, 1550, 1600, 1580, 1650]
        default_divs = [0, 25, 0, 30, 0, 25, 0, 30, 0, 25,
                        0, 30, 0, 25, 0, 30, 0, 25, 0, 30]

        prices = []
        dividends = []
        for i in range(n_period):
            c = st.columns([1, 1, 1])
            c[0].write(f"t = {i}")
            p = c[1].number_input(f"P_{i}", value=default_prices[i], min_value=1,
                                  key=f"p_{i}", label_visibility="collapsed")
            d = c[2].number_input(f"D_{i}", value=default_divs[i] if i > 0 else 0,
                                  min_value=0, key=f"d_{i}", label_visibility="collapsed")
            prices.append(p)
            dividends.append(d)

        if st.button("Hitung Imbal Hasil Terwujud", type="primary"):
            returns = []
            for t in range(1, n_period):
                r = (prices[t] - prices[t-1] + dividends[t]) / prices[t-1]
                returns.append(r)

            returns = np.array(returns)
            mean_r = np.mean(returns)
            var_r = np.var(returns, ddof=1)
            std_r = np.std(returns, ddof=1)
            cv = std_r / mean_r if mean_r != 0 else float('inf')

            st.markdown("### Hasil Perhitungan")

            # Show each period return
            cols_res = st.columns(min(len(returns), 5))
            for i, r in enumerate(returns):
                with cols_res[i % 5]:
                    color = "green" if r >= 0 else "red"
                    st.metric(f"R (t={i+1})", f"{r:.2%}")

            st.markdown("---")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Rata-rata Imbal Hasil", f"{mean_r:.4%}")
            c2.metric("Ragam (Variance)", f"{var_r:.6f}")
            c3.metric("Simpangan Baku (σ)", f"{std_r:.4%}")
            c4.metric("Koefisien Variasi (CV)", f"{cv:.4f}")

            with st.expander("📝 Langkah Perhitungan"):
                st.markdown("**Imbal hasil tiap periode:**")
                for t in range(1, n_period):
                    r = returns[t-1]
                    st.latex(
                        rf"R_{{{t}}} = \frac{{{prices[t]} - {prices[t-1]} + {dividends[t]}}}"
                        rf"{{{prices[t-1]}}} = {r:.4f} = {r:.2%}"
                    )
                st.markdown("**Rata-rata:**")
                sum_r = sum(returns)
                st.latex(
                    rf"\bar{{R}} = \frac{{{sum_r:.4f}}}{{{len(returns)}}} = {mean_r:.4f} = {mean_r:.2%}"
                )
                st.markdown("**Ragam (sampel):**")
                sum_sq = sum((r - mean_r)**2 for r in returns)
                st.latex(
                    rf"s^2 = \frac{{{sum_sq:.6f}}}{{{len(returns)}-1}} = {var_r:.6f}"
                )
                st.latex(rf"\sigma = \sqrt{{{var_r:.6f}}} = {std_r:.4f} = {std_r:.2%}")


    # ─── MODE 2: EXPECTED RETURN ───
    elif mode == "🎲 Imbal Hasil Harapan (Probabilitas)":
        st.subheader("Imbal Hasil Harapan dengan Skenario Probabilitas")
        st.markdown("Masukkan kondisi ekonomi, probabilitas, dan imbal hasil.")

        n_states = st.slider("Jumlah kondisi ekonomi", 2, 6, 3)

        defaults = [
            ("Resesi", 0.25, -0.10),
            ("Normal", 0.50, 0.12),
            ("Ekspansi", 0.25, 0.25),
            ("Boom", 0.00, 0.35),
            ("Krisis", 0.00, -0.30),
            ("Stagflasi", 0.00, -0.05),
        ]

        states = []
        probs = []
        rets = []

        for i in range(n_states):
            c = st.columns([2, 1, 1])
            nm = c[0].text_input(f"Kondisi {i+1}", value=defaults[i][0], key=f"nm_{i}")
            pr = c[1].number_input("Probabilitas", value=defaults[i][1],
                                   min_value=0.0, max_value=1.0, step=0.05, key=f"pr_{i}")
            rt = c[2].number_input("Imbal Hasil", value=defaults[i][2],
                                   min_value=-1.0, max_value=5.0, step=0.01,
                                   format="%.2f", key=f"rt_{i}")
            states.append(nm)
            probs.append(pr)
            rets.append(rt)

        total_prob = sum(probs)
        if abs(total_prob - 1.0) > 0.001:
            st.warning(f"⚠️ Total probabilitas = {total_prob:.3f} (seharusnya 1,000)")

        if st.button("Hitung Imbal Hasil Harapan", type="primary"):
            probs_arr = np.array(probs)
            rets_arr = np.array(rets)

            er = np.sum(probs_arr * rets_arr)
            var_e = np.sum(probs_arr * (rets_arr - er)**2)
            std_e = np.sqrt(var_e)
            cv_e = std_e / er if er != 0 else float('inf')

            st.markdown("### Hasil Perhitungan")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("E(R)", f"{er:.4%}")
            c2.metric("Ragam σ²", f"{var_e:.6f}")
            c3.metric("Simpangan Baku σ", f"{std_e:.4%}")
            c4.metric("Koefisien Variasi", f"{cv_e:.4f}")

            with st.expander("📝 Langkah Perhitungan"):
                st.markdown("**E(R) = Σ pᵢ × Rᵢ**")
                parts = []
                for i in range(n_states):
                    parts.append(f"({probs[i]:.2f} \\times {rets[i]:.2f})")
                st.latex(f"E(R) = {' + '.join(parts)} = {er:.4f} = {er:.2%}")

                st.markdown("**σ² = Σ pᵢ × (Rᵢ − E(R))²**")
                for i in range(n_states):
                    dev = rets[i] - er
                    st.latex(
                        rf"{states[i]}: {probs[i]:.2f} \times ({rets[i]:.2f} - {er:.4f})^2"
                        rf" = {probs[i]:.2f} \times {dev**2:.6f} = {probs[i] * dev**2:.6f}"
                    )
                st.latex(rf"\sigma^2 = {var_e:.6f}")
                st.latex(rf"\sigma = \sqrt{{{var_e:.6f}}} = {std_e:.4f} = {std_e:.2%}")

            # Bar chart
            fig = go.Figure()
            colors = ['#ef4444' if r < 0 else '#22c55e' for r in rets]
            fig.add_trace(go.Bar(
                x=states, y=[r * 100 for r in rets],
                marker_color=colors,
                text=[f"{r:.1%}" for r in rets],
                textposition='outside',
            ))
            fig.add_hline(y=er*100, line_dash="dash", line_color="blue",
                          annotation_text=f"E(R) = {er:.2%}")
            fig.update_layout(
                title="Imbal Hasil per Kondisi Ekonomi",
                yaxis_title="Imbal Hasil (%)",
                xaxis_title="Kondisi Ekonomi",
                showlegend=False,
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)


    # ─── MODE 3: RISK-RETURN COMPARISON ───
    else:
        st.subheader("Perbandingan Risiko–Imbal Hasil Beberapa Aset")
        st.markdown("Masukkan E(R) dan σ untuk beberapa aset.")

        n_assets = st.slider("Jumlah aset", 2, 8, 4)
        default_assets = [
            ("Deposito", 0.045, 0.005),
            ("Obligasi Negara", 0.07, 0.04),
            ("Saham LQ45", 0.14, 0.22),
            ("Saham Teknologi", 0.22, 0.38),
            ("Emas", 0.08, 0.15),
            ("Reksa Dana", 0.10, 0.12),
            ("Properti", 0.09, 0.10),
            ("Kripto", 0.30, 0.65),
        ]

        asset_names = []
        asset_er = []
        asset_std = []

        for i in range(n_assets):
            c = st.columns([2, 1, 1])
            nm = c[0].text_input(f"Aset {i+1}", value=default_assets[i][0], key=f"a_nm_{i}")
            er = c[1].number_input("E(R)", value=default_assets[i][1],
                                   min_value=-1.0, max_value=5.0, step=0.01,
                                   format="%.3f", key=f"a_er_{i}")
            sd = c[2].number_input("σ", value=default_assets[i][2],
                                   min_value=0.0, max_value=5.0, step=0.01,
                                   format="%.3f", key=f"a_sd_{i}")
            asset_names.append(nm)
            asset_er.append(er)
            asset_std.append(sd)

        if st.button("Tampilkan Grafik Risk–Return", type="primary"):
            st.markdown("### Grafik Risk–Return Tradeoff")

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[s*100 for s in asset_std],
                y=[e*100 for e in asset_er],
                mode='markers+text',
                text=asset_names,
                textposition='top center',
                marker=dict(size=14, color='#3b82f6'),
            ))
            fig.update_layout(
                xaxis_title="Risiko — Simpangan Baku σ (%)",
                yaxis_title="Imbal Hasil Harapan E(R) (%)",
                height=500,
                title="Risk–Return Tradeoff",
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Tabel Perbandingan")
            import pandas as pd
            df = pd.DataFrame({
                "Aset": asset_names,
                "E(R)": [f"{e:.2%}" for e in asset_er],
                "σ": [f"{s:.2%}" for s in asset_std],
                "CV": [f"{s/e:.4f}" if e != 0 else "∞"
                       for e, s in zip(asset_er, asset_std)],
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Find most efficient
            cvs = [s/e if e > 0 else float('inf') for e, s in zip(asset_er, asset_std)]
            best = np.argmin(cvs)
            st.success(
                f"✅ Aset paling efisien (CV terendah): **{asset_names[best]}** "
                f"dengan CV = {cvs[best]:.4f}"
            )
