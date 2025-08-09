"""
Advanced Medical Training Service for Clang Chatbot
Provides enhanced medical knowledge, drug interactions, and symptom checking
"""

import re
import json
from typing import Dict, List, Optional, Tuple

class AdvancedMedicalService:
    def __init__(self):
        self.medical_knowledge = self._load_medical_database()
        self.drug_interactions = self._load_drug_interaction_database()
        self.symptoms_database = self._load_symptoms_database()
        self.medical_specialties = self._load_medical_specialties()
        
    def _load_medical_database(self) -> Dict:
        """Enhanced medical knowledge database"""
        return {
            'conditions': {
                'diabetes': {
                    'type': 'chronic_disease',
                    'description': 'A group of metabolic disorders characterized by high blood sugar levels',
                    'types': ['Type 1', 'Type 2', 'Gestational'],
                    'symptoms': ['increased thirst', 'frequent urination', 'unexplained weight loss', 'fatigue', 'blurred vision'],
                    'risk_factors': ['family history', 'obesity', 'sedentary lifestyle', 'age over 45'],
                    'complications': ['heart disease', 'stroke', 'kidney disease', 'eye problems', 'nerve damage'],
                    'management': ['blood sugar monitoring', 'healthy diet', 'regular exercise', 'medication as prescribed'],
                    'emergency_signs': ['very high blood sugar (over 400)', 'severe dehydration', 'difficulty breathing']
                },
                'hypertension': {
                    'type': 'cardiovascular',
                    'description': 'High blood pressure - a condition where blood pressure is consistently elevated',
                    'normal_range': '120/80 mmHg or lower',
                    'stages': {
                        'elevated': '120-129 systolic, less than 80 diastolic',
                        'stage_1': '130-139 systolic or 80-89 diastolic',
                        'stage_2': '140/90 mmHg or higher',
                        'crisis': 'over 180/120 mmHg'
                    },
                    'symptoms': ['often no symptoms', 'headaches', 'shortness of breath', 'nosebleeds'],
                    'lifestyle_changes': ['reduce sodium', 'exercise regularly', 'maintain healthy weight', 'limit alcohol', 'quit smoking'],
                    'complications': ['heart attack', 'stroke', 'kidney disease', 'heart failure']
                },
                'covid19': {
                    'type': 'infectious_disease',
                    'description': 'Coronavirus disease caused by SARS-CoV-2 virus',
                    'symptoms': {
                        'common': ['fever', 'cough', 'fatigue', 'loss of taste or smell'],
                        'serious': ['difficulty breathing', 'chest pain', 'confusion', 'bluish lips or face']
                    },
                    'prevention': ['vaccination', 'mask wearing', 'hand hygiene', 'social distancing'],
                    'when_to_seek_help': ['difficulty breathing', 'persistent chest pain', 'confusion', 'bluish lips']
                },
                'depression': {
                    'type': 'mental_health',
                    'description': 'A mood disorder causing persistent feelings of sadness and loss of interest',
                    'symptoms': ['persistent sadness', 'loss of interest', 'fatigue', 'sleep changes', 'appetite changes', 'difficulty concentrating'],
                    'treatment_options': ['therapy', 'medication', 'lifestyle changes', 'support groups'],
                    'emergency_signs': ['suicidal thoughts', 'self-harm behavior', 'severe hopelessness'],
                    'help_resources': ['National Suicide Prevention Lifeline: 988', 'Crisis Text Line: Text HOME to 741741']
                },
                'asthma': {
                    'type': 'respiratory',
                    'description': 'A condition where airways narrow and swell, making breathing difficult',
                    'symptoms': ['wheezing', 'shortness of breath', 'chest tightness', 'coughing'],
                    'triggers': ['allergens', 'cold air', 'exercise', 'stress', 'smoke', 'strong odors'],
                    'treatment': ['rescue inhalers', 'controller medications', 'trigger avoidance'],
                    'emergency_signs': ['severe breathing difficulty', 'inability to speak in full sentences', 'blue lips or fingernails'],
                    'management': ['action plan', 'peak flow monitoring', 'regular check-ups']
                },
                'heart_attack': {
                    'type': 'cardiovascular_emergency',
                    'description': 'Blockage of blood flow to the heart muscle causing tissue damage',
                    'symptoms': ['chest pain', 'arm pain', 'jaw pain', 'shortness of breath', 'nausea', 'sweating'],
                    'risk_factors': ['smoking', 'high cholesterol', 'high blood pressure', 'diabetes', 'family history'],
                    'emergency_action': 'Call 911 immediately, chew aspirin if not allergic',
                    'prevention': ['healthy diet', 'regular exercise', 'no smoking', 'stress management']
                },
                'stroke': {
                    'type': 'neurological_emergency',
                    'description': 'Interrupted blood supply to the brain causing brain cell death',
                    'symptoms': ['face drooping', 'arm weakness', 'speech difficulty', 'sudden confusion', 'severe headache'],
                    'fast_signs': ['Face drooping', 'Arms weak', 'Speech slurred', 'Time to call 911'],
                    'risk_factors': ['high blood pressure', 'smoking', 'diabetes', 'high cholesterol', 'age'],
                    'emergency_action': 'Call 911 immediately - time is critical for treatment'
                },
                'anxiety': {
                    'type': 'mental_health',
                    'description': 'Excessive worry and fear that interferes with daily activities',
                    'symptoms': ['excessive worry', 'restlessness', 'fatigue', 'difficulty concentrating', 'muscle tension', 'sleep problems'],
                    'types': ['generalized anxiety', 'panic disorder', 'social anxiety', 'specific phobias'],
                    'treatment': ['therapy', 'medication', 'relaxation techniques', 'lifestyle changes'],
                    'coping_strategies': ['deep breathing', 'mindfulness', 'regular exercise', 'adequate sleep']
                },
                'migraine': {
                    'type': 'neurological',
                    'description': 'Severe headaches often accompanied by nausea and light sensitivity',
                    'symptoms': ['throbbing headache', 'nausea', 'vomiting', 'light sensitivity', 'sound sensitivity'],
                    'triggers': ['stress', 'certain foods', 'hormonal changes', 'sleep changes', 'weather changes'],
                    'treatment': ['pain medications', 'preventive medications', 'lifestyle modifications'],
                    'warning_signs': ['sudden severe headache', 'headache with fever', 'headache with vision changes']
                },
                'arthritis': {
                    'type': 'musculoskeletal',
                    'description': 'Joint inflammation causing pain and stiffness',
                    'types': ['osteoarthritis', 'rheumatoid arthritis', 'psoriatic arthritis'],
                    'symptoms': ['joint pain', 'stiffness', 'swelling', 'reduced range of motion'],
                    'management': ['medications', 'physical therapy', 'exercise', 'weight management'],
                    'lifestyle_tips': ['stay active', 'maintain healthy weight', 'protect joints', 'manage stress']
                },
                'pneumonia': {
                    'type': 'respiratory_infection',
                    'description': 'Infection that inflames air sacs in lungs, filling them with fluid',
                    'symptoms': ['cough with phlegm', 'fever', 'chills', 'shortness of breath', 'chest pain'],
                    'types': ['bacterial', 'viral', 'fungal'],
                    'risk_factors': ['age over 65', 'smoking', 'chronic conditions', 'weakened immune system'],
                    'emergency_signs': ['difficulty breathing', 'high fever', 'confusion', 'blue lips']
                },
                'kidney_stones': {
                    'type': 'urological',
                    'description': 'Hard deposits of minerals and salts that form in kidneys',
                    'symptoms': ['severe back pain', 'pain radiating to groin', 'nausea', 'blood in urine', 'frequent urination'],
                    'types': ['calcium stones', 'uric acid stones', 'struvite stones', 'cystine stones'],
                    'prevention': ['drink plenty of water', 'limit sodium', 'reduce animal protein', 'maintain healthy weight'],
                    'treatment': ['pain management', 'increased fluid intake', 'medications', 'surgical procedures if large']
                },
                'allergies': {
                    'type': 'immune_system',
                    'description': 'Immune system reaction to substances that are usually harmless',
                    'types': ['food allergies', 'environmental allergies', 'drug allergies', 'insect allergies'],
                    'symptoms': ['sneezing', 'runny nose', 'itchy eyes', 'skin rash', 'swelling'],
                    'severe_reaction': 'Anaphylaxis - life-threatening emergency requiring immediate epinephrine',
                    'management': ['allergen avoidance', 'antihistamines', 'nasal sprays', 'allergy shots']
                }
            },
            'medications': {
                'metformin': {
                    'generic_name': 'metformin',
                    'brand_names': ['Glucophage', 'Fortamet', 'Glumetza'],
                    'class': 'biguanide',
                    'indication': 'Type 2 diabetes',
                    'mechanism': 'Decreases glucose production by liver, improves insulin sensitivity',
                    'common_side_effects': ['nausea', 'diarrhea', 'stomach upset', 'metallic taste'],
                    'serious_side_effects': ['lactic acidosis (rare)', 'vitamin B12 deficiency'],
                    'contraindications': ['kidney disease', 'liver disease', 'heart failure'],
                    'monitoring': 'kidney function, vitamin B12 levels'
                },
                'lisinopril': {
                    'generic_name': 'lisinopril',
                    'brand_names': ['Prinivil', 'Zestril'],
                    'class': 'ACE inhibitor',
                    'indication': 'High blood pressure, heart failure',
                    'mechanism': 'Blocks ACE enzyme, relaxes blood vessels',
                    'common_side_effects': ['dry cough', 'dizziness', 'headache'],
                    'serious_side_effects': ['angioedema', 'hyperkalemia', 'kidney problems'],
                    'contraindications': ['pregnancy', 'angioedema history'],
                    'monitoring': 'blood pressure, kidney function, potassium levels'
                },
                'atorvastatin': {
                    'generic_name': 'atorvastatin',
                    'brand_names': ['Lipitor'],
                    'class': 'statin',
                    'indication': 'High cholesterol, cardiovascular disease prevention',
                    'mechanism': 'Inhibits HMG-CoA reductase, reduces cholesterol production',
                    'common_side_effects': ['muscle aches', 'headache', 'nausea'],
                    'serious_side_effects': ['rhabdomyolysis', 'liver problems', 'diabetes'],
                    'contraindications': ['active liver disease', 'pregnancy'],
                    'monitoring': 'liver function, lipid levels, muscle symptoms'
                },
                'albuterol': {
                    'generic_name': 'albuterol',
                    'brand_names': ['ProAir', 'Ventolin', 'Proventil'],
                    'class': 'beta-2 agonist bronchodilator',
                    'indication': 'Asthma, COPD, bronchospasm',
                    'mechanism': 'Relaxes airway smooth muscles, opens airways',
                    'common_side_effects': ['tremor', 'nervousness', 'headache', 'rapid heartbeat'],
                    'serious_side_effects': ['severe allergic reactions', 'paradoxical bronchospasm'],
                    'contraindications': ['hypersensitivity to albuterol'],
                    'monitoring': 'heart rate, blood pressure, respiratory status'
                },
                'sertraline': {
                    'generic_name': 'sertraline',
                    'brand_names': ['Zoloft'],
                    'class': 'SSRI antidepressant',
                    'indication': 'Depression, anxiety, PTSD, OCD',
                    'mechanism': 'Blocks serotonin reuptake, increases serotonin levels',
                    'common_side_effects': ['nausea', 'insomnia', 'sexual dysfunction', 'weight changes'],
                    'serious_side_effects': ['serotonin syndrome', 'suicidal thoughts', 'bleeding risk'],
                    'contraindications': ['MAO inhibitor use', 'pimozide use'],
                    'monitoring': 'mood changes, suicidal thoughts, weight'
                },
                'ibuprofen': {
                    'generic_name': 'ibuprofen',
                    'brand_names': ['Advil', 'Motrin'],
                    'class': 'NSAID',
                    'indication': 'Pain, inflammation, fever',
                    'mechanism': 'Inhibits COX enzymes, reduces inflammation',
                    'common_side_effects': ['stomach upset', 'heartburn', 'dizziness'],
                    'serious_side_effects': ['GI bleeding', 'kidney problems', 'heart attack risk'],
                    'contraindications': ['peptic ulcer disease', 'severe kidney disease'],
                    'monitoring': 'kidney function, blood pressure, GI symptoms'
                },
                'omeprazole': {
                    'generic_name': 'omeprazole',
                    'brand_names': ['Prilosec'],
                    'class': 'proton pump inhibitor',
                    'indication': 'GERD, peptic ulcers, heartburn',
                    'mechanism': 'Blocks proton pumps, reduces stomach acid',
                    'common_side_effects': ['headache', 'nausea', 'diarrhea'],
                    'serious_side_effects': ['C. diff infection', 'bone fractures', 'magnesium deficiency'],
                    'contraindications': ['hypersensitivity to PPIs'],
                    'monitoring': 'magnesium levels, bone health with long-term use'
                }
            }
        }
    
    def _load_drug_interaction_database(self) -> Dict:
        """Drug interaction database"""
        return {
            'major_interactions': {
                ('warfarin', 'aspirin'): {
                    'severity': 'major',
                    'effect': 'Increased bleeding risk',
                    'mechanism': 'Additive anticoagulant effects',
                    'management': 'Monitor INR closely, consider dose adjustment'
                },
                ('metformin', 'contrast_dye'): {
                    'severity': 'major',
                    'effect': 'Increased risk of lactic acidosis',
                    'mechanism': 'Kidney function impairment',
                    'management': 'Discontinue metformin before procedure, restart after kidney function confirmed normal'
                },
                ('simvastatin', 'clarithromycin'): {
                    'severity': 'major',
                    'effect': 'Increased risk of muscle problems',
                    'mechanism': 'Inhibition of statin metabolism',
                    'management': 'Avoid combination or reduce statin dose'
                }
            },
            'moderate_interactions': {
                ('lisinopril', 'ibuprofen'): {
                    'severity': 'moderate',
                    'effect': 'Reduced blood pressure lowering effect',
                    'mechanism': 'NSAIDs can counteract ACE inhibitor effects',
                    'management': 'Monitor blood pressure, consider alternative pain relief'
                }
            }
        }
    
    def _load_symptoms_database(self) -> Dict:
        """Enhanced symptom checker database"""
        return {
            'symptom_patterns': {
                'chest_pain': {
                    'emergency_keywords': ['crushing', 'squeezing', 'radiating to arm', 'shortness of breath', 'sweating'],
                    'possible_conditions': ['heart attack', 'angina', 'pulmonary embolism', 'pneumonia', 'acid reflux'],
                    'red_flags': ['sudden onset', 'severe pain', 'difficulty breathing', 'dizziness'],
                    'immediate_action': 'Call 911 immediately if experiencing severe chest pain'
                },
                'headache': {
                    'types': {
                        'tension': ['band-like pressure', 'both sides', 'mild to moderate'],
                        'migraine': ['throbbing', 'one side', 'nausea', 'light sensitivity'],
                        'cluster': ['severe', 'around eye', 'tearing', 'nasal congestion']
                    },
                    'red_flags': ['sudden severe headache', 'fever with stiff neck', 'vision changes', 'confusion'],
                    'emergency_action': 'Seek immediate care for sudden severe headache or headache with fever and stiff neck'
                },
                'fever': {
                    'ranges': {
                        'low_grade': '100.4-102°F (38-38.9°C)',
                        'moderate': '102-104°F (38.9-40°C)',
                        'high': 'Above 104°F (40°C)'
                    },
                    'concerning_symptoms': ['difficulty breathing', 'severe headache', 'stiff neck', 'confusion', 'persistent vomiting'],
                    'emergency_thresholds': ['fever above 104°F', 'fever with severe symptoms', 'fever in immunocompromised']
                }
            }
        }
    
    def _load_medical_specialties(self) -> Dict:
        """Medical specialties and when to refer"""
        return {
            'cardiology': {
                'conditions': ['heart disease', 'arrhythmia', 'heart failure', 'high blood pressure'],
                'symptoms': ['chest pain', 'palpitations', 'shortness of breath', 'leg swelling']
            },
            'endocrinology': {
                'conditions': ['diabetes', 'thyroid disorders', 'hormone imbalances'],
                'symptoms': ['unexplained weight changes', 'fatigue', 'excessive thirst']
            },
            'gastroenterology': {
                'conditions': ['acid reflux', 'IBS', 'inflammatory bowel disease'],
                'symptoms': ['persistent abdominal pain', 'changes in bowel habits', 'heartburn']
            },
            'neurology': {
                'conditions': ['migraine', 'seizures', 'stroke', 'multiple sclerosis'],
                'symptoms': ['severe headaches', 'numbness', 'memory problems', 'coordination issues']
            }
        }
    
    def check_drug_interactions(self, medications: List[str]) -> Dict:
        """Check for drug interactions"""
        interactions = []
        medications = [med.lower().strip() for med in medications]
        
        # Check major interactions
        for i, med1 in enumerate(medications):
            for med2 in medications[i+1:]:
                interaction_key = tuple(sorted([med1, med2]))
                
                if interaction_key in self.drug_interactions['major_interactions']:
                    interaction = self.drug_interactions['major_interactions'][interaction_key]
                    interactions.append({
                        'drugs': [med1, med2],
                        'severity': interaction['severity'],
                        'effect': interaction['effect'],
                        'management': interaction['management']
                    })
                elif interaction_key in self.drug_interactions['moderate_interactions']:
                    interaction = self.drug_interactions['moderate_interactions'][interaction_key]
                    interactions.append({
                        'drugs': [med1, med2],
                        'severity': interaction['severity'],
                        'effect': interaction['effect'],
                        'management': interaction['management']
                    })
        
        return {
            'interactions_found': len(interactions) > 0,
            'interactions': interactions,
            'total_medications': len(medications)
        }
    
    def analyze_symptoms(self, symptoms_text: str) -> Dict:
        """Enhanced symptom analysis"""
        symptoms_lower = symptoms_text.lower()
        analysis = {
            'symptoms_identified': [],
            'possible_conditions': [],
            'urgency_level': 'routine',
            'recommendations': [],
            'red_flags': [],
            'specialist_referral': None
        }
        
        # Check for emergency symptoms
        emergency_keywords = ['crushing chest pain', 'difficulty breathing', 'severe headache', 'confusion', 'chest pain']
        for keyword in emergency_keywords:
            if keyword in symptoms_lower:
                analysis['urgency_level'] = 'emergency'
                analysis['red_flags'].append(f"Emergency symptom detected: {keyword}")
                analysis['recommendations'].append("🚨 SEEK IMMEDIATE MEDICAL ATTENTION - Call 911")
        
        # Symptom pattern matching
        if 'chest pain' in symptoms_lower:
            chest_info = self.symptoms_database['symptom_patterns']['chest_pain']
            analysis['symptoms_identified'].append('chest pain')
            analysis['possible_conditions'].extend(chest_info['possible_conditions'])
            
            for red_flag in chest_info['red_flags']:
                if any(word in symptoms_lower for word in red_flag.split()):
                    analysis['red_flags'].append(red_flag)
                    analysis['urgency_level'] = 'urgent'
        
        if 'headache' in symptoms_lower:
            analysis['symptoms_identified'].append('headache')
            headache_info = self.symptoms_database['symptom_patterns']['headache']
            
            # Determine headache type
            for h_type, characteristics in headache_info['types'].items():
                if any(char in symptoms_lower for char in characteristics):
                    analysis['possible_conditions'].append(f"{h_type} headache")
        
        if any(word in symptoms_lower for word in ['fever', 'temperature', 'hot']):
            analysis['symptoms_identified'].append('fever')
            fever_info = self.symptoms_database['symptom_patterns']['fever']
            
            for concerning in fever_info['concerning_symptoms']:
                if concerning in symptoms_lower:
                    analysis['urgency_level'] = 'urgent'
                    analysis['red_flags'].append(f"Concerning symptom with fever: {concerning}")
        
        # Recommend specialist if needed
        for specialty, info in self.medical_specialties.items():
            if any(symptom in symptoms_lower for symptom in info['symptoms']):
                analysis['specialist_referral'] = specialty
                break
        
        # General recommendations based on urgency
        if analysis['urgency_level'] == 'routine':
            analysis['recommendations'].extend([
                "Monitor symptoms and consult healthcare provider if they persist or worsen",
                "Maintain a symptom diary to track patterns",
                "Consider lifestyle factors that might contribute to symptoms"
            ])
        elif analysis['urgency_level'] == 'urgent':
            analysis['recommendations'].extend([
                "Seek medical attention within 24 hours",
                "Contact your healthcare provider or visit urgent care",
                "Do not ignore these symptoms"
            ])
        
        return analysis
    
    def get_condition_information(self, condition: str) -> Optional[Dict]:
        """Get detailed information about a medical condition"""
        condition_lower = condition.lower().strip()
        
        for cond_name, cond_info in self.medical_knowledge['conditions'].items():
            if condition_lower in cond_name or cond_name in condition_lower:
                return {
                    'condition': cond_name,
                    'information': cond_info,
                    'disclaimer': "This information is for educational purposes only. Always consult with a healthcare professional for medical advice."
                }
        return None
    
    def get_medication_information(self, medication: str) -> Optional[Dict]:
        """Get detailed medication information"""
        med_lower = medication.lower().strip()
        
        for med_name, med_info in self.medical_knowledge['medications'].items():
            if (med_lower in med_name or med_name in med_lower or 
                any(brand.lower() in med_lower for brand in med_info.get('brand_names', []))):
                return {
                    'medication': med_name,
                    'information': med_info,
                    'disclaimer': "This information is for educational purposes only. Always follow your healthcare provider's instructions."
                }
        return None
    
    def format_medical_response(self, query: str) -> str:
        """Format a comprehensive medical response"""
        query_lower = query.lower()
        
        # Check if it's a drug interaction query
        if 'interaction' in query_lower or 'together' in query_lower:
            # Extract potential medication names (this is simplified)
            meds = []
            for med_name in self.medical_knowledge['medications'].keys():
                if med_name in query_lower:
                    meds.append(med_name)
            
            if len(meds) >= 2:
                interaction_result = self.check_drug_interactions(meds)
                if interaction_result['interactions_found']:
                    response = "🔬 **Drug Interaction Analysis:**\n\n"
                    for interaction in interaction_result['interactions']:
                        response += f"⚠️ **{interaction['severity'].upper()} Interaction:**\n"
                        response += f"**Drugs:** {' + '.join(interaction['drugs'])}\n"
                        response += f"**Effect:** {interaction['effect']}\n"
                        response += f"**Management:** {interaction['management']}\n\n"
                    response += "⚠️ **Important:** Always consult your healthcare provider before making any medication changes."
                    return response
        
        # Check if it's a symptom query
        if any(word in query_lower for word in ['symptom', 'pain', 'ache', 'feel', 'hurt', 'sick']):
            symptom_analysis = self.analyze_symptoms(query)
            
            response = "🏥 **Symptom Analysis:**\n\n"
            
            if symptom_analysis['urgency_level'] == 'emergency':
                response += "🚨 **EMERGENCY ALERT:**\n"
                for red_flag in symptom_analysis['red_flags']:
                    response += f"• {red_flag}\n"
                response += "\n"
            
            if symptom_analysis['symptoms_identified']:
                response += f"**Symptoms Identified:** {', '.join(symptom_analysis['symptoms_identified'])}\n\n"
            
            if symptom_analysis['possible_conditions']:
                response += f"**Possible Conditions:** {', '.join(symptom_analysis['possible_conditions'])}\n\n"
            
            response += "**Recommendations:**\n"
            for rec in symptom_analysis['recommendations']:
                response += f"• {rec}\n"
            
            if symptom_analysis['specialist_referral']:
                response += f"\n**Consider consulting:** {symptom_analysis['specialist_referral']} specialist\n"
            
            response += "\n⚠️ **Medical Disclaimer:** This analysis is for informational purposes only and should not replace professional medical advice."
            return response
        
        # Check for specific condition or medication queries
        condition_info = self.get_condition_information(query)
        if condition_info:
            info = condition_info['information']
            response = f"🏥 **Medical Information: {condition_info['condition'].title()}**\n\n"
            response += f"**Description:** {info['description']}\n\n"
            
            if 'symptoms' in info:
                response += f"**Symptoms:** {', '.join(info['symptoms'])}\n\n"
            
            if 'risk_factors' in info:
                response += f"**Risk Factors:** {', '.join(info['risk_factors'])}\n\n"
            
            if 'management' in info:
                response += f"**Management:** {', '.join(info['management'])}\n\n"
            
            if 'emergency_signs' in info:
                response += f"🚨 **Emergency Signs:** {', '.join(info['emergency_signs'])}\n\n"
            
            response += f"⚠️ {condition_info['disclaimer']}"
            return response
        
        medication_info = self.get_medication_information(query)
        if medication_info:
            info = medication_info['information']
            response = f"💊 **Medication Information: {medication_info['medication'].title()}**\n\n"
            response += f"**Generic Name:** {info['generic_name']}\n"
            
            if 'brand_names' in info:
                response += f"**Brand Names:** {', '.join(info['brand_names'])}\n"
            
            response += f"**Class:** {info['class']}\n"
            response += f"**Indication:** {info['indication']}\n\n"
            
            if 'common_side_effects' in info:
                response += f"**Common Side Effects:** {', '.join(info['common_side_effects'])}\n\n"
            
            if 'serious_side_effects' in info:
                response += f"⚠️ **Serious Side Effects:** {', '.join(info['serious_side_effects'])}\n\n"
            
            response += f"⚠️ {medication_info['disclaimer']}"
            return response
        
        return None

# Global instance
advanced_medical_service = AdvancedMedicalService()
