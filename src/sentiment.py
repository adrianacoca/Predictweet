from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_scores(sentence): 
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict['compound']

def sentiment_averages_vader(lst):
    l = []
    for e in lst: 
        l.append(sentiment_scores(e))
    return sum(l)/len(l)

