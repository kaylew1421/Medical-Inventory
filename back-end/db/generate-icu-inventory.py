import csv
import random
from datetime import datetime, timedelta

# Categories with SKU prefixes and item lists from your examples
categories = {
    "Equipment": {
        "prefix": "EQP",
        "items": [
            "ICU Bed (Neuro Positioning)",
            "Ventilator (Neuro Settings)",
            "Cardiac Monitor (ECG)",
            "Defibrillator / AED",
            "Infusion Pump (IV and Syringe)",
            "Suction Machine",
            "Pulse Oximeter",
            "ICP Monitor & Transducers",
            "External Ventricular Drain (EVD Kit)",
            "Continuous EEG Machine & Electrodes",
            "Brain Tissue Oxygen Monitor",
            "Arterial Line Kit",
            "Central Venous Catheter Kit",
            "Endotracheal Tubes (various sizes)",
            "Nasogastric Tubes / Feeding Tubes",
            "Foley Catheters (various sizes)",
            "Lumbar Puncture Kit",
            "Head Immobilizer / Cervical Collar",
            "Cooling / Therapeutic Hypothermia Device",
            "Blood Gas Analyzer",
            "Portable Ultrasound Machine",
            "Neuromuscular Blockade Delivery Equip",
            "Oxygen Delivery Devices (Masks, Cannulas)",
            "Respiratory Humidifiers",
            "Blood Pressure Cuffs (all sizes)",
            "Additional Equipment 1",
            "Additional Equipment 2",
            "Additional Equipment 3",
            "Additional Equipment 4",
            "Additional Equipment 5",
            "Additional Equipment 6",
            "Additional Equipment 7",
            "Additional Equipment 8",
            "Additional Equipment 9",
            "Additional Equipment 10",
            "Additional Equipment 11",
            "Additional Equipment 12",
            "Additional Equipment 13",
            "Additional Equipment 14",
            "Additional Equipment 15"
        ]
    },
    "Consumable": {
        "prefix": "CON",
        "items": [
            "Sterile Gloves (various sizes)",
            "Non-sterile Gloves",
            "Surgical Face Masks (surgical, N95)",
            "Disposable Isolation Gowns",
            "Sterile Gauze Pads (multiple sizes)",
            "Non-sterile Gauze Pads",
            "Alcohol Prep Pads / Wipes",
            "Chlorhexidine Wipes",
            "Surgical Drapes and Towels",
            "Adhesive Surgical Tape (various widths)",
            "Transparent Film Dressings (Tegaderm)",
            "IV Cannulas (various gauges)",
            "Syringes (1ml, 3ml, 5ml, 10ml, 20ml, 60ml)",
            "Needles (various sizes)",
            "Sterile Water and Saline (vials, bags)",
            "IV Fluids (Normal Saline, LR, Dextrose)",
            "Suction Catheters (sterile)",
            "Endotracheal Tube Holders",
            "Feeding Syringes",
            "Specimen Containers (urine, sputum, blood culture)",
            "Sharps Disposal Containers",
            "Biohazard Waste Bags",
            "Bedpans and Urinals",
            "Oral Care Swabs and Suction Toothbrushes",
            "Blood Collection Tubes and Butterfly Needles",
            "Blood Tubing and IV Extension Sets",
            "Nebulizer Kits and Masks",
            "Tape Removers",
            "Cotton Balls and Cotton Tipped Applicators",
            "Disposable Thermometers and Covers",
            "Pressure Relief Mattress Covers or Overlays",
            "Additional Consumable 1",
            "Additional Consumable 2",
            "Additional Consumable 3",
            "Additional Consumable 4",
            "Additional Consumable 5",
            "Additional Consumable 6",
            "Additional Consumable 7",
            "Additional Consumable 8",
            "Additional Consumable 9",
            "Additional Consumable 10"
        ]
    },
    "Medication": {
        "prefix": "MED",
        "items": [
            "Propofol (Sedative)",
            "Midazolam (Sedative)",
            "Lorazepam (Sedative)",
            "Morphine (Analgesic)",
            "Fentanyl (Analgesic)",
            "Acetaminophen (Analgesic/Antipyretic)",
            "Norepinephrine (Vasopressor)",
            "Dopamine (Vasopressor)",
            "Phenylephrine (Vasopressor)",
            "Mannitol (Osmotic Diuretic)",
            "Hypertonic Saline (Osmotic Diuretic)",
            "Levetiracetam (Antiepileptic)",
            "Phenytoin (Antiepileptic)",
            "Valproate (Antiepileptic)",
            "Vecuronium (Neuromuscular Blocker)",
            "Cisatracurium (Neuromuscular Blocker)",
            "Acetaminophen (Antipyretic)",
            "Ibuprofen (Antipyretic)",
            "Dexamethasone (Corticosteroid)",
            "Hydrocortisone (Corticosteroid)",
            "Labetalol (Blood Pressure Med)",
            "Nicardipine (Blood Pressure Med)",
            "Heparin (Anticoagulant)",
            "Enoxaparin (Anticoagulant)",
            "Protamine (Heparin Reversal)",
            "Potassium Chloride (Electrolyte)",
            "Magnesium Sulfate (Electrolyte)",
            "Epinephrine (Emergency Med)",
            "Atropine (Emergency Med)",
            "Insulin",
            "Ranitidine (Gastric Protectant)",
            "Pantoprazole (Gastric Protectant)",
            "Broad Spectrum Antibiotics",
            "Targeted Antibiotics",
            "Thrombolytics",
            "Packed RBCs (Blood Product)",
            "Plasma (Blood Product)",
            "Platelets (Blood Product)",
            "Enteral Nutrition Formulas",
            "Parenteral Nutrition Formulas"
        ]
    },
    "Diagnostic": {
        "prefix": "LAB",
        "items": [
            "Blood Gas Analyzer Cartridges",
            "Glucometer Strips and Lancets",
            "Urine Test Strips",
            "Culture Swabs (Wound, Blood, Sputum)",
            "Lab Tubes and Labels",
            "Coagulation Testing Kits",
            "Blood Draw Supplies"
        ]
    },
    "Cleaning": {
        "prefix": "CLN",
        "items": [
            "Disinfectant Sprays and Wipes (Bleach, Alcohol)",
            "Hand Sanitizer (Alcohol Based)",
            "Mop Heads and Cleaning Cloths",
            "Laundry Bags for Soiled Linens",
            "Equipment Sterilization Wraps and Indicators"
        ]
    },
    "Misc": {
        "prefix": "MSC",
        "items": [
            "Patient Charts and Documentation Forms",
            "Clipboards and Pens",
            "Communication Devices (Call Buttons, Intercom)",
            "Batteries and Power Cords for Devices",
            "Positioning Pillows and Bolsters",
            "Emergency Airway Kits (Laryngoscopes, ET Tubes, Stylets)",
            "Specimen Transport Containers"
        ]
    }
}

