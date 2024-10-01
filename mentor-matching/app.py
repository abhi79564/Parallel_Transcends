# app.py
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

mentors = [
    {
        "id": 1,
        "name": "John Doe",
        "photo": "https://randomuser.me/api/portraits/men/1.jpg",
        "domain": "Software Engineering",
        "experience": "10 years",
        "skills": "Python, JavaScript, Machine Learning",
        "company": "Google",
        "email": "john.doe@example.com",
        "phone": "+1 (123) 456-7890",
        "bio": "Experienced software engineer with a passion for machine learning and web development."
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "photo": "https://randomuser.me/api/portraits/women/1.jpg",
        "domain": "Data Science",
        "experience": "8 years",
        "skills": "Python, R, Statistics, Big Data",
        "company": "Amazon",
        "email": "jane.smith@example.com",
        "phone": "+1 (234) 567-8901",
        "bio": "Data scientist with expertise in big data analytics and machine learning algorithms."
    },
    {
        "id": 3,
        "name": "Aarav Sharma",
        "photo": "https://randomuser.me/api/portraits/men/2.jpg",
        "domain": "Machine Learning",
        "experience": "7 years",
        "skills": "TensorFlow, Keras, Python",
        "company": "Microsoft",
        "email": "aarav.sharma@example.com",
        "phone": "+91 9876543210",
        "bio": "Machine learning engineer with experience in deep learning and AI models."
    },
    {
        "id": 4,
        "name": "Diya Patel",
        "photo": "https://randomuser.me/api/portraits/women/2.jpg",
        "domain": "Web Development",
        "experience": "5 years",
        "skills": "React, Angular, JavaScript",
        "company": "Infosys",
        "email": "diya.patel@example.com",
        "phone": "+91 9123456789",
        "bio": "Front-end developer specializing in building interactive and responsive web applications."
    },
    {
        "id": 5,
        "name": "Rohan Gupta",
        "photo": "https://randomuser.me/api/portraits/men/3.jpg",
        "domain": "Data Science",
        "experience": "6 years",
        "skills": "Python, R, Machine Learning",
        "company": "TCS",
        "email": "rohan.gupta@example.com",
        "phone": "+91 9001234567",
        "bio": "Data scientist with a focus on predictive modeling and data visualization."
    },
    {
        "id": 6,
        "name": "Priya Kapoor",
        "photo": "https://randomuser.me/api/portraits/women/3.jpg",
        "domain": "Cloud Computing",
        "experience": "8 years",
        "skills": "AWS, Azure, DevOps",
        "company": "Wipro",
        "email": "priya.kapoor@example.com",
        "phone": "+91 9898765432",
        "bio": "Cloud solutions architect with expertise in cloud migration and infrastructure automation."
    },
    {
        "id": 7,
        "name": "Kabir Singh",
        "photo": "https://randomuser.me/api/portraits/men/4.jpg",
        "domain": "Cybersecurity",
        "experience": "10 years",
        "skills": "Network Security, Ethical Hacking, SIEM",
        "company": "HCL",
        "email": "kabir.singh@example.com",
        "phone": "+91 9876123456",
        "bio": "Cybersecurity expert with a focus on ethical hacking and network security strategies."
    },
    {
        "id": 8,
        "name": "Neha Joshi",
        "photo": "https://randomuser.me/api/portraits/women/4.jpg",
        "domain": "Mobile App Development",
        "experience": "4 years",
        "skills": "React Native, Flutter, Swift",
        "company": "Zomato",
        "email": "neha.joshi@example.com",
        "phone": "+91 9234567890",
        "bio": "Mobile app developer with experience in building cross-platform applications."
    },
    {
        "id": 9,
        "name": "Vikram Desai",
        "photo": "https://randomuser.me/api/portraits/men/5.jpg",
        "domain": "Product Management",
        "experience": "9 years",
        "skills": "Agile, Scrum, Product Strategy",
        "company": "Flipkart",
        "email": "vikram.desai@example.com",
        "phone": "+91 9012345678",
        "bio": "Product manager with a strong background in agile methodologies and product lifecycle management."
    },
    {
        "id": 10,
        "name": "Ananya Iyer",
        "photo": "https://randomuser.me/api/portraits/women/5.jpg",
        "domain": "UI/UX Design",
        "experience": "6 years",
        "skills": "Figma, Sketch, User Testing",
        "company": "Paytm",
        "email": "ananya.iyer@example.com",
        "phone": "+91 9198765432",
        "bio": "UI/UX designer with a focus on creating user-centered designs and enhancing user experiences."
    },
    {
        "id": 11,
        "name": "Raj Malhotra",
        "photo": "https://randomuser.me/api/portraits/men/6.jpg",
        "domain": "Artificial Intelligence",
        "experience": "7 years",
        "skills": "NLP, Computer Vision, Python",
        "company": "Ola",
        "email": "raj.malhotra@example.com",
        "phone": "+91 9876541230",
        "bio": "AI specialist with experience in natural language processing and computer vision."
    },
    {
        "id": 12,
        "name": "Maya Mehta",
        "photo": "https://randomuser.me/api/portraits/women/6.jpg",
        "domain": "Software Engineering",
        "experience": "6 years",
        "skills": "C++, Java, System Design",
        "company": "Reliance Jio",
        "email": "maya.mehta@example.com",
        "phone": "+91 9009876543",
        "bio": "Software engineer with a focus on system architecture and backend development."
    },
    {
        "id": 13,
        "name": "Siddharth Verma",
        "photo": "https://randomuser.me/api/portraits/men/7.jpg",
        "domain": "Blockchain",
        "experience": "5 years",
        "skills": "Ethereum, Solidity, Smart Contracts",
        "company": "CoinDCX",
        "email": "siddharth.verma@example.com",
        "phone": "+91 9876432100",
        "bio": "Blockchain developer with experience in decentralized applications and smart contract development."
    },
    {
        "id": 14,
        "name": "Kavya Reddy",
        "photo": "https://randomuser.me/api/portraits/women/7.jpg",
        "domain": "Cybersecurity",
        "experience": "6 years",
        "skills": "Penetration Testing, Risk Assessment, Incident Response",
        "company": "Tata Consultancy Services",
        "email": "kavya.reddy@example.com",
        "phone": "+91 9234512345",
        "bio": "Cybersecurity analyst with a focus on penetration testing and incident management."
    },
    {
        "id": 15,
        "name": "Ishaan Ahuja",
        "photo": "https://randomuser.me/api/portraits/men/8.jpg",
        "domain": "Cloud Computing",
        "experience": "7 years",
        "skills": "AWS, Google Cloud, Kubernetes",
        "company": "Cognizant",
        "email": "ishaan.ahuja@example.com",
        "phone": "+91 9012345679",
        "bio": "Cloud architect with expertise in cloud infrastructure and container orchestration."
    },
    {
        "id": 16,
        "name": "Lakshmi Nair",
        "photo": "https://randomuser.me/api/portraits/women/8.jpg",
        "domain": "Data Science",
        "experience": "5 years",
        "skills": "Python, SQL, Machine Learning",
        "company": "Walmart Labs",
        "email": "lakshmi.nair@example.com",
        "phone": "+91 9876123456",
        "bio": "Data scientist with a focus on machine learning models and data-driven decision making."
    },
    {
        "id": 17,
        "name": "Arjun Menon",
        "photo": "https://randomuser.me/api/portraits/men/9.jpg",
        "domain": "Mobile App Development",
        "experience": "4 years",
        "skills": "Android, Kotlin, Java",
        "company": "Swiggy",
        "email": "arjun.menon@example.com",
        "phone": "+91 9012345670",
        "bio": "Android developer with experience in building high-performance mobile applications."
    },
    {
        "id": 18,
        "name": "Meera Subramanian",
        "photo": "https://randomuser.me/api/portraits/women/9.jpg",
        "domain": "UI/UX Design",
        "experience": "8 years",
        "skills": "Adobe XD, Figma, User Research",
        "company": "UrbanClap",
        "email": "meera.subramanian@example.com",
        "phone": "+91 9876432101",
        "bio": "Senior UI/UX designer with a passion for crafting intuitive and engaging user experiences."
    }
]

