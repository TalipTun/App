from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

"""

1. Create one route: /github/{username}
2. Call GitHub events API
3. Filter only PushEvent
4. Count commits
5. Return username + commit count + recent commit messages

"""

@app.get("/commitData")
def get_data():
    x = requests.get('https://api.github.com/users/TalipTun/events')
    print(x)
    return {
        "user ": x.json(), 
    }