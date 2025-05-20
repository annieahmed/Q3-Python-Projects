import streamlit as st
import random
import os



class Medicine:
    def __init__(self, name, used_for, dosage_adult, dosage_child, image_path=None):
        self.name = name
        self.used_for = used_for
        self.dosage_adult = dosage_adult
        self.dosage_child = dosage_child
        self.image_path = image_path

    def matches_symptom(self, symptom):
        return symptom.lower() in [s.lower() for s in self.used_for]

    def get_dosage_by_age(self, age):
        return self.dosage_adult if age >= 12 else self.dosage_child


class Symptom:
    def __init__(self, name):
        self.name = name.lower().strip()

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.symptoms = []

    def add_symptom(self, symptom):
        self.symptoms.append(symptom)

# ========== Medicine Data ==========

def get_image_path(name):
    filename = f"images/{name.lower().replace(' ', '_')}.jpg"
    return filename if os.path.exists(filename) else None

medicines = [
    Medicine("Paracetamol", ["fever", "headache", "body pain"], "500mg (Adult)", "250mg (Child)", get_image_path("paracetamol")),
    Medicine("Ibuprofen", ["inflammation", "body pain", "fever"], "200mg every 6 hrs (Adult)", "100mg every 6 hrs (Child)", get_image_path("ibuprofen")),
    Medicine("Cetirizine", ["allergy", "sneezing", "runny nose"], "10mg at night (Adult)", "5mg at night (Child)", get_image_path("cetirizine")),
    Medicine("Loratadine", ["allergy", "itchy eyes", "runny nose"], "10mg once daily (Adult)", "5mg once daily (Child)", get_image_path("loratadine")),
    Medicine("Dextromethorphan", ["dry cough"], "20mg every 6 hrs (Adult)", "10mg every 6 hrs (Child)", get_image_path("dextromethorphan")),
    Medicine("Salbutamol", ["asthma", "wheezing"], "2 puffs as needed (Adult)", "1 puff as needed (Child)", get_image_path("salbutamol")),
    Medicine("Omeprazole", ["acid reflux", "stomach pain"], "20mg before meal (Adult)", "10mg before meal (Child)", get_image_path("omeprazole")),
    Medicine("ORS Solution", ["dehydration", "diarrhea"], "1 sachet in water after each stool (Adult)", "½ sachet (Child)", get_image_path("ors_solution")),
    Medicine("Clotrimazole", ["fungal infection", "itching"], "Apply twice daily (Adult)", "Apply once daily (Child)", get_image_path("clotrimazole")),
    Medicine("Zinc Supplement", ["diarrhea", "weak immunity"], "20mg daily for 10 days (Adult)", "10mg daily (Child)", get_image_path("zinc_supplement")),
]

# ========== UI Config ==========

st.set_page_config(page_title="MediGuide", layout="wide")
st.title("🩺 MediGuide - Smart Medicine Recommender")

# ========== Sidebar ==========

with st.sidebar:
    st.header("🔍 Check Your Symptoms")
    name = st.text_input("👤 Your Name")
    age = st.number_input("🎂 Your Age", min_value=0, max_value=120, step=1)
    symptom_input = st.text_input("💬 Enter Symptoms (comma separated)")
    submit = st.button("🚀 Get Suggestions")

# ========== Logic ==========

if submit and name and age and symptom_input:
    user = User(name, age)
    symptoms = [Symptom(s.strip()) for s in symptom_input.split(",") if s.strip()]

    matched = []
    for med in medicines:
        for symptom in symptoms:
            if med.matches_symptom(symptom.name):
                matched.append(med)
                break

    if matched:
        st.subheader(f"👋 Hi {name}, here are your medicine suggestions:")
        cols = st.columns(2)
        for i, med in enumerate(matched):
            with cols[i % 2]:
                if med.image_path:
                    st.image(med.image_path, use_column_width=True)
                st.markdown(f"### 💊 {med.name}")
                st.markdown(f"**Dosage (Age {user.age}):** {med.get_dosage_by_age(user.age)}")
                st.markdown("---")
    else:
        st.warning("😕 Sorry, no medicines found for your symptoms.")
