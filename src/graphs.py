import plotly.graph_objects as go
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
import plotly.express as px

def plot_sentiment(data, user):
    fig = go.Figure(data=go.Scatter(y=data['sentiments'],
                                mode='lines+markers',
                                text=(data['time'])))
    fig.update_layout(title=f"Sentiment Analysis of {user}'s twitter interactions")
    return fig.show()

def plot_retweets(data, user):
    fig = go.Figure(data=go.Scatter(y=data['retweets'],
                                    mode='lines+markers',
                                    #marker_color=df['sentiment'],
                                    text=data['time'])) # hover text goes here


    fig.update_layout(title=f"Sentiment Analysis of {user}'s twitter interactions")
    fig.show()

def sentiment_prediction(data, user):
    y_train = data["sentiments"][0:99]
    model = AR(y_train)
    model_fit = model.fit(maxlag=3)
    future_pred = model_fit.predict(start=99, end=105, dynamic=False)
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data['sentiments'],
                                    mode='lines+markers',
                                    name='ground truth',
                                    text=(data['time'])))
    fig.add_trace(go.Scatter(y=future_pred, x=list(range(99,105)),
                                    mode='lines+markers',
                                    name='predictions',
                                    text=(data['time'])))

    fig.update_layout(title=f"Sentiment Analysis of @{user} twitter interactions")
    fig.show()

def plot_hashtags(topics):
    fig = px.bar(topics, x="plot", y="Hashtag", color="Average Sentiment", template="seaborn")
    fig.show()