import json
import random

# Sample medical topics and templates
conditions = [
    "diabetes", "hypertension", "asthma", "anemia", "pneumonia", "depression", "migraine", "arthritis", "bronchitis", "hypothyroidism",
    "gout", "anxiety", "conjunctivitis", "otitis media", "influenza", "peptic ulcer", "kidney disease", "appendicitis", "cholesterol", "heart disease",
    "eczema", "psoriasis", "COPD", "tuberculosis", "hepatitis", "lupus", "multiple sclerosis", "epilepsy", "stroke", "cancer",
    "obesity", "insomnia", "fibromyalgia", "meningitis", "scoliosis", "thyroid cancer", "pancreatitis", "ulcerative colitis", "Crohn's disease", "celiac disease",
    "rheumatoid arthritis", "osteoarthritis", "bipolar disorder", "schizophrenia", "autism", "ADHD", "dyslexia", "glaucoma", "cataract", "macular degeneration"
]
symptoms = [
    "What are the symptoms of {condition}?",
    "How does {condition} present clinically?",
    "List common signs of {condition}.",
    "Describe the early warning signs of {condition}.",
    "What are the complications associated with {condition}?",
    "How can {condition} be detected?"
]
treatments = [
    "What is the recommended treatment for {condition}?",
    "How do you manage {condition}?",
    "What medications are used for {condition}?",
    "What are the latest therapies for {condition}?",
    "Are there surgical options for {condition}?",
    "What is the prognosis for {condition}?"
]
prescriptions = [
    "Write a prescription for {condition} in adults.",
    "Prescribe medication for {condition} in children.",
    "What is the dosage of medication for {condition}?",
    "What are the contraindications for {condition} medications?",
    "List possible side effects of drugs for {condition}.",
    "What is the recommended duration of therapy for {condition}?"
]
advice = [
    "What lifestyle changes help prevent {condition}?",
    "What advice should be given for managing {condition}?",
    "How can patients reduce risk of {condition}?",
    "What dietary recommendations are there for {condition}?",
    "What exercise is suitable for {condition}?",
    "How can family support help with {condition}?"
]

answers = [
    "Treatment may include medication, physical therapy, and regular follow-up with a specialist.",
    "Symptoms vary but often include pain, fatigue, and organ-specific issues.",
    "Prescription should be tailored to the patient's age, weight, and comorbidities.",
    "Lifestyle changes such as diet, exercise, and stress management are crucial.",
    "Management involves a multidisciplinary team and patient education.",
    "Early detection and intervention can improve outcomes.",
    "Surgical options are considered in severe cases.",
    "Side effects may include nausea, dizziness, or allergic reactions.",
    "Family support and counseling are important for chronic conditions.",
    "Prognosis depends on timely diagnosis and adherence to treatment."
]

def generate_qa(num_entries=10000):
    qa_set = set()
    qa_list = []
    attempts = 0
    max_attempts = num_entries * 2
    while len(qa_list) < num_entries and attempts < max_attempts:
        condition = random.choice(conditions)
        template_type = random.choice([symptoms, treatments, prescriptions, advice])
        question = random.choice(template_type).format(condition=condition)
        answer = random.choice(answers)
        qa_pair = (question, answer)
        if qa_pair not in qa_set:
            qa_set.add(qa_pair)
            qa_list.append({"question": question, "answer": answer})
        attempts += 1
    return qa_list

if __name__ == "__main__":
    output_file = "medical_training_data_template.json"
    qa_data = generate_qa(10000)
    with open(output_file, "w") as f:
        json.dump(qa_data, f, indent=2)
    print(f"Generated {len(qa_data)} medical Q&A pairs in {output_file}")