mentors.extend([
    {
        "id": 3,
        "name": "Michael Chen",
        "photo": "https://randomuser.me/api/portraits/men/2.jpg",
        "domain": "Mobile App Development",
        "experience": "7 years",
        "skills": "iOS, Swift, Android, Kotlin, React Native",
        "company": "Apple",
        "email": "michael.chen@example.com",
        "phone": "+1 (345) 678-9012",
        "bio": "Passionate mobile app developer with expertise in both iOS and Android platforms."
    },
    {
        "id": 4,
        "name": "Sarah Johnson",
        "photo": "https://randomuser.me/api/portraits/women/2.jpg",
        "domain": "UX/UI Design",
        "experience": "9 years",
        "skills": "User Research, Wireframing, Prototyping, Figma, Adobe XD",
        "company": "Microsoft",
        "email": "sarah.johnson@example.com",
        "phone": "+1 (456) 789-0123",
        "bio": "Creative UX/UI designer focused on creating intuitive and engaging user experiences."
    },
    {
        "id": 5,
        "name": "David Kim",
        "photo": "https://randomuser.me/api/portraits/men/3.jpg",
        "domain": "Cybersecurity",
        "experience": "12 years",
        "skills": "Network Security, Ethical Hacking, Cryptography, CISSP",
        "company": "Cisco",
        "email": "david.kim@example.com",
        "phone": "+1 (567) 890-1234",
        "bio": "Experienced cybersecurity expert specializing in protecting organizations from digital threats."
    },
    {
        "id": 6,
        "name": "Emily Patel",
        "photo": "https://randomuser.me/api/portraits/women/3.jpg",
        "domain": "Product Management",
        "experience": "6 years",
        "skills": "Agile, Scrum, Product Strategy, Market Research",
        "company": "Airbnb",
        "email": "emily.patel@example.com",
        "phone": "+1 (678) 901-2345",
        "bio": "Dynamic product manager with a track record of launching successful tech products."
    },
    {
        "id": 7,
        "name": "Robert Taylor",
        "photo": "https://randomuser.me/api/portraits/men/4.jpg",
        "domain": "Cloud Computing",
        "experience": "10 years",
        "skills": "AWS, Azure, Google Cloud, Docker, Kubernetes",
        "company": "IBM",
        "email": "robert.taylor@example.com",
        "phone": "+1 (789) 012-3456",
        "bio": "Cloud computing expert helping businesses leverage the power of distributed computing."
    },
    {
        "id": 8,
        "name": "Lisa Wong",
        "photo": "https://randomuser.me/api/portraits/women/4.jpg",
        "domain": "Artificial Intelligence",
        "experience": "8 years",
        "skills": "Machine Learning, Deep Learning, NLP, TensorFlow, PyTorch",
        "company": "NVIDIA",
        "email": "lisa.wong@example.com",
        "phone": "+1 (890) 123-4567",
        "bio": "AI researcher and practitioner specializing in deep learning and natural language processing."
    },
    {
        "id": 9,
        "name": "Carlos Rodriguez",
        "photo": "https://randomuser.me/api/portraits/men/5.jpg",
        "domain": "Blockchain Development",
        "experience": "5 years",
        "skills": "Ethereum, Solidity, Smart Contracts, DApps",
        "company": "ConsenSys",
        "email": "carlos.rodriguez@example.com",
        "phone": "+1 (901) 234-5678",
        "bio": "Blockchain enthusiast developing decentralized applications and smart contracts."
    },
    {
        "id": 10,
        "name": "Anna Novak",
        "photo": "https://randomuser.me/api/portraits/women/5.jpg",
        "domain": "Data Engineering",
        "experience": "7 years",
        "skills": "Hadoop, Spark, SQL, NoSQL, ETL, Data Warehousing",
        "company": "Netflix",
        "email": "anna.novak@example.com",
        "phone": "+1 (012) 345-6789",
        "bio": "Data engineering professional specializing in building robust data pipelines and warehouses."
    }
])



