"""
Enhanced Medical Knowledge Service for Clang AI
Comprehensive medical information system with symptoms, treatments, medications, and drug information
"""

import sqlite3
import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

class MedicalKnowledgeService:
    """
    Advanced Medical Knowledge System providing:
    - Disease symptoms and diagnosis
    - Treatment recommendations
    - Medication information
    - Drug interactions and side effects
    - First aid guidance
    - Health monitoring
    """
    
    def __init__(self):
        self.db_path = 'medical_knowledge.db'
        self.initialize_medical_database()
        print("🏥 Medical Knowledge Service initialized")
    
    def initialize_medical_database(self):
        """Initialize comprehensive medical knowledge database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create medical conditions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_conditions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                condition_name TEXT UNIQUE,
                category TEXT,
                symptoms TEXT,
                causes TEXT,
                treatments TEXT,
                medications TEXT,
                severity_level TEXT,
                prevention TEXT,
                when_to_see_doctor TEXT,
                complications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create medications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drug_name TEXT UNIQUE,
                generic_name TEXT,
                brand_names TEXT,
                drug_class TEXT,
                indication TEXT,
                dosage_forms TEXT,
                common_dosages TEXT,
                side_effects TEXT,
                contraindications TEXT,
                interactions TEXT,
                pregnancy_category TEXT,
                mechanism_of_action TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create first aid table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS first_aid (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emergency_type TEXT UNIQUE,
                immediate_steps TEXT,
                things_to_avoid TEXT,
                when_to_call_911 TEXT,
                materials_needed TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Populate with comprehensive medical data
        self._populate_medical_conditions(cursor)
        self._populate_medications(cursor)
        self._populate_first_aid(cursor)
        
        conn.commit()
        conn.close()
        print("✅ Medical database initialized with comprehensive data")
    
    def _populate_medical_conditions(self, cursor):
        """Populate database with medical conditions"""
        conditions = [
            {
                'condition_name': 'Dengue Fever',
                'category': 'Infectious Disease',
                'symptoms': 'High fever (104-106°F), severe joint pain, skin rash, swollen lymph nodes, nausea, vomiting, fatigue, severe headache, eye pain',
                'causes': 'Dengue virus transmitted by Aedes mosquitoes',
                'treatments': 'Rest, fluid replacement, fever management, platelet monitoring, hospitalization for severe cases',
                'medications': 'Paracetamol (acetaminophen) for fever, avoid aspirin and ibuprofen, IV fluids for dehydration',
                'severity_level': 'Moderate to Severe',
                'prevention': 'Mosquito control, eliminate standing water, use mosquito repellent, wear long sleeves',
                'when_to_see_doctor': 'High fever lasting more than 2 days, severe abdominal pain, bleeding, difficulty breathing',
                'complications': 'Dengue hemorrhagic fever, dengue shock syndrome, organ failure'
            },
            {
                'condition_name': 'Diabetes Type 2',
                'category': 'Endocrine Disorder',
                'symptoms': 'Increased thirst, frequent urination, unexplained weight loss, fatigue, blurred vision, slow healing wounds',
                'causes': 'Insulin resistance, genetics, obesity, sedentary lifestyle, age',
                'treatments': 'Lifestyle modification, diet control, regular exercise, blood glucose monitoring, medication management',
                'medications': 'Metformin, Glipizide, Insulin (if needed), Januvia (sitagliptin), Jardiance (empagliflozin)',
                'severity_level': 'Chronic - Manageable',
                'prevention': 'Healthy diet, regular exercise, weight management, regular health checkups',
                'when_to_see_doctor': 'Blood sugar over 300 mg/dL, signs of ketoacidosis, severe hypoglycemia',
                'complications': 'Heart disease, kidney damage, nerve damage, eye problems, foot problems'
            },
            {
                'condition_name': 'Hypertension',
                'category': 'Cardiovascular',
                'symptoms': 'Often asymptomatic, headaches, dizziness, chest pain, shortness of breath, nosebleeds',
                'causes': 'Unknown (primary), kidney disease, sleep apnea, thyroid problems, stress, obesity',
                'treatments': 'Lifestyle changes, regular exercise, salt reduction, stress management, medication',
                'medications': 'Lisinopril (ACE inhibitor), Amlodipine (calcium channel blocker), Metoprolol (beta blocker), Hydrochlorothiazide (diuretic)',
                'severity_level': 'Moderate - Requires Management',
                'prevention': 'Low sodium diet, regular exercise, weight management, limit alcohol, quit smoking',
                'when_to_see_doctor': 'BP over 180/120, chest pain, severe headache, vision changes',
                'complications': 'Heart attack, stroke, kidney failure, aneurysm, heart failure'
            },
            {
                'condition_name': 'Common Cold',
                'category': 'Respiratory',
                'symptoms': 'Runny nose, congestion, sore throat, cough, sneezing, mild fever, fatigue',
                'causes': 'Viral infection (rhinovirus, coronavirus, others)',
                'treatments': 'Rest, fluids, throat lozenges, humidifier, saline nasal rinse',
                'medications': 'Acetaminophen or ibuprofen for aches, decongestants (pseudoephedrine), cough suppressants (dextromethorphan)',
                'severity_level': 'Mild',
                'prevention': 'Hand washing, avoid close contact with sick people, don\'t touch face',
                'when_to_see_doctor': 'Fever over 101.3°F, symptoms worsen after 10 days, severe headache, chest pain',
                'complications': 'Secondary bacterial infections, sinusitis, ear infections'
            },
            {
                'condition_name': 'Migraine',
                'category': 'Neurological',
                'symptoms': 'Severe headache, nausea, vomiting, sensitivity to light and sound, visual aura',
                'causes': 'Genetics, hormonal changes, stress, certain foods, sleep changes, weather changes',
                'treatments': 'Rest in dark room, cold compress, relaxation techniques, trigger avoidance',
                'medications': 'Sumatriptan (Imitrex), Rizatriptan (Maxalt), Propranolol (prevention), Topiramate (prevention)',
                'severity_level': 'Moderate to Severe',
                'prevention': 'Identify triggers, regular sleep schedule, stress management, regular meals',
                'when_to_see_doctor': 'Sudden severe headache, fever with headache, confusion, vision changes',
                'complications': 'Chronic migraine, medication overuse headache, status migrainosus'
            },
            {
                'condition_name': 'Gastroenteritis',
                'category': 'Gastrointestinal',
                'symptoms': 'Diarrhea, nausea, vomiting, abdominal cramps, fever, dehydration',
                'causes': 'Viral infection (norovirus, rotavirus), bacterial infection, food poisoning',
                'treatments': 'Fluid replacement, rest, BRAT diet (bananas, rice, applesauce, toast), probiotics',
                'medications': 'Oral rehydration solution, Loperamide (for diarrhea), Ondansetron (for nausea)',
                'severity_level': 'Mild to Moderate',
                'prevention': 'Hand hygiene, food safety, avoid contaminated water, proper food storage',
                'when_to_see_doctor': 'Signs of severe dehydration, blood in stool, high fever, severe abdominal pain',
                'complications': 'Dehydration, electrolyte imbalance, kidney problems'
            }
        ]
        
        for condition in conditions:
            cursor.execute('''
                INSERT OR REPLACE INTO medical_conditions 
                (condition_name, category, symptoms, causes, treatments, medications, severity_level, prevention, when_to_see_doctor, complications)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                condition['condition_name'], condition['category'], condition['symptoms'],
                condition['causes'], condition['treatments'], condition['medications'],
                condition['severity_level'], condition['prevention'], condition['when_to_see_doctor'],
                condition['complications']
            ))
    
    def _populate_medications(self, cursor):
        """Populate database with medication information"""
        medications = [
            {
                'drug_name': 'Paracetamol',
                'generic_name': 'Acetaminophen',
                'brand_names': 'Tylenol, Panadol, Calpol',
                'drug_class': 'Analgesic, Antipyretic',
                'indication': 'Pain relief, fever reduction',
                'dosage_forms': 'Tablets, capsules, liquid, suppositories',
                'common_dosages': 'Adults: 500-1000mg every 4-6 hours, max 4000mg/day',
                'side_effects': 'Rare: liver damage with overdose, allergic reactions',
                'contraindications': 'Severe liver disease, alcohol abuse',
                'interactions': 'Warfarin (increased bleeding risk), chronic alcohol use',
                'pregnancy_category': 'Safe in pregnancy',
                'mechanism_of_action': 'Inhibits cyclooxygenase in CNS, blocks pain signals'
            },
            {
                'drug_name': 'Metformin',
                'generic_name': 'Metformin hydrochloride',
                'brand_names': 'Glucophage, Glumetza, Fortamet',
                'drug_class': 'Biguanide antidiabetic',
                'indication': 'Type 2 diabetes mellitus',
                'dosage_forms': 'Tablets, extended-release tablets',
                'common_dosages': 'Initial: 500mg twice daily, max 2550mg/day',
                'side_effects': 'Nausea, diarrhea, metallic taste, vitamin B12 deficiency',
                'contraindications': 'Kidney disease, liver disease, heart failure',
                'interactions': 'Contrast dye, alcohol, cimetidine',
                'pregnancy_category': 'Category B - generally safe',
                'mechanism_of_action': 'Decreases hepatic glucose production, improves insulin sensitivity'
            },
            {
                'drug_name': 'Lisinopril',
                'generic_name': 'Lisinopril',
                'brand_names': 'Prinivil, Zestril',
                'drug_class': 'ACE inhibitor',
                'indication': 'Hypertension, heart failure, post-MI',
                'dosage_forms': 'Tablets',
                'common_dosages': 'Initial: 10mg once daily, maintenance: 20-40mg daily',
                'side_effects': 'Dry cough, hyperkalemia, angioedema, dizziness',
                'contraindications': 'Pregnancy, bilateral renal artery stenosis, angioedema history',
                'interactions': 'Potassium supplements, NSAIDs, lithium',
                'pregnancy_category': 'Category D - avoid in pregnancy',
                'mechanism_of_action': 'Inhibits ACE, reduces angiotensin II formation'
            },
            {
                'drug_name': 'Sumatriptan',
                'generic_name': 'Sumatriptan succinate',
                'brand_names': 'Imitrex, Imigran',
                'drug_class': '5-HT1 receptor agonist',
                'indication': 'Acute migraine treatment',
                'dosage_forms': 'Tablets, injection, nasal spray',
                'common_dosages': '50-100mg tablet at onset, may repeat after 2 hours',
                'side_effects': 'Chest tightness, drowsiness, dizziness, injection site reactions',
                'contraindications': 'Coronary artery disease, uncontrolled hypertension, stroke history',
                'interactions': 'MAO inhibitors, ergot alkaloids, SSRIs',
                'pregnancy_category': 'Category C - use if benefit outweighs risk',
                'mechanism_of_action': 'Selective 5-HT1B/1D receptor agonist, causes vasoconstriction'
            },
            {
                'drug_name': 'Amoxicillin',
                'generic_name': 'Amoxicillin',
                'brand_names': 'Amoxil, Trimox, Moxatag',
                'drug_class': 'Penicillin antibiotic',
                'indication': 'Bacterial infections (respiratory, UTI, skin)',
                'dosage_forms': 'Capsules, tablets, oral suspension',
                'common_dosages': 'Adults: 250-500mg every 8 hours or 500-875mg every 12 hours',
                'side_effects': 'Diarrhea, nausea, rash, allergic reactions',
                'contraindications': 'Penicillin allergy, mononucleosis',
                'interactions': 'Methotrexate, warfarin, oral contraceptives',
                'pregnancy_category': 'Category B - safe in pregnancy',
                'mechanism_of_action': 'Inhibits bacterial cell wall synthesis'
            },
            {
                'drug_name': 'Aspirin',
                'generic_name': 'Acetylsalicylic acid',
                'brand_names': 'Bayer, Bufferin, Ecotrin',
                'drug_class': 'NSAID, Antiplatelet',
                'indication': 'Pain relief, fever reduction, cardiovascular protection',
                'dosage_forms': 'Tablets, chewable tablets',
                'common_dosages': 'Adults: 325-650mg every 4 hours for pain, 81mg daily for heart protection',
                'side_effects': 'Stomach irritation, bleeding risk, allergic reactions',
                'contraindications': 'Active bleeding, children under 16 (Reye syndrome risk)',
                'interactions': 'Warfarin (increased bleeding), alcohol (stomach irritation)',
                'pregnancy_category': 'Avoid in pregnancy (especially 3rd trimester)',
                'mechanism_of_action': 'Irreversibly inhibits COX enzymes, reduces platelet aggregation'
            },
            {
                'drug_name': 'Ibuprofen',
                'generic_name': 'Ibuprofen',
                'brand_names': 'Advil, Motrin, Nurofen',
                'drug_class': 'NSAID',
                'indication': 'Pain relief, fever reduction, inflammation reduction',
                'dosage_forms': 'Tablets, capsules, liquid, gel',
                'common_dosages': 'Adults: 200-400mg every 4-6 hours, max 1200mg/day',
                'side_effects': 'Stomach upset, dizziness, increased blood pressure',
                'contraindications': 'Heart disease, kidney disease, stomach ulcers',
                'interactions': 'Warfarin (bleeding risk), ACE inhibitors (reduced effectiveness)',
                'pregnancy_category': 'Avoid after 30 weeks pregnancy',
                'mechanism_of_action': 'Reversibly inhibits COX enzymes, reduces prostaglandin synthesis'
            },
            {
                'drug_name': 'Atorvastatin',
                'generic_name': 'Atorvastatin calcium',
                'brand_names': 'Lipitor',
                'drug_class': 'Statin',
                'indication': 'High cholesterol, cardiovascular disease prevention',
                'dosage_forms': 'Tablets',
                'common_dosages': 'Adults: 10-80mg once daily, usually at night',
                'side_effects': 'Muscle pain, liver enzyme elevation, headache',
                'contraindications': 'Active liver disease, pregnancy',
                'interactions': 'Warfarin (increased bleeding), cyclosporine (muscle toxicity)',
                'pregnancy_category': 'Pregnancy category X - contraindicated',
                'mechanism_of_action': 'Inhibits HMG-CoA reductase, reduces cholesterol synthesis'
            },
            {
                'drug_name': 'Omeprazole',
                'generic_name': 'Omeprazole',
                'brand_names': 'Prilosec, Losec',
                'drug_class': 'Proton pump inhibitor',
                'indication': 'GERD, peptic ulcers, acid reflux',
                'dosage_forms': 'Capsules, tablets',
                'common_dosages': 'Adults: 20-40mg once daily before breakfast',
                'side_effects': 'Headache, nausea, diarrhea, long-term use may cause B12 deficiency',
                'contraindications': 'Severe liver disease',
                'interactions': 'Warfarin (increased levels), clopidogrel (decreased effectiveness)',
                'pregnancy_category': 'Generally safe in pregnancy',
                'mechanism_of_action': 'Irreversibly blocks gastric proton pumps, reduces acid production'
            },
            {
                'drug_name': 'Cetirizine',
                'generic_name': 'Cetirizine hydrochloride',
                'brand_names': 'Zyrtec, Reactine',
                'drug_class': 'Antihistamine',
                'indication': 'Allergies, hay fever, urticaria',
                'dosage_forms': 'Tablets, liquid, chewable tablets',
                'common_dosages': 'Adults: 10mg once daily, children: 5mg once daily',
                'side_effects': 'Drowsiness, dry mouth, fatigue',
                'contraindications': 'Severe kidney disease',
                'interactions': 'Alcohol (increased drowsiness), sedatives (additive effects)',
                'pregnancy_category': 'Safe in pregnancy (category B)',
                'mechanism_of_action': 'Blocks H1 histamine receptors, prevents allergic responses'
            }
        ]
        
        for med in medications:
            cursor.execute('''
                INSERT OR REPLACE INTO medications
                (drug_name, generic_name, brand_names, drug_class, indication, dosage_forms, common_dosages, side_effects, contraindications, interactions, pregnancy_category, mechanism_of_action)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                med['drug_name'], med['generic_name'], med['brand_names'], med['drug_class'],
                med['indication'], med['dosage_forms'], med['common_dosages'], med['side_effects'],
                med['contraindications'], med['interactions'], med['pregnancy_category'], med['mechanism_of_action']
            ))
    
    def _populate_first_aid(self, cursor):
        """Populate database with first aid information"""
        first_aid_data = [
            {
                'emergency_type': 'Heart Attack',
                'immediate_steps': '1. Call 911 immediately, 2. Give aspirin if not allergic, 3. Keep person calm and sitting, 4. Loosen tight clothing, 5. Monitor breathing and pulse',
                'things_to_avoid': 'Do not give food or water, do not leave person alone, do not let them drive',
                'when_to_call_911': 'Chest pain lasting more than 5 minutes, shortness of breath, nausea with chest discomfort',
                'materials_needed': 'Aspirin (if available), phone to call 911'
            },
            {
                'emergency_type': 'Severe Bleeding',
                'immediate_steps': '1. Apply direct pressure with clean cloth, 2. Elevate injured area above heart, 3. Apply pressure bandage, 4. Do not remove embedded objects',
                'things_to_avoid': 'Do not remove bandages once applied, do not use tourniquet unless trained',
                'when_to_call_911': 'Bleeding that won\'t stop after 10 minutes of pressure, severe wounds, signs of shock',
                'materials_needed': 'Clean cloths, bandages, gloves if available'
            },
            {
                'emergency_type': 'Choking',
                'immediate_steps': '1. Ask "Are you choking?", 2. If conscious: 5 back blows, then 5 abdominal thrusts, 3. If unconscious: CPR, 4. Check mouth before rescue breaths',
                'things_to_avoid': 'Do not hit back if person can speak or cough, do not use fingers to remove object blindly',
                'when_to_call_911': 'Person becomes unconscious, cannot breathe or speak, cyanosis (blue lips/face)',
                'materials_needed': 'None required - use hands only'
            },
            {
                'emergency_type': 'Burns',
                'immediate_steps': '1. Remove from heat source, 2. Cool with running water for 10-20 minutes, 3. Remove jewelry before swelling, 4. Cover with sterile bandage',
                'things_to_avoid': 'Do not use ice, butter, or oil, do not break blisters, do not remove stuck clothing',
                'when_to_call_911': 'Burns larger than palm size, electrical burns, chemical burns, airway burns',
                'materials_needed': 'Cool water, sterile bandages, pain medication if available'
            }
        ]
        
        for aid in first_aid_data:
            cursor.execute('''
                INSERT OR REPLACE INTO first_aid
                (emergency_type, immediate_steps, things_to_avoid, when_to_call_911, materials_needed)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                aid['emergency_type'], aid['immediate_steps'], aid['things_to_avoid'],
                aid['when_to_call_911'], aid['materials_needed']
            ))
    
    def search_medical_condition(self, query: str) -> Dict[str, Any]:
        """Search for medical condition information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search by condition name or symptoms
        cursor.execute('''
            SELECT * FROM medical_conditions 
            WHERE condition_name LIKE ? OR symptoms LIKE ? OR category LIKE ?
            ORDER BY condition_name
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            conditions = []
            for result in results:
                condition = {
                    'condition_name': result[1],
                    'category': result[2],
                    'symptoms': result[3],
                    'causes': result[4],
                    'treatments': result[5],
                    'medications': result[6],
                    'severity_level': result[7],
                    'prevention': result[8],
                    'when_to_see_doctor': result[9],
                    'complications': result[10]
                }
                conditions.append(condition)
            
            return {
                'found': True,
                'conditions': conditions,
                'count': len(conditions)
            }
        
        return {'found': False, 'message': 'No medical conditions found matching your query.'}
    
    def search_medication(self, query: str) -> Dict[str, Any]:
        """Search for medication information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM medications 
            WHERE drug_name LIKE ? OR generic_name LIKE ? OR brand_names LIKE ? OR indication LIKE ?
            ORDER BY drug_name
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            medications = []
            for result in results:
                medication = {
                    'drug_name': result[1],
                    'generic_name': result[2],
                    'brand_names': result[3],
                    'drug_class': result[4],
                    'indication': result[5],
                    'dosage_forms': result[6],
                    'common_dosages': result[7],
                    'side_effects': result[8],
                    'contraindications': result[9],
                    'interactions': result[10],
                    'pregnancy_category': result[11],
                    'mechanism_of_action': result[12]
                }
                medications.append(medication)
            
            return {
                'found': True,
                'medications': medications,
                'count': len(medications)
            }
        
        return {'found': False, 'message': 'No medications found matching your query.'}
    
    def get_first_aid_info(self, emergency_type: str) -> Dict[str, Any]:
        """Get first aid information for emergency"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM first_aid 
            WHERE emergency_type LIKE ?
            ORDER BY emergency_type
        ''', (f'%{emergency_type}%',))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            first_aid_info = []
            for result in results:
                info = {
                    'emergency_type': result[1],
                    'immediate_steps': result[2],
                    'things_to_avoid': result[3],
                    'when_to_call_911': result[4],
                    'materials_needed': result[5]
                }
                first_aid_info.append(info)
            
            return {
                'found': True,
                'first_aid': first_aid_info,
                'count': len(first_aid_info)
            }
        
        return {'found': False, 'message': 'No first aid information found for this emergency type.'}
    
    def analyze_symptoms(self, symptoms_list: List[str]) -> Dict[str, Any]:
        """Analyze symptoms and suggest possible conditions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        possible_conditions = []
        
        for symptom in symptoms_list:
            cursor.execute('''
                SELECT condition_name, category, symptoms, severity_level, when_to_see_doctor
                FROM medical_conditions 
                WHERE symptoms LIKE ?
            ''', (f'%{symptom}%',))
            
            results = cursor.fetchall()
            for result in results:
                if result[0] not in [c['condition_name'] for c in possible_conditions]:
                    possible_conditions.append({
                        'condition_name': result[0],
                        'category': result[1],
                        'matching_symptoms': symptom,
                        'all_symptoms': result[2],
                        'severity_level': result[3],
                        'when_to_see_doctor': result[4]
                    })
        
        conn.close()
        
        return {
            'analyzed_symptoms': symptoms_list,
            'possible_conditions': possible_conditions,
            'disclaimer': 'This is for informational purposes only. Please consult a healthcare professional for proper diagnosis and treatment.'
        }
    
    def get_drug_interactions(self, medications: List[str]) -> Dict[str, Any]:
        """Check for potential drug interactions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        interactions_found = []
        
        for med in medications:
            cursor.execute('''
                SELECT drug_name, interactions, contraindications
                FROM medications 
                WHERE drug_name LIKE ? OR generic_name LIKE ?
            ''', (f'%{med}%', f'%{med}%'))
            
            results = cursor.fetchall()
            for result in results:
                if result[1]:  # If interactions field is not empty
                    interactions_found.append({
                        'medication': result[0],
                        'interactions': result[1],
                        'contraindications': result[2]
                    })
        
        conn.close()
        
        return {
            'medications_checked': medications,
            'interactions_found': interactions_found,
            'recommendation': 'Always consult your doctor or pharmacist about drug interactions before starting new medications.'
        }

# Global medical knowledge service instance
medical_service = MedicalKnowledgeService()

def get_medical_information(query: str, query_type: str = 'general') -> Dict[str, Any]:
    """
    Get medical information based on query type
    Types: 'condition', 'medication', 'first_aid', 'symptoms', 'interactions'
    """
    if query_type == 'condition':
        return medical_service.search_medical_condition(query)
    elif query_type == 'medication':
        return medical_service.search_medication(query)
    elif query_type == 'first_aid':
        return medical_service.get_first_aid_info(query)
    elif query_type == 'symptoms':
        symptoms = [s.strip() for s in query.split(',')]
        return medical_service.analyze_symptoms(symptoms)
    elif query_type == 'interactions':
        medications = [m.strip() for m in query.split(',')]
        return medical_service.get_drug_interactions(medications)
    else:
        # General search across all categories
        condition_result = medical_service.search_medical_condition(query)
        medication_result = medical_service.search_medication(query)
        first_aid_result = medical_service.get_first_aid_info(query)
        
        return {
            'query': query,
            'conditions': condition_result if condition_result['found'] else None,
            'medications': medication_result if medication_result['found'] else None,
            'first_aid': first_aid_result if first_aid_result['found'] else None
        }
