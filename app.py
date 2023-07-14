import spacy
from flask import Flask, render_template, request
from gensim.summarization import summarize
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
    return render_template('results-text-analyse.html', result=result, stories=stories)

@app.route('/analyze-text', methods=['POST'])
def analyze1():
    print("Enter --ANALYZE TEXT --")
    nlp = spacy.load('en_core_web_sm')
    text = request.form['text']
    doc = nlp(text)


    try:
        # Create bullet point summary
        summary = []
        for sentence in doc.sents:
            sentence_summary = summarize(str(sentence))
            summary.append(sentence_summary)
    except:
        print("Summary Fail")
        #return render_template('error.html')


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
        "summary": summary
    }

    return render_template('results-text-analyse.html',
                           result=result,stories=stories)


if __name__ == '__main__':
    app.run()
