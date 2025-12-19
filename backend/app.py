# Import Flask and required modules
from flask import Flask, render_template, request

# Create Flask application instance
app = Flask(__name__)

def get_drug_recommendation(patient_data):
    """
    Simple rule-based drug recommendation logic
    This will be replaced with ML model later
    """
    
    age = int(patient_data.get('age', 0))
    symptoms = patient_data.get('symptoms', [])
    conditions = patient_data.get('conditions', [])
    creatinine = patient_data.get('creatinine')
    allergies = patient_data.get('allergies', '').lower()
    blood_sugar = patient_data.get('blood_sugar')
    
    # Initialize recommendation dictionary
    recommendation = {
        'drug_name': '',
        'dosage': '',
        'alternatives': [],
        'warnings': [],
        'reason': '',
        'precautions': []
    }
    
    # Check for kidney issues
    has_kidney_issue = 'kidney_disease' in conditions
    if creatinine and float(creatinine) > 1.5:
        has_kidney_issue = True
        recommendation['warnings'].append('⚠️ Elevated creatinine detected - Kidney function impaired')
    
    # Check for liver issues
    has_liver_issue = 'liver_disease' in conditions
    
    # Check for diabetes
    has_diabetes = 'diabetes' in conditions
    if blood_sugar and float(blood_sugar) > 126:
        has_diabetes = True
    
    # Rule 1: Fever treatment
    if 'fever' in symptoms:
        if has_kidney_issue:
            recommendation['drug_name'] = 'Paracetamol'
            recommendation['dosage'] = '500mg every 6 hours (max 3g/day for kidney patients)'
            recommendation['alternatives'] = ['Paracetamol 650mg', 'Acetaminophen']
            recommendation['warnings'].append('⚠️ NSAIDs avoided due to kidney issues')
            recommendation['reason'] = 'Paracetamol is the safest antipyretic for patients with kidney disease'
            recommendation['precautions'].append('Monitor temperature every 4 hours')
            recommendation['precautions'].append('Ensure adequate hydration')
        elif has_liver_issue:
            recommendation['drug_name'] = 'Ibuprofen'
            recommendation['dosage'] = '400mg every 8 hours with food'
            recommendation['alternatives'] = ['Aspirin 325mg']
            recommendation['warnings'].append('⚠️ Paracetamol avoided due to liver disease')
            recommendation['reason'] = 'NSAIDs are safer for liver disease patients'
            recommendation['precautions'].append('Take with food to prevent gastric irritation')
        elif 'nsaid' in allergies or 'ibuprofen' in allergies:
            recommendation['drug_name'] = 'Paracetamol'
            recommendation['dosage'] = '500mg every 6 hours (max 4g/day)'
            recommendation['alternatives'] = ['Paracetamol 650mg']
            recommendation['warnings'].append('⚠️ Patient allergic to NSAIDs')
            recommendation['reason'] = 'Paracetamol chosen due to documented NSAID allergy'
            recommendation['precautions'].append('Avoid combination with other paracetamol products')
        else:
            recommendation['drug_name'] = 'Ibuprofen'
            recommendation['dosage'] = '400mg every 8 hours with food'
            recommendation['alternatives'] = ['Paracetamol 500mg', 'Aspirin 325mg', 'Naproxen 250mg']
            recommendation['reason'] = 'Standard fever treatment with anti-inflammatory effect'
            recommendation['precautions'].append('Take after meals')
            recommendation['precautions'].append('Avoid if stomach ulcer history')
    
    # Rule 2: Joint pain treatment
    elif 'joint_pain' in symptoms:
        if has_kidney_issue:
            recommendation['drug_name'] = 'Paracetamol'
            recommendation['dosage'] = '650mg every 8 hours'
            recommendation['alternatives'] = ['Topical Diclofenac gel', 'Capsaicin cream']
            recommendation['warnings'].append('⚠️ NSAIDs contraindicated due to kidney dysfunction')
            recommendation['reason'] = 'Paracetamol provides pain relief without kidney toxicity'
            recommendation['precautions'].append('Consider physiotherapy')
            recommendation['precautions'].append('Apply hot/cold compress')
        elif age > 65:
            recommendation['drug_name'] = 'Paracetamol'
            recommendation['dosage'] = '500mg every 8 hours'
            recommendation['alternatives'] = ['Topical Diclofenac gel', 'Low-dose Ibuprofen 200mg']
            recommendation['warnings'].append('⚠️ Elderly patient - reduced NSAID use recommended')
            recommendation['reason'] = 'Lower risk pain management for elderly patients to prevent GI bleeding'
            recommendation['precautions'].append('Monitor for side effects closely')
            recommendation['precautions'].append('Use minimum effective dose')
        else:
            recommendation['drug_name'] = 'Ibuprofen'
            recommendation['dosage'] = '400mg every 8 hours with food'
            recommendation['alternatives'] = ['Naproxen 250mg', 'Diclofenac 50mg', 'Paracetamol 650mg']
            recommendation['reason'] = 'Effective NSAID for inflammatory joint pain'
            recommendation['precautions'].append('Take with food or milk')
            recommendation['precautions'].append('Avoid alcohol')
    
    # Rule 3: Headache treatment
    elif 'headache' in symptoms:
        if 'aspirin' in allergies:
            recommendation['drug_name'] = 'Paracetamol'
            recommendation['dosage'] = '500mg every 6 hours as needed'
            recommendation['alternatives'] = ['Ibuprofen 200mg']
            recommendation['warnings'].append('⚠️ Aspirin allergy documented')
            recommendation['reason'] = 'Safe alternative to aspirin for headache relief'
            recommendation['precautions'].append('Rest in dark, quiet room')
        else:
            recommendation['drug_name'] = 'Aspirin'
            recommendation['dosage'] = '325mg every 6 hours'
            recommendation['alternatives'] = ['Paracetamol 500mg', 'Ibuprofen 200mg']
            recommendation['reason'] = 'Effective first-line treatment for mild to moderate headache'
            recommendation['precautions'].append('Avoid on empty stomach')
            recommendation['precautions'].append('Stay hydrated')
    
    # Rule 4: Cough treatment
    elif 'cough' in symptoms:
        if 'asthma' in conditions:
            recommendation['drug_name'] = 'Dextromethorphan'
            recommendation['dosage'] = '15mg syrup every 8 hours'
            recommendation['alternatives'] = ['Guaifenesin syrup', 'Honey with warm water']
            recommendation['warnings'].append('⚠️ Asthma patient - codeine-based suppressants avoided')
            recommendation['reason'] = 'Non-opioid cough suppressant safe for asthma patients'
            recommendation['precautions'].append('Use inhaler as prescribed')
            recommendation['precautions'].append('Monitor breathing difficulty')
        else:
            recommendation['drug_name'] = 'Dextromethorphan'
            recommendation['dosage'] = '15mg syrup every 8 hours'
            recommendation['alternatives'] = ['Guaifenesin expectorant', 'Honey-based syrup']
            recommendation['reason'] = 'Standard cough suppressant for dry cough'
            recommendation['precautions'].append('Drink plenty of fluids')
            recommendation['precautions'].append('Avoid if cough produces thick mucus')
    
    # Rule 5: Nausea treatment
    elif 'nausea' in symptoms:
        recommendation['drug_name'] = 'Ondansetron'
        recommendation['dosage'] = '4mg tablet, dissolve on tongue'
        recommendation['alternatives'] = ['Metoclopramide 10mg', 'Ginger tea']
        recommendation['reason'] = 'Effective antiemetic with minimal side effects'
        recommendation['precautions'].append('Take 30 minutes before meals')
        recommendation['precautions'].append('Avoid heavy, greasy foods')
        if has_liver_issue:
            recommendation['warnings'].append('⚠️ Use lower dose in liver disease')
    
    # Rule 6: Chest pain - requires immediate attention
    elif 'chest_pain' in symptoms:
        recommendation['drug_name'] = '🚨 EMERGENCY CONSULTATION REQUIRED'
        recommendation['dosage'] = 'DO NOT SELF-MEDICATE'
        recommendation['alternatives'] = []
        recommendation['warnings'].append('🚨 CRITICAL: Chest pain requires immediate medical evaluation')
        recommendation['warnings'].append('⚠️ Rule out cardiac emergency (heart attack)')
        recommendation['reason'] = 'Chest pain is a potentially life-threatening symptom'
        recommendation['precautions'].append('Seek emergency medical care immediately')
        recommendation['precautions'].append('Call emergency services or visit ER')
        recommendation['precautions'].append('Do not drive yourself')
    
    # Rule 7: Dizziness
    elif 'dizziness' in symptoms:
        recommendation['drug_name'] = 'Betahistine'
        recommendation['dosage'] = '16mg three times daily with food'
        recommendation['alternatives'] = ['Meclizine 25mg', 'Rest and hydration']
        recommendation['reason'] = 'Helps with vertigo and balance issues'
        recommendation['precautions'].append('Avoid sudden position changes')
        recommendation['precautions'].append('Stay seated if dizziness worsens')
        if 'hypertension' in conditions:
            recommendation['warnings'].append('⚠️ Check blood pressure - may be cause of dizziness')
    
    # Default: No clear symptoms or multiple complex symptoms
    else:
        recommendation['drug_name'] = '🔍 Detailed Consultation Required'
        recommendation['dosage'] = 'N/A'
        recommendation['alternatives'] = []
        recommendation['warnings'].append('⚠️ Symptoms unclear or require detailed physical examination')
        recommendation['warnings'].append('⚠️ Multiple symptoms may indicate complex condition')
        recommendation['reason'] = 'Further medical evaluation needed for proper diagnosis and treatment'
        recommendation['precautions'].append('Schedule appointment with physician')
        recommendation['precautions'].append('Bring all current medications to consultation')
    
    # General age-related warnings
    if age > 70:
        recommendation['warnings'].append('⚠️ Elderly patient - increased risk of side effects and drug interactions')
        recommendation['precautions'].append('Start with lowest effective dose')
    
    if age < 12:
        recommendation['warnings'].append('⚠️ Pediatric patient - dosage must be weight-adjusted')
        recommendation['precautions'].append('Consult pediatrician for exact dosing')
    
    # Kidney function warnings
    if creatinine:
        creat_val = float(creatinine)
        if creat_val > 1.3:
            recommendation['warnings'].append('⚠️ Elevated creatinine - kidney function monitoring required')
            recommendation['precautions'].append('Regular kidney function tests advised')
    
    # Diabetes warnings
    if has_diabetes:
        recommendation['precautions'].append('Monitor blood sugar levels regularly')
        if blood_sugar and float(blood_sugar) > 180:
            recommendation['warnings'].append('⚠️ High blood sugar detected - review diabetes management')
    
    # Interaction checks with current medications
    current_meds = patient_data.get('current_meds', '').lower()
    if current_meds:
        if 'warfarin' in current_meds or 'blood thinner' in current_meds:
            recommendation['warnings'].append('⚠️ CRITICAL: Patient on blood thinners - avoid NSAIDs and Aspirin')
        if 'metformin' in current_meds and has_kidney_issue:
            recommendation['warnings'].append('⚠️ Metformin + kidney disease - review with doctor immediately')
    
    return recommendation


