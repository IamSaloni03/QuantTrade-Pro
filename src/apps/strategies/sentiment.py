# src/apps/strategies/sentiment.py

from textblob import TextBlob

def get_sentiment_score(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # -1 to +1


def get_market_sentiment():
    # Static sample headlines (for demo)
    headlines = [
        "Market shows strong bullish momentum",
        "Investors optimistic about economic growth",
        "Stock prices surge amid positive earnings",
    ]

    scores = [get_sentiment_score(h) for h in headlines]

    return sum(scores) / len(scores) if scores else 0