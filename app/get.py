from fastapi import FastAPI # type: ignore
import requests # type: ignore
from datetime import datetime, timezone, timedelta
from app.database import engine
from app.models import Base
from app.database import SessionLocal # type: ignore
from app.models import Commit
from sqlalchemy import select

app = FastAPI()

Base.metadata.create_all(bind=engine)

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

def convert(date_time):
    format = '%b %d %Y %I:%M%p'
    datetime_str = datetime.datetime.strptime(date_time, format)
    return datetime_str

@app.get("/users/{username}/{repo}/commits")
def get_user_repo_commits(username: str, repo: str):

    try:
        response = github_get(f"https://api.github.com/repos/{username}/{repo}/commits")
        commits = response.json()
        session = SessionLocal()
        now = datetime.now(timezone.utc)

        daily_cutoff = now - timedelta(days=1)
        weekly_cutoff = now - timedelta(days=7)
        monthly_cutoff = now - timedelta(days=30)

        dayCount = 0
        weekCount = 0
        monthCount = 0

        for commit in commits:
            # message = commit["commit"]["message"] 
            sha = commit["sha"]
            date = datetime.fromisoformat(
                commit["commit"]["committer"]["date"].replace("Z", "+00:00")
            )

            if date > daily_cutoff:
                dayCount += 1
            if date > weekly_cutoff:
                weekCount += 1
            if date > monthly_cutoff:
                monthCount += 1

            existing_commit = session.execute(
                select(Commit).where(Commit.sha == sha)
            ).scalar_one_or_none()

            if existing_commit is None:
                newCommit = Commit(
                    username=username,
                    repo_name=repo,
                    committed_at=date,
                    sha=sha
                )

                session.add(newCommit)

        session.commit()

        stmt = select(Commit)
        result = session.execute(stmt)
        sqlCommits = result.scalars().all()

        return {
            "count" : len(sqlCommits),
            "last 24h" : dayCount,
            "last week" : weekCount,
            "last month" : monthCount,
            "SQLCOMMITS" : sqlCommits
        }

    finally: 
        session.close()

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
