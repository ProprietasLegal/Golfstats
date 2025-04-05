import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Golf Scorecard", layout="wide")
st.title("🏌️ Encodage Partie de Golf")

# Initialiser les données
if "scorecard" not in st.session_state:
    st.session_state.scorecard = pd.DataFrame([{
        "Trou": i+1, "Par": "", "Coups": "", "Putts": "", "Club 1": "", "Club 2": ""
    } for i in range(18)])

df = st.session_state.scorecard

# Formulaire
st.subheader("➡️ Encodage trou par trou")
edited_df = st.data_editor(df, num_rows="fixed", use_container_width=True)
st.session_state.scorecard = edited_df

# Statistiques simples
st.subheader("📊 Statistiques")
if edited_df["Coups"].apply(lambda x: str(x).isdigit()).any():
    edited_df["Coups"] = pd.to_numeric(edited_df["Coups"], errors="coerce")
    edited_df["Putts"] = pd.to_numeric(edited_df["Putts"], errors="coerce")

    st.write("**Total de coups :**", int(edited_df["Coups"].sum(skipna=True)))
    st.write("**Putts moyens par trou :**", round(edited_df["Putts"].mean(skipna=True), 2))
    st.write("**Score brut :**", int(edited_df["Coups"].sum(skipna=True)))

# Export Excel
st.subheader("📤 Exporter les données")
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
    edited_df.to_excel(writer, sheet_name="Scorecard", index=False)
    writer.save()
    st.download_button(
        label="📥 Télécharger le fichier Excel",
        data=buffer,
        file_name="golf_scorecard.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
