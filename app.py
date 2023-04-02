import spacy
from flask import Flask, render_template ,request
from gensim.summarization import summarize
from textblob import TextBlob

app = Flask(__name__)


@app.route('/')
def home():
    print("Default PUSH")
    text = "This is a sample text. Please modify your text and submit to see the results. Text Analysis is a powerful tool that allows you to extract valuable insights from any written text. Whether you're a student, researcher, or business professional, being able to analyze and understand text is a critical skill. With Text Analysis, you can identify the most common nouns, verbs, and adjectives in your text, and gain a better understanding of the language being used. You can also identify the overall tone of the text, which can be helpful in determining whether the author is expressing a positive or negative sentiment. Additionally, Text Analysis can provide you with a summary of the text, which can be useful if you're short on time or need to quickly understand the main points of a longer document."

    nouns = ["sample text", "results", "Text Analysis", "tool", "insights", "text", "student", "researcher",
             "business professional", "skill", "nouns", "verbs", "adjectives", "language", "tone", "author",
             "sentiment", "summary", "time", "document"]
    verbs = ["modify", "submit", "allows", "extract", "being", "analyze", "understand", "identify", "gain", "helpful",
             "determining", "expressing", "provide", "useful", "short", "need"]
    adjectives = ["powerful", "valuable", "critical", "common", "overall", "positive", "negative", "main", "longer"]
    other_words = ["This", "is", "a", "please", "your", "to", "you", "can", "also", "of", "which", "in", "or", "if",
                   "on", "the", "and", "then", "few", "lines", "explaining", "what", "built", "by", "Anuj", "Dwivedi",
                   "-", "name", "ok"]
    tone = "informative"
    word_count = 95
    char_count = 498
    summary = "Text Analysis is a powerful tool that can help you identify key insights and trends in any written text. With this tool, you can quickly analyze text to identify the most common nouns, verbs, and adjectives, as well as the overall tone and sentiment. This can be particularly helpful for students, researchers, and business professionals who need to quickly understand large volumes of text."
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

    return render_template('results-text-analyse.html',result=result)


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
                           result=result)


if __name__ == '__main__':
    app.run()