WEIGHTS = {
    'company': 0.4,
    'domain': 0.3,
    'skills': 0.2,
    'experience': 0.1
}

def get_mentor_matches(mentee_profile):
    mentor_profiles = [
        {
            'profile': f"{m['company']} {m['domain']} {m['skills']} {m['experience']}",
            'company': m['company'],
            'domain': m['domain'],
            'skills': m['skills'],
            'experience': m['experience']
        }
        for m in mentors
    ]
    
    mentee_profile_data = {
        'profile': f"{request.form['company']} {request.form['domain']} {', '.join(request.form.getlist('skills'))} {request.form['experience']}",
        'company': request.form['company'],
        'domain': request.form['domain'],
        'skills': ', '.join(request.form.getlist('skills')),
        'experience': request.form['experience']
    }
    
    vectorizer = TfidfVectorizer()
    
    profiles = [m['profile'] for m in mentor_profiles] + [mentee_profile_data['profile']]
    tfidf_matrix = vectorizer.fit_transform(profiles)
    
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    scores = []
    for i, similarity in enumerate(cosine_similarities[0]):
        mentor = mentor_profiles[i]
        company_sim = 1 if mentee_profile_data['company'] == mentor['company'] else 0
        domain_sim = similarity if mentee_profile_data['domain'] == mentor['domain'] else 0
        skills_sim = similarity if set(mentee_profile_data['skills'].split(', ')).intersection(set(mentor['skills'].split(', '))) else 0
        experience_sim = similarity if mentee_profile_data['experience'] == mentor['experience'] else 0
        
        score = (WEIGHTS['company'] * company_sim +
                 WEIGHTS['domain'] * domain_sim +
                 WEIGHTS['skills'] * skills_sim +
                 WEIGHTS['experience'] * experience_sim)
        scores.append((i, score))
    
    sorted_mentors = sorted(scores, key=lambda x: x[1], reverse=True)
    top_matches = [mentors[i[0]] for i in sorted_mentors[:3]]
    return top_matches

def get_unique_values():
    domains = sorted(set(m['domain'] for m in mentors))
    skills = sorted(set(skill for m in mentors for skill in m['skills'].split(', ')))
    experiences = sorted(set(m['experience'] for m in mentors))
    companies = sorted(set(m['company'] for m in mentors))
    return domains, skills, experiences, companies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    domains, skills, experiences, companies = get_unique_values()
    return render_template('questionnaire.html', domains=domains, skills=skills, experiences=experiences, companies=companies)

@app.route('/match', methods=['POST'])
def match():
    mentee_profile = {
        'company': request.form['company'],
        'domain': request.form['domain'],
        'skills': ', '.join(request.form.getlist('skills')),
        'experience': request.form['experience']
    }
    matched_mentors = get_mentor_matches(mentee_profile)
    return render_template('results.html', mentors=matched_mentors)

@app.route('/mentor/<int:mentor_id>')
def mentor_profile(mentor_id):
    mentor = next((m for m in mentors if m['id'] == mentor_id), None)
    if mentor:
        return render_template('mentor_profile.html', mentor=mentor)
    return "Mentor not found", 404

@app.route('/mentors')
def mentors_page():
    return render_template('mentors.html', mentors=mentors)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