# Route for home page (GET request)
@app.route('/')
def home():
    """Display the patient information form"""
    return render_template('index.html')


# Route to handle form submission (POST request)
@app.route('/recommend', methods=['POST'])
def recommend():
    """Process form data and return drug recommendation"""
    
    # Collect all patient data from form
    patient_data = {
        'age': request.form.get('age'),
        'gender': request.form.get('gender'),
        'weight': request.form.get('weight'),
        'symptoms': request.form.getlist('symptoms'),
        'conditions': request.form.getlist('conditions'),
        'allergies': request.form.get('allergies', ''),
        'current_meds': request.form.get('current_meds', ''),
        'blood_sugar': request.form.get('blood_sugar'),
        'creatinine': request.form.get('creatinine'),
        'blood_pressure': request.form.get('blood_pressure'),
        'hemoglobin': request.form.get('hemoglobin')
    }
    
    # Log received data (for debugging)
    print("\n=== Patient Data Received ===")
    print(f"Age: {patient_data['age']}, Gender: {patient_data['gender']}")
    print(f"Symptoms: {patient_data['symptoms']}")
    print(f"Conditions: {patient_data['conditions']}")
    print(f"Allergies: {patient_data['allergies']}")
    print(f"Current Meds: {patient_data['current_meds']}")
    print(f"Lab Values - Creatinine: {patient_data['creatinine']}, Blood Sugar: {patient_data['blood_sugar']}")
    print("============================\n")
    
    # Get recommendation from rule engine
    recommendation = get_drug_recommendation(patient_data)
    
    # Render result page with data
    return render_template('result.html', 
                          patient=patient_data, 
                          recommendation=recommendation)


# Run the Flask application
if __name__ == '__main__':
    # debug=True: Shows detailed errors and auto-reloads on code changes
    # port=5000: Application runs on http://localhost:5000
    app.run(debug=True, port=5000)
