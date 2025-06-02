import streamlit as st
import requests

st.title("🍎 Nährstoffanalyse deiner Ernährung")

# Benutzer-Eingabe
lebensmittel = st.text_input("Gib ein Lebensmittel ein (z. B. 'Banane'):")
menge = st.number_input("Menge in Gramm:", min_value=1, step=1)

# Funktion zur Abfrage der Open Food Facts API
def get_nutrition_data(query):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["count"] > 0:
            return data["products"][0]  # Nimmt das erste gefundene Produkt
    return None

if st.button("Analyse starten"):
    if lebensmittel:
        produkt = get_nutrition_data(lebensmittel)
        if produkt:
            st.subheader(f"Nährwertangaben für {produkt.get('product_name', 'unbekannt')}")
            nutriments = produkt.get("nutriments", {})
            faktor = menge / 100  # Umrechnung auf die eingegebene Menge

            # Liste der anzuzeigenden Nährstoffe
            naehrstoffe = {
                "energy-kcal": "Kalorien (kcal)",
                "proteins": "Proteine (g)",
                "carbohydrates": "Kohlenhydrate (g)",
                "sugars": "Zucker (g)",
                "fat": "Fett (g)",
                "saturated-fat": "Gesättigte Fettsäuren (g)",
                "fiber": "Ballaststoffe (g)",
                "sodium": "Natrium (mg)",
                "salt": "Salz (g)"
            }

            for schluessel, name in naehrstoffe.items():
                wert = nutriments.get(schluessel)
                if wert is not None:
                    st.write(f"{name}: {wert * faktor:.2f}")
        else:
            st.warning("Lebensmittel nicht gefunden. Bitte überprüfe die Eingabe.")
    else:
        st.warning("Bitte gib ein Lebensmittel ein.")
