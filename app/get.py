from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/users/{username}")
def get_data(username: str):
    response = github_get(f"https://api.github.com/users/{username}")

    return {
        "username": username,
        "user": response.json(), 
        "status code": response.status_code, 
        "remaining_requests": response.headers.get("X-RateLimit-Remaining")
    }

@app.get("/users/{username}/summary")
def get_user_summary(username: str):
    response = github_get(f"https://api.github.com/users/{username}")
    user = response.json()

    return {
        "username": user["login"],
        "name": user["name"],
        "profile_url": user["html_url"],
        "avatar_url": user["avatar_url"],
        "public_repos": user["public_repos"],
        "followers": user["followers"],
        "following": user["following"],
        "created_at": user["created_at"],
        "remaining_requests": response.headers.get("X-RateLimit-Remaining")
    }

@app.get("/users/{username}/repos")
def get_user_repos(username: str):
    response = github_get(f"https://api.github.com/users/{username}/repos")
    repos = response.json()

    cleaned_repos = []

    for repo in repos:
        cleaned_repos.append({
            "name": repo["name"],
            "full_name": repo["full_name"],
            "url": repo["html_url"],
            "description": repo["description"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "pushed_at": repo["pushed_at"]
        })

    return {
        "username": username,
        "repo_count": len(cleaned_repos),
        "repos": cleaned_repos,
        "remaining_requests": response.headers.get("X-RateLimit-Remaining")
    }

def github_get(url):
    headers = {
        "Authorization": f"Bearer {get_github_token()}",
        "Accept": "application/vnd.github+json"
    }

    return requests.get(
        url,
        headers=headers,
        timeout=10
    )

def get_github_token():
    with open("/run/secrets/github_token", "r") as file:
        return file.read().strip()
