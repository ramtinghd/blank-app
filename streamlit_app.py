import streamlit as st
import requests
import pandas as pd

st.title("🍏 Nährstoffanalyse mit Open Food Facts")

# Session-State initialisieren
if "lebensmittel_liste" not in st.session_state:
    st.session_state.lebensmittel_liste = []

# Eingabemaske für Lebensmittel
lebensmittel = st.text_input("Gib ein Lebensmittel ein (z. B. 'Banane'):")
menge = st.number_input("Menge in Gramm:", min_value=1, step=1)

# Funktion: Open Food Facts API abfragen
def get_nutrition_data(query):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["count"] > 0:
            return data["products"][0]  # Das erste Produkt zurückgeben
    return None

# Nährstoffe, die wir analysieren (Mineralstoffe & Vitamine)
naehrstoffe = {
    "energy-kcal": "Kalorien (kcal)",
    "proteins": "Proteine (g)",
    "carbohydrates": "Kohlenhydrate (g)",
    "sugars": "Zucker (g)",
    "fat": "Fett (g)",
    "saturated-fat": "Gesättigte Fettsäuren (g)",
    "fiber": "Ballaststoffe (g)",
    "sodium": "Natrium (mg)",
    "salt": "Salz (g)",
    "vitamin-a": "Vitamin A (µg)",
    "vitamin-c": "Vitamin C (mg)",
    "calcium": "Calcium (mg)",
    "iron": "Eisen (mg)",
    "magnesium": "Magnesium (mg)",
    "potassium": "Kalium (mg)"
}

# Wenn Button gedrückt
if st.button("Lebensmittel hinzufügen"):
    if lebensmittel:
        produkt = get_nutrition_data(lebensmittel)
        if produkt:
            name = produkt.get("product_name", lebensmittel)
            nutriments = produkt.get("nutriments", {})
            st.session_state.lebensmittel_liste.append({
                "name": name,
                "menge": menge,
                "nutriments": nutriments
            })
        else:
            st.warning("Lebensmittel nicht gefunden.")
    else:
        st.warning("Bitte gib ein Lebensmittel ein.")

# Liste anzeigen
if st.session_state.lebensmittel_liste:
    st.subheader("📋 Aufgenommene Lebensmittel:")
    for eintrag in st.session_state.lebensmittel_liste:
        st.write(f"- {eintrag['menge']}g {eintrag['name']}")

    # Gesamtauswertung vorbereiten
    gesamt = {}
    for eintrag in st.session_state.lebensmittel_liste:
        menge = eintrag["menge"]
        nutriments = eintrag["nutriments"]
        faktor = menge / 100
        for schluessel, label in naehrstoffe.items():
            wert = nutriments.get(schluessel)
            if wert:
                gesamt[label] = gesamt.get(label, 0) + wert * faktor

    # Gesamtübersicht anzeigen
    st.subheader("📊 Gesamt-Nährstoffaufnahme:")
    df = pd.DataFrame(gesamt.items(), columns=["Nährstoff", "Aufnahme"])
    df["Aufnahme"] = df["Aufnahme"].round(2)
    st.dataframe(df)

    # Download-Button (optional)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSV herunterladen", csv, "naehrstoffanalyse.csv", "text/csv")

# Reset-Button
if st.button("Daten zurücksetzen"):
    st.session_state.lebensmittel_liste = []

