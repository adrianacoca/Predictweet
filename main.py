from fastapi import FastAPI, Request, Form
from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return "Welcome to Predictweet"

# Generating HTML

@app.get("/generate")
def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Predictweet</title>
        </head>
        <body>
            <h1>Predictweet</h1>
            <form method=post enctype=application/x-www-form-urlencoded>
                <label for="fname">Twitter User:</label><br>
                <input type="text" name="uname" value=""><br>
                <input type="submit">
             </form>
             <p>Result: </p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

#class Item(BaseModel):
#    name:str

@app.post("/generate")
def get_input(uname:str =Form(...)):
    return getuser(uname)

"""
@app.get("/sentiment", response_class=ORJSONResponse)
async def read_items():
    return generate_html_response()

@app.post("/sentiment")
async def read_items(request: Request, user):
    return RedirectResponse("http://127.0.0.1:8000/sentiment/{user}")
"""
import src.extraction as ex
import src.sentiment as se
import src.graphs as gr

"""
@app.get("/sentiment/")"""
def getuser(user):
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
    except ValueError: 
        return "Too many requests, you will have to wait 15 minutes..."
