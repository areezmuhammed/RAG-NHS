import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "smpc"

# Sample Content
WARFARIN_CONTENT = """
WARFARIN SODIUM 5MG TABLETS - SUMMARY OF PRODUCT CHARACTERISTICS

1. INDICATIONS
Prophylaxis and treatment of venous thrombosis and its extension, and pulmonary embolism.
Prophylaxis and treatment of thromboembolic complications associated with atrial fibrillation and/or cardiac valve replacement.

2. CONTRAINDICATIONS
Pregnancy: Warfarin is contraindicated in women who are or may become pregnant because the drug passes through the placental barrier and may cause fatal hemorrhage to the fetus in utero.

3. DRUG INTERACTIONS
ASPIRIN: Concomitant use of aspirin and warfarin significantly increases the risk of major bleeding. Aspirin inhibits platelet aggregation while warfarin inhibits clotting factors. High-potency synergistic effect.
NSAIDs: Avoid ibuprofen and other NSAIDs where possible as they increase bleeding risk through gastric mucosal irritation and antiplatelet effects.
ANTIBIOTICS: Many broad-spectrum antibiotics (e.g., amoxicillin, clarithromycin) may increase the effect of warfarin by reducing vitamin K-producing gut flora. Monitor INR closely.

4. SEVERITY: MAJOR / HIGH RISK
Concomitant use with other anticoagulants or antiplatelets is considered a high-severity interaction requiring strict clinical monitoring.
"""

ASPIRIN_CONTENT = """
ASPIRIN 75MG DISPERSIBLE TABLETS - SUMMARY OF PRODUCT CHARACTERISTICS

1. INDICATIONS
Secondary prevention of thrombotic cerebrovascular or cardiovascular disease.

2. DRUG INTERACTIONS
WARFARIN: Major interaction. Increased risk of life-threatening hemorrhage. 
CLOPIDOGREL: Synergistic antiplatelet effect; used intentionally in some cardiac cases but increases bleeding risk.
SSRIs (e.g., Sertraline): Increased risk of upper gastrointestinal bleeding. Use with caution.

3. MONITORING
Monitor for signs of GI bleeding, bruising, and dark stools.
"""

def seed_data():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create Warfarin file
    with open(RAW_DATA_DIR / "warfarin_smpc.txt", "w") as f:
        f.write(WARFARIN_CONTENT)
        
    # Create Aspirin file
    with open(RAW_DATA_DIR / "aspirin_smpc.txt", "w") as f:
        f.write(ASPIRIN_CONTENT)
        
    print(f"Sample data seeded in {RAW_DATA_DIR}")

if __name__ == "__main__":
    seed_data()
