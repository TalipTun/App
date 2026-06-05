# GitPulse

Make sure you have docker installed and then type in your terminal:

<code> docker compose build </code>

<code>  docker compose up </code>

Your application will start working at 0.0.0.0:8000 after installing necessary files and modules

# GitPulse

GitPulse is a Dockerized FastAPI backend that integrates with the GitHub API to retrieve repository activity, commit history, and developer statistics.

The goal of the project is to explore backend engineering concepts including API integrations, containerization, secret management, databases, and analytics.

## Technologies Used

* Python
* FastAPI
* Docker
* Docker Compose
* PostgreSQL
* Adminer
* GitHub REST API

---

# What I Learned

## FastAPI

FastAPI is a Python framework used to build APIs.

Example:

```python
@app.get("/users/{username}")
def get_user(username: str):
    ...
```

The decorator registers a route and associates it with the function below it.

Request flow:

```
Browser
↓
FastAPI Route
↓
Python Function
↓
JSON Response
```

---

## Docker

Docker allows applications to run inside containers.

Benefits:

* Consistent environment
* Easy deployment
* Isolation between services

This project uses three containers:

### Backend Container

Runs FastAPI.

### PostgreSQL Container

Stores application data.

### Adminer Container

Provides a web interface for interacting with PostgreSQL.

---

## Dockerfile

The Dockerfile defines how the backend image is built.

Example:

```dockerfile
FROM python:3.12-slim
```

Uses a lightweight Python 3.12 image.

```dockerfile
WORKDIR /code
```

Sets the working directory inside the container.

```dockerfile
COPY ./app /code/app
```

Copies application files into the image.

```dockerfile
CMD [...]
```

Starts the FastAPI server when the container launches.

---

## Docker Compose

Docker Compose orchestrates multiple containers.

This project uses:

```text
backend
db
adminer
```

Compose automatically creates a network so containers can communicate.

For example:

```python
host="db"
```

connects the backend container to PostgreSQL.

---

## Ports

Port mappings:

```yaml
8000:8000
5432:5432
8080:8080
```

Meaning:

```
Host Port
↓
Container Port
```

Examples:

```
localhost:8000 → FastAPI
localhost:5432 → PostgreSQL
localhost:8080 → Adminer
```

---

## Volumes

Volumes persist data outside containers.

Example:

```yaml
postgres_data:/var/lib/postgresql/data
```

Without volumes:

```
Delete container
↓
Lose database
```

With volumes:

```
Delete container
↓
Database survives
```

---

## Docker Secrets

GitHub tokens and database passwords should never be committed to GitHub.

This project uses Docker Secrets.

Example:

```yaml
secrets:
  github_token:
    file: ./secrets/github_token.txt
```

Inside the container:

```text
/run/secrets/github_token
```

Benefits:

* Not stored in source code
* Not committed to GitHub
* Injected at runtime

---

## .gitignore

Prevents files from being tracked by Git.

Examples:

```text
__pycache__/
secrets/
```

Important:

`.gitignore` does not remove files already tracked by Git.

---

## .dockerignore

Prevents files from being sent to Docker during image builds.

Examples:

```text
secrets/
.git
__pycache__/
```

Benefits:

* Smaller images
* Faster builds
* Better security

---

## GitHub API

The application uses authenticated GitHub API requests.

Example:

```python
response = github_get(
    "https://api.github.com/users/TalipTun"
)
```

Authenticated requests increase the rate limit from:

```
60 requests/hour
```

to:

```
5000 requests/hour
```

---

## Dynamic Routes

Example:

```python
/users/{username}
```

FastAPI automatically extracts path parameters.

Request:

```text
/users/TalipTun
```

Result:

```python
username = "TalipTun"
```

---

## Commit Analytics

The application retrieves commit history and calculates:

* Last 24 hours
* Last 7 days
* Last 30 days

GitHub dates are converted into Python datetime objects:

```python
datetime.fromisoformat(
    date.replace("Z", "+00:00")
)
```

Time windows are calculated using:

```python
timedelta(days=1)
timedelta(days=7)
timedelta(days=30)
```

---

## PostgreSQL

PostgreSQL is used as the project's database.

Current workflow:

```
GitHub API
↓
FastAPI
↓
PostgreSQL
```

Future goal:

```
GitHub API
↓
Store Commits
↓
PostgreSQL
↓
Analytics
↓
Leaderboards
```

---

## Adminer

Adminer is a browser-based database management tool.

Access:

```
http://localhost:8080
```

Used for:

* Creating tables
* Inserting rows
* Running SQL queries
* Viewing data

Example query:

```sql
SELECT * FROM test;
```

## Accessing PostgreSQL Through the Terminal

While Adminer provides a graphical interface, PostgreSQL can also be accessed directly from the terminal.

Connect to the PostgreSQL container:

```bash
docker compose exec db psql -U gitpulse_user -d gitpulse_db
```

Explanation:

```text
docker compose exec
↓
Run a command inside a running container

db
↓
The PostgreSQL service name

psql
↓
PostgreSQL command-line client

-U gitpulse_user
↓
Database username

-d gitpulse_db
↓
Database name
```

Successful connection:

```text
gitpulse_db=#
```

Common commands:

List all tables:

```sql
\dt
```

Describe a table:

```sql
\d table_name
```

Example:

```sql
\d commits
```

View all rows:

```sql
SELECT * FROM test;
```

Count rows:

```sql
SELECT COUNT(*) FROM test;
```

View current database:

```sql
SELECT current_database();
```

Exit PostgreSQL:

```sql
\q
```

This approach is useful for debugging, inspecting data, and understanding how applications interact with databases behind the scenes.

Request Flow:

```text
Terminal
↓
psql
↓
PostgreSQL Container
↓
Database
↓
Query Results
```

---

# Future Roadmap

* Store commit history in PostgreSQL
* Build user activity analytics
* Daily leaderboard
* Weekly leaderboard
* Monthly leaderboard
* Scheduled GitHub synchronization
* Deploy to AWS
* Migrate PostgreSQL to RDS

---

# Key Takeaway

This project evolved from a simple GitHub API experiment into a complete backend system involving:

* API Integration
* Docker
* Secret Management
* PostgreSQL
* Database Administration
* Backend Analytics

The primary objective is to understand how production backend systems are designed, deployed, and maintained.
