import os

import PyPDF2
import spacy
from flask import Flask, render_template, request
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from textblob import TextBlob

app = Flask(__name__)

# Dictionary of stories
stories = [
    {
        "title": "The Magical Forest",
        "tone": "positive",
        "paragraph": "Once upon a time, in a magical forest far away, there lived a group of friendly animals. They would spend their days playing and helping each other. The forest was filled with colorful flowers and sparkling streams. It was a place of joy and wonder."
    },
    {
        "title": "The Mischievous Goblin",
        "tone": "negative",
        "paragraph": "In a small village, there was a mischievous goblin causing trouble everywhere. He would hide people's belongings and create chaos. The villagers were scared and annoyed by his antics. They decided to come up with a plan to teach the goblin a lesson."
    },
    {
        "title": "The Enchanted Castle",
        "tone": "neutral",
        "paragraph": "Once, there was an enchanted castle on top of a hill. It was said to hold many secrets and treasures. Many adventurers tried to uncover its mysteries, but only a few succeeded. The castle had hidden rooms, secret passages, and magical artifacts."
    },
    {
        "title": "The Brave Knight",
        "tone": "positive",
        "paragraph": "In the kingdom of Elysia, there was a brave knight named Sir Arthur. He was known for his unwavering courage and chivalry. Sir Arthur embarked on daring quests to protect the realm from evil forces and restore peace and justice."
    },
    {
        "title": "The Mysterious Island",
        "tone": "neutral",
        "paragraph": "Deep in the heart of the vast ocean, there lay a mysterious island shrouded in mist. Legends spoke of hidden treasures and mythical creatures dwelling on its shores. Many adventurers set sail in search of this enigmatic island, but few returned with tales to tell."
    },
    {
        "title": "The Secret Garden",
        "tone": "positive",
        "paragraph": "Behind the old mansion, there was a secret garden untouched by time. Its lush greenery and vibrant flowers created a serene oasis. The garden held the power to heal and bring joy to those who discovered its hidden beauty."
    },
    {
        "title": "The Lost City",
        "tone": "neutral",
        "paragraph": "Buried deep within the dense jungle, there existed a lost city filled with ancient ruins and untold stories. The city held the remnants of a once-great civilization, waiting to be unraveled by curious explorers."
    },
    {
        "title": "The Haunted Manor",
        "tone": "negative",
        "paragraph": "On a desolate hill, stood a haunted manor with a dark past. Its halls echoed with ghostly whispers, and shadows danced along its decaying walls. Many believed the manor was cursed, and dared not venture near after sunset."
    },
    {
        "title": "The Time Traveler's Journal",
        "tone": "positive",
        "paragraph": "Within the pages of an ancient journal, a time traveler chronicled their extraordinary adventures across different eras. From the majestic courts of Renaissance Europe to the futuristic landscapes of the 31st century, the journal revealed the wonders and perils of time travel."
    },
    {
        "title": "The Legendary Sword",
        "tone": "neutral",
        "paragraph": "Legends spoke of a mythical sword with the power to vanquish any foe. It was said to be hidden deep within a treacherous mountain range, guarded by fierce creatures and ancient traps. Many warriors set out on a quest to wield this legendary weapon and bring peace to the land."
    }
]

@app.route('/')
def home():
    return render_template('start.html')


@app.route('/analyze-pdf', methods=['POST'])
def analyze_pdf():
    # Get the uploaded PDF file from the request
    pdf_file = request.files['pdfFile']

    # Get the page range from the form input
    page_range = request.form.get('pageRange')
    start_page, end_page = None, None
    if page_range:
        start_page, end_page = map(int, page_range.split('-'))

    # Process the PDF file and extract text from paragraphs within the specified range
    # Process the PDF file and extract text from paragraphs within the specified range
    paragraphs = []
    if pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)  # Number of pages
        if start_page is None:
            start_page = 1
        if end_page is None or end_page > num_pages:
            end_page = num_pages
        for page_number in range(start_page, end_page + 1):
            page = pdf_reader.pages[page_number - 1]
            page_text = page.extract_text()
            paragraphs.extend(page_text.split('\n\n'))  # Extract paragraphs based on double line breaks


    # Perform sentiment analysis and parts of speech analysis for each paragraph
    sentiment_results = []
    page_analysis = []
    nlp = spacy.load('en_core_web_sm')
    total_words = 0
    current_page_number = start_page
    for i, paragraph in enumerate(paragraphs, start=1):
        doc = nlp(paragraph)

        # Discard paragraphs with less than 10 words
        word_count = len(doc)
        if word_count < 10:
            continue

        # Identify parts of speech
        nouns = []
        verbs = []
        adjectives = []
        other_words = []
        for token in doc:
            if token.pos_ == 'NOUN':
                nouns.append(token.text)
            elif token.pos_ == 'VERB':
                verbs.append(token.text)
            elif token.pos_ == 'ADJ':
                adjectives.append(token.text)
            else:
                other_words.append(token.text)

        # Identify tone
        tone = 'neutral'
        sentiment_score = TextBlob(paragraph).sentiment.polarity
        if sentiment_score > 0:
            tone = 'positive'
        elif sentiment_score < 0:
            tone = 'negative'

        # Count words and characters
        char_count = len(paragraph)

        # Store sentiment analysis results
        sentiment_results.append({
            "page_number": current_page_number,  # Append current page number
            "paragraph_number": i,  # Append paragraph number
            "paragraph": paragraph,
            "sentiment": sentiment_score,
            "tone": tone,
        })

        # Store page analysis results
        page_analysis.append({
            "line_number": i,
            "paragraph_number": i,  # Use line number as paragraph number
            "page_number": current_page_number,
            "nouns": nouns,
            "verbs": verbs,
            "adjectives": adjectives,
            "others": other_words,
            "sentiment": tone,
            "word_count": word_count,
        })

        total_words += word_count

        # Increment current page number when reaching the last paragraph of a page
        if i % len(pdf_reader.pages[current_page_number - 1].extract_text().split('\n\n')) == 0:
            current_page_number += 1

        # Generate the PDF file using reportlab
        pdf_filename = 'analysis_results.pdf'
        generate_pdf(sentiment_results, page_analysis, pdf_filename)

    # Render the template and pass the sentiment analysis, page analysis, and additional analysis results
    return render_template('results-pdf.html', sentiment_results=sentiment_results, page_analysis=page_analysis, num_pages=end_page-start_page+1, total_words=total_words,pdf_filename=pdf_filename)

@app.route('/sample')
def sample():
    text = "This is a sample text. Please modify your text and submit to see the results."
    result = {
        "text": text,
        "nouns": [],
        "verbs": [],
        "adjectives": [],
        "other": [],
        "tone": "neutral",
        "word_count": 0,
    }
    return render_template('index.html', result=result, stories=stories)





def generate_pdf(sentiment_results, page_analysis, filename):
    # Create a new PDF document
    doc = SimpleDocTemplate(os.path.join('static', filename), pagesize=A4)

    try: # Define the styles for the PDF table
        styles = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Create the sentiment analysis table
        sentiment_data = [['Page Number', 'Paragraph Number', 'Paragraph', 'Tone', 'Sentiment']]
        for result in sentiment_results:
            sentiment_data.append([result['page_number'], result['paragraph_number'], result['paragraph'], result['tone'], result['sentiment']])
        sentiment_table = Table(sentiment_data, style=styles)

        # Create the page analysis table
        page_data = [['Line Number', 'Paragraph Number', 'Nouns', 'Verbs', 'Adjectives', 'Others', 'Sentiment', 'Word Count']]
        for analysis in page_analysis:
            page_data.append([analysis['line_number'], analysis['paragraph_number'], ', '.join(analysis['nouns']), ', '.join(analysis['verbs']), ', '.join(analysis['adjectives']), ', '.join(analysis['others']), analysis['sentiment'], analysis['word_count']])
        page_table = Table(page_data, style=styles)

        # Build the PDF document
        elements = [sentiment_table, page_table]
        doc.build(elements)
    except:
        print("Not Feasible")





@app.route('/analyze-text', methods=['POST'])
def analyze1():
    print("Enter --ANALYZE TEXT --")
    nlp = spacy.load('en_core_web_sm')
    text = request.form['text']
    doc = nlp(text)

    # Identify parts of speech
    nouns = []
    verbs = []
    adjectives = []
    other_words = []
    for token in doc:
        if token.pos_ == 'NOUN':
            nouns.append(token.text)
        elif token.pos_ == 'VERB':
            verbs.append(token.text)
        elif token.pos_ == 'ADJ':
            adjectives.append(token.text)
        else:
            other_words.append(token.text)

    print(nouns)
    print(nouns)
    print(verbs)
    print(adjectives)
    print(other_words)

    # Identify tone
    tone = 'neutral'
    sentiment_score = TextBlob(text).sentiment.polarity
    if sentiment_score > 0:
        tone = 'positive'
    elif sentiment_score < 0:
        tone = 'negative'

    # Count words and characters
    word_count = len(doc)
    char_count = len(text)
    print(word_count)
    print(char_count)



    print("Exit --ANALYZE TEXT --")

    result = {
        "text": text,
        "nouns": nouns,
        "verbs": verbs,
        "adjectives": adjectives,
        "other": other_words,
        "tone": tone,
        "word_count": word_count,
        "char_count": char_count,
    }

    return render_template('index.html',
                           result=result, stories=stories)


if __name__ == '__main__':
    app.run()