def random_date(start_days=30, end_days=365):
    start = datetime.now() + timedelta(days=start_days)
    end = datetime.now() + timedelta(days=end_days)
    return start + (end - start) * random.random()

def generate_inventory_data():
    data = []
    for category, details in categories.items():
        prefix = details["prefix"]
        items = details["items"]
        for i, item_name in enumerate(items):
            sku = f"{prefix}-{i+1:03d}"
            quantity = random.randint(10, 200)
            reorder_threshold = max(5, int(quantity * 0.2))
            expiration_date = None
            if category in ["Medication", "Consumable", "Diagnostic"]:
                expiration_date = random_date().strftime("%Y-%m-%d")
            data.append({
                "SKU": sku,
                "Item Name": item_name,
                "Item Type": category,
                "Quantity": quantity,
                "Reorder Threshold": reorder_threshold,
                "Expiration Date": expiration_date if expiration_date else ""
            })
    return data

def save_to_csv(data, filename="icu_inventory_mock.csv"):
    fieldnames = ["SKU", "Item Name", "Item Type", "Quantity", "Reorder Threshold", "Expiration Date"]
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    inventory_data = generate_inventory_data()
    save_to_csv(inventory_data)
    print(f"Generated {len(inventory_data)} inventory items in icu_inventory_mock.csv")
