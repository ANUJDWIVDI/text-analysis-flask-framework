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
    # Add more stories here
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
