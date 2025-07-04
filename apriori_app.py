import streamlit as st
import requests

API_URL = "http://localhost:5000"

st.set_page_config(page_title="Apriori Hukum Tajwid", layout="wide")
st.title("Apriori: Pola Hukum Tajwid")

# --- SIDEBAR INPUT DATA ---
st.sidebar.header("Tambah Data Ayat")
with st.sidebar.form(key="form_input"):
    hukum_input = st.text_input("List hukum tajwid (pisahkan dengan koma)", "")
    submit = st.form_submit_button("Tambah")

if submit and hukum_input:
    items = [x.strip() for x in hukum_input.split(",") if x.strip()]
    res = requests.post(f"{API_URL}/dataset", json=items)
    if res.status_code == 200:
        st.sidebar.success("Transaksi berhasil ditambahkan")

# --- TAMPILKAN DATASET ---
st.subheader("Dataset Hukum Tajwid")
dataset_res = requests.get(f"{API_URL}/dataset")

if dataset_res.ok:
    dataset = dataset_res.json()
    for idx, trans in enumerate(dataset):
        col1, col2 = st.columns([5, 2])
        with col1:
            st.markdown(f"**{idx+1}.** {', '.join(trans)}")
        with col2:
            # Hapus tombol Edit, hanya tampilkan tombol Hapus
            if st.button("Hapus", key=f"del-{idx}"):
                requests.delete(f"{API_URL}/dataset/{idx}")
                st.experimental_rerun()


# --- PARAMETER & PROSES APRIORI ---
st.subheader("Proses Apriori")
min_support = st.number_input("Minimum Support", min_value=0.01, max_value=1.0, value=0.3, step=0.01)
min_confidence = st.number_input("Minimum Confidence", min_value=0.01, max_value=1.0, value=0.6, step=0.01)

if st.button("Generate Rules"):
    rule_req = {
        "min_support": min_support,
        "min_confidence": min_confidence
    }
    res = requests.post(f"{API_URL}/rules", json=rule_req)
    if res.status_code == 200 and res.json():
        rules = res.json()
        st.success(f"{len(rules)} aturan ditemukan.")
        for i, rule in enumerate(rules):
            st.write(f"**{i+1}.** Jika `{' + '.join(rule['antecedents'])}` → Maka `{' + '.join(rule['consequents'])}`")
            st.caption(f"Support: {rule['support']:.2f}, Confidence: {rule['confidence']:.2f}, Lift: {rule['lift']:.2f}")
    else:
        st.warning("Tidak ditemukan aturan atau dataset masih kosong.")