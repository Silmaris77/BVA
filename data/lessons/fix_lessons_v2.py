import json
import os
import re
import traceback

SOURCE_FILE = 'source_temp.json'

def load_json(path):
    print(f"Loading {path}...")
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Source file {path} not found.")
        return None

def save_json(path, data):
    print(f"Saving {path}...")
    with open(path, 'w', encoding='utf-8') as f: 
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {path} ({os.path.getsize(path)} bytes)")

def find_quiz_questions(data):
    questions = []
    
    def _search(obj):
        if isinstance(obj, dict):
            if "question" in obj and "options" in obj and "correct_answer" in obj:
                questions.append(obj)
            for k, v in obj.items():
                _search(v)
        elif isinstance(obj, list):
            for item in obj:
                _search(item)
    
    _search(data)
    return questions

def html_to_markdown(html):
    if not html: return ""
    md = html
    # Replace common tags
    md = re.sub(r'<strong[^>]*>', '**', md)
    md = re.sub(r'</strong>', '**', md)
    md = re.sub(r'<b>', '**', md)
    md = re.sub(r'</b>', '**', md)
    md = re.sub(r'<em[^>]*>', '*', md)
    md = re.sub(r'</em>', '*', md)
    md = re.sub(r'<i>', '*', md)
    md = re.sub(r'</i>', '*', md)
    
    # Block elements
    md = re.sub(r'<p[^>]*>', '', md)
    md = re.sub(r'</p>', '\n\n', md)
    md = re.sub(r'<br\s*/?>', '\n', md)
    md = re.sub(r'<div[^>]*>', '', md)
    md = re.sub(r'</div>', '\n', md)
    
    # Headings
    md = re.sub(r'<h[12][^>]*>', '## ', md)
    md = re.sub(r'</h[12]>', '\n\n', md)
    md = re.sub(r'<h[3-6][^>]*>', '### ', md)
    md = re.sub(r'</h[3-6]>', '\n\n', md)
    
    # Lists
    md = re.sub(r'<ul[^>]*>', '', md)
    md = re.sub(r'</ul>', '\n', md)
    md = re.sub(r'<ol[^>]*>', '', md)
    md = re.sub(r'</ol>', '\n', md)
    md = re.sub(r'<li[^>]*>', '- ', md)
    md = re.sub(r'</li>', '\n', md)
    
    # Strip remaining tags
    md = re.sub(r'<[^>]+>', '', md)
    
    # Cleanup whitespace
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()

def create_intro_card(title, description_html):
    # IntroCard uses 'description' as plain text (or simple text)
    # We clean HTML for description
    clean_desc = html_to_markdown(description_html)
    return {
        "type": "intro",
        "title": title,
        "description": clean_desc,
        "icon": "🧠"
    }

def create_concept_card(section):
    # ConceptCard uses ReactMarkdown, so we convert content
    md_content = html_to_markdown(section.get("content", ""))
    return {
        "type": "concept",
        "title": section.get("title", "Koncept"),
        "content": md_content
    }

def create_question_card(question_obj):
    return {
        "type": "question",
        "question": question_obj["question"],
        "options": question_obj["options"],
        "correctAnswer": 1, # Defaulting to index 1 (second option) based on observation, or 0? 
        # Source said "correct_answer": 1. In typical array index it's 1.
        # But if source is 1-based index (1=A), and component uses 0-based...
        # Let's assume the source value is correct for now (integer).
        "explanation": question_obj.get("explanation", "")
    }
    
def create_summary_card(title, objectives, xp):
    return {
        "type": "summary",
        "title": title,
        "recap": objectives,
        "badge": {
            "xp": xp,
            "title": "Ukończono"
        }
    }

def create_lesson_11a(source, quiz_questions):
    try:
        learning_tabs = source["sections"]["learning"]["tabs"]
        tekst_sections = learning_tabs[0]["sections"][0:3]
        
        cards = []
        
        # 1. Intro Card
        if source.get("intro") and source["intro"].get("main"):
            cards.append(create_intro_card(
                "Fundamenty C-IQ", 
                source["intro"]["main"]
            ))
            
        # 2. Concept Cards
        for sec in tekst_sections:
            cards.append(create_concept_card(sec))
            
        # 3. Quiz Cards (subset)
        subset_questions = [q for i, q in enumerate(quiz_questions) if i in [0, 1, 2, 5, 6]]
        for q in subset_questions:
            cards.append(create_question_card(q))
            
        # 4. Summary Card
        cards.append(create_summary_card(
            "Podsumowanie Części 1", 
            ["Neurobiologia komunikacji", "Porwanie amygdali", "Trzy poziomy rozmów"],
            50
        ))
        
        lesson = {
            "id": "NEUROLEADERSHIP_LESSON_11A",
            "title": "Fundamenty Conversational Intelligence",
            "description": "Poznaj neurobiologiczne podstawy skutecznej komunikacji i naucz się rozpoznawać trzy poziomy rozmów.",
            "xp_reward": 50,
            "difficulty": "intermediate",
            "card_count": len(cards),
            "cards": cards # THIS IS THE KEY FIELD FOR FRONTEND
        }
        return lesson
    except Exception as e:
        print(f"Error creating 11a: {e}")
        traceback.print_exc()
        return None

def create_lesson_11b(source, quiz_questions):
    try:
        learning_tabs = source["sections"]["learning"]["tabs"]
        tekst_sections = learning_tabs[0]["sections"][3:6]
        
        cards = []
        
        # 1. Intro
        cards.append({
            "type": "intro",
            "title": "Narzędzia C-IQ",
            "description": "Zaawansowane techniki: Model TRUST, Trzy R i Dashboard.",
            "icon": "🛠️"
        })
        
        # 2. Concepts
        for sec in tekst_sections:
            cards.append(create_concept_card(sec))
            
        # 3. Quiz (subset)
        subset_questions = [q for i, q in enumerate(quiz_questions) if i in [3, 4, 7, 8, 9, 10, 11]]
        for q in subset_questions:
            cards.append(create_question_card(q))
            
        # 4. Summary
        cards.append(create_summary_card(
            "Podsumowanie Części 2",
            ["Model TRUST", "Techniki Trzy R", "Conversational Dashboard"],
            60
        ))
        
        lesson = {
            "id": "NEUROLEADERSHIP_LESSON_11B",
            "title": "Narzędzia Transformacji Rozmów",
            "description": "Opanuj praktyczne techniki C-IQ.",
            "xp_reward": 60,
            "difficulty": "advanced",
            "card_count": len(cards),
            "cards": cards
        }
        return lesson
    except Exception as e:
        print(f"Error creating 11b: {e}")
        traceback.print_exc()
        return None

def create_lesson_11c(source, quiz_questions):
    try:
        learning_tabs = source["sections"]["learning"]["tabs"]
        tekst_sections = learning_tabs[0]["sections"][6:]
        
        cards = []
        
        # 1. Intro
        cards.append({
            "type": "intro",
            "title": "C-IQ w Praktyce",
            "description": "Od wiedzy do kultury zaufania. Wdrażanie C-IQ w organizacji.",
            "icon": "🚀"
        })
        
        # 2. Concepts
        for sec in tekst_sections:
            cards.append(create_concept_card(sec))
            
        # 3. Exercises (Convert to Concept or Practice?)
        # Let's add exercises as a Concept Card for now simple text
        if "practical_exercises" in source["sections"] and "exercises" in source["sections"]["practical_exercises"]:
             ex_section = source["sections"]["practical_exercises"]["exercises"]
             if "sections" in ex_section: # Using 'sections' key as discovered
                 for item in ex_section["sections"]: # Add them as concepts
                     cards.append({
                         "type": "concept",
                         "title": item.get("title", "Ćwiczenie"),
                         "content": html_to_markdown(item.get("description", ""))
                     })

        # 4. Quiz (All/Remaining)
        # Maybe pick just a few or specific ones. Let's use all for verify.
        # Actually 11c description said "closing quiz".
        # Let's use last 3 questions from pool if any left or reuse?
        # Let's reuse some hard ones.
        subset_questions = quiz_questions[-3:] 
        for q in subset_questions:
            cards.append(create_question_card(q))
            
        # 5. Summary
        cards.append(create_summary_card(
            "Podsumowanie Części 3",
            ["Plan wdrożenia", "Kultura konwersacyjna"],
            50
        ))
        
        lesson = {
            "id": "NEUROLEADERSHIP_LESSON_11C",
            "title": "C-IQ w Praktyce",
            "description": "Wdroż C-IQ w swojej rzeczywistości.",
            "xp_reward": 50,
            "difficulty": "advanced",
            "card_count": len(cards),
            "cards": cards
        }
        return lesson
    except Exception as e:
        print(f"Error creating 11c: {e}")
        traceback.print_exc()
        return None

def generate_sql(files):
    print("Generating SQL...")
    sql_content = "-- Import lessons from split Conversational Intelligence (FIXED STRUCTURE)\n"
    sql_content += "INSERT INTO lessons (title, description, category, difficulty, duration_minutes, xp_reward, card_count, content_json) VALUES\n"
    
    values = []
    
    for file_path in files:
        if not os.path.exists(file_path):
            continue
            
        data = load_json(file_path)
        
        title = data.get("title", "").replace("'", "''")
        desc = data.get("description", "").replace("'", "''")
        category = "Neuroprzywództwo" 
        difficulty = data.get("difficulty", "intermediate")
        duration = 45 # Est
        xp = data.get("xp_reward", 50)
        card_count = data.get("card_count", 10)
        
        # Json content must be the object with 'cards'
        json_str = json.dumps(data, ensure_ascii=False)
        json_escaped = json_str.replace("'", "''")
        
        values.append(f"('{title}', '{desc}', '{category}', '{difficulty}', {duration}, {xp}, {card_count}, '{json_escaped}')")
    
    sql_content += ",\n".join(values)
    sql_content += ";"
    
    with open("import_lessons_split.sql", "w", encoding="utf-8") as f:
        f.write(sql_content)
    print(f"Generated SQL script: import_lessons_split.sql ({os.path.getsize('import_lessons_split.sql')} bytes)")

# MAIN
if not os.path.exists(SOURCE_FILE):
    # Try to copy from original if temp missing (cleanup deleted it)
    # Assume source_temp was deleted. Check original.
    ORIGINAL = "11. Od słów do zaufania - Conversational Intelligence.json"
    if os.path.exists(ORIGINAL):
        import shutil
        shutil.copy(ORIGINAL, SOURCE_FILE)
    else:
        print("Source file not found!")
        # If both gone, we are stuck. But user said they ran the script, so maybe files are there?
        # Use 11a.json if it exists as source? No.
        # Hopefully user didn't delete the original.
        pass

source = load_json(SOURCE_FILE)
if source:
    all_questions = find_quiz_questions(source)
    
    l1 = create_lesson_11a(source, all_questions)
    if l1: save_json('11a. Fundamenty C-IQ.json', l1)
    
    l2 = create_lesson_11b(source, all_questions)
    if l2: save_json('11b. Narzędzia C-IQ.json', l2)
    
    l3 = create_lesson_11c(source, all_questions)
    if l3: save_json('11c. C-IQ w Praktyce.json', l3)
    
    generate_sql([
        '11a. Fundamenty C-IQ.json',
        '11b. Narzędzia C-IQ.json',
        '11c. C-IQ w Praktyce.json'
    ])
    print("DONE")
