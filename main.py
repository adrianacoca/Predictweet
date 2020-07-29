from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

import src.extraction as ex
import src.sentiment as se
import src.graphs as gr

@app.get("/{user}")
async def getuser(user):
    try:
        user_t = ex.get_tweets(user)
        #creating DataFrame from json
        data = ex.create_data(user_t)
        #creating responses lists
        responses = ex.add_replies(user, data)
        data["responses"] = responses
        #extracting sentiments from responses list
        sentiments = []
        for i in range(len(data)):
            sentiments.append(se.sentiment_averages_vader(data["responses"][i]))
        data["sentiments"]=sentiments
        gr.sentiment_prediction(data, user)
        #create hashtags df
        topics = ex.get_hashtag(data)
        #plot hashtags df
        gr.plot_hashtags(topics)
    except KeyError:
        return "Too many requests, you will have to wait 15 minutes..."