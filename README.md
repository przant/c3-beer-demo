# 🍺 C3 Beer Analysis Demo - Containerization Benefits

A fun, educational demo showing how containers solve research reproducibility problems using a beer dataset.

## The Problem We're Solving

**Scenario familiar to every researcher:**

👨‍🔬 **Researcher A** (2024): 
```bash
"Works on my machine! Python 3.9, just pip install these..."
```

👩‍🔬 **Researcher B** (6 months later):
```bash
"Error: ModuleNotFoundError... wait, which PostgreSQL version?"
"Why doesn't this work?! 😤"
```

**Root causes:**
- Different Python versions on different machines
- Database version mismatches
- Dependency conflicts ("pandas 2.0 broke everything!")
- Missing documentation ("where's the setup script?")
- The dreaded "works on my machine" syndrome

## The Container Solution

**Everyone gets the exact same environment. Period.**

```bash
docker compose up
# Done. It just works. ✅
```

No more:
- ❌ "Which Python version do I need?"
- ❌ "How do I install PostgreSQL?"
- ❌ "What were those pip packages again?"
- ❌ "Why does this work for you but not me?"

---

## What This Demo Shows

### 1. **Layer Reuse (Don't Rebuild Everything)**

Instead of every researcher installing:
- Python interpreter
- PostgreSQL client tools
- Common libraries (pandas, psycopg2)
- System dependencies

**We build a base image once, reuse it everywhere:**

```dockerfile
# base-python/Dockerfile
FROM python:3.11-slim-bookworm
RUN apt-get install postgresql-client
RUN pip install pandas psycopg2-binary
```

Then each algorithm just adds its specific needs:

```dockerfile
# algorithm-xxx/Dockerfile
FROM base-python:latest   # ← Reuse everything from base!
COPY analyze.py .
CMD ["python", "analyze.py"]
```

**Benefits:**
- Faster builds (don't reinstall Python every time)
- Consistency (everyone uses same Python/library versions)
- Less disk space (Docker shares layers between containers)

### 2. **Template Reusability**

Want to run a different analysis? **Change one line:**

```yaml
# docker-compose.yml

# Run average ABV analysis
services:
  avg-abv:
    build: ./algorithm-avg-abv  # ← This line

# Want different analysis? Change to:
  top-breweries:
    build: ./algorithm-top-breweries  # ← Just this!
```

Everything else (database, data loading, configuration) stays the same.

### 3. **One Command Deployment**

```bash
docker compose up
```

This single command:
1. Builds base Python image (if needed)
2. Builds algorithm image (if needed)
3. Starts PostgreSQL database
4. Loads beer dataset automatically
5. Runs your analysis
6. Shows results

No manual steps. No "don't forget to...". It just works.

---

## Project Structure

```
c3-beer-demo/
├── docker-compose.yml           # Orchestration (the magic command)
├── dataset/
│   └── beers.csv                # 60 fictional beers
├── base-python/
│   └── Dockerfile               # Base image (Python + PostgreSQL + pandas)
├── database/
│   ├── Dockerfile               # PostgreSQL with auto-loader
│   └── init.sql                 # Table creation + data import
├── algorithm-avg-abv/
│   ├── Dockerfile               # Inherits from base-python
│   ├── requirements.txt
│   └── analyze.py               # Calculate avg ABV by style
└── algorithm-top-breweries/
    ├── Dockerfile               # Same base, different analysis
    ├── requirements.txt
    └── analyze.py               # Find most productive breweries
```

---

## Quick Start

### Prerequisites

- Docker installed ([get it here](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)

### Run the Demo

```bash
# Clone this repo
git clone <your-repo-url>
cd c3-beer-demo

# Build the base image first (one-time setup)
docker build -t base-python:latest ./base-python

# Run the analysis
docker compose up

# Watch the magic happen! 🎉
```

**What you'll see:**
1. PostgreSQL starts and loads beer data
2. Analysis algorithm runs
3. Results print to console
4. Everything shuts down cleanly

### Switch to Different Algorithm

Edit `docker-compose.yml`:

```yaml
# Comment out the current algorithm
# avg-abv:
#   build: ./algorithm-avg-abv
#   ...

# Uncomment the one you want
top-breweries:
  build: ./algorithm-top-breweries
  ...
```

Then run again:
```bash
docker compose up --build
```

---

## Understanding the Architecture

### Component Flow

```
┌─────────────────────────────────────────┐
│  docker-compose.yml                     │
│  (Orchestrates everything)              │
└────────┬────────────────────────────────┘
         │
         ├──► database (PostgreSQL)
         │    ├─ Loads beers.csv automatically
         │    └─ Creates tables and indexes
         │
         └──► algorithm (Python)
              ├─ Waits for database to be ready
              ├─ Connects via environment variables
              └─ Runs analysis and prints results
```

### Why This Pattern Works for Research

**Problem:** Research teams need to:
- Share analysis methods
- Reproduce results months/years later
- Run same analysis on different datasets
- Collaborate across different machines/OS

**Solution:** Containerized templates provide:
- ✅ Exact same environment for everyone
- ✅ Version-controlled infrastructure (Dockerfiles in git)
- ✅ Easy to swap datasets (just change the CSV)
- ✅ Easy to swap algorithms (just change docker-compose.yml)
- ✅ No installation instructions needed (it's all automated)

---

## Teaching Points for José Luis

### 1. Layer Caching Makes Everything Fast

First build (base image):
```
Step 1/5 : FROM python:3.11-slim-bookworm   ← Download Python
Step 2/5 : RUN apt-get install ...          ← Install PostgreSQL client
Step 3/5 : RUN pip install pandas ...       ← Install libraries
```

Second build (algorithm):
```
Step 1/3 : FROM base-python:latest          ← CACHED! (instant)
Step 2/3 : COPY analyze.py                  ← Only new stuff
Step 3/3 : CMD ["python", "analyze.py"]     ← Done in seconds
```

**Key insight:** Docker caches layers. If base image doesn't change, we never rebuild it.

### 2. Environment Variables = Configuration

No hardcoded passwords or database URLs in code:

```python
# Bad (hardcoded)
conn = psycopg2.connect("postgresql://user:pass@localhost/db")

# Good (configurable)
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    database=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD']
)
```

Docker Compose injects these automatically:

```yaml
environment:
  DB_HOST: database
  POSTGRES_DB: beers_db
  POSTGRES_USER: researcher
  POSTGRES_PASSWORD: c3demo2024
```

**Benefit:** Same code works in dev/staging/production, just different environment variables.

### 3. Service Dependencies

```yaml
depends_on:
  database:
    condition: service_healthy
```

This ensures:
- Database starts first
- Algorithm waits until database is fully ready
- No race conditions or connection errors

### 4. Volume Persistence

```yaml
volumes:
  - beer-data:/var/lib/postgresql/data
```

Database data persists between runs. Even if you `docker compose down`, the data stays.

**To start completely fresh:**
```bash
docker compose down -v  # The -v flag removes volumes
```

---

## Extending This Demo

### Add a New Algorithm

1. Create directory: `algorithm-my-analysis/`
2. Copy Dockerfile from existing algorithm
3. Write your `analyze.py` script
4. Add service to `docker-compose.yml`
5. Run: `docker compose up --build`

### Use a Different Dataset

1. Replace `dataset/beers.csv` with your data
2. Update `database/init.sql` to match new schema
3. Update algorithm SQL queries
4. Everything else stays the same!

### Add More Base Libraries

Edit `base-python/Dockerfile`:
```dockerfile
RUN pip install pandas psycopg2-binary numpy scipy scikit-learn
```

Rebuild base:
```bash
docker build -t base-python:latest ./base-python
```

All algorithms automatically get the new libraries.

---

## Common Questions

**Q: Why not just use conda/virtualenv?**

A: Virtual environments solve Python dependencies, but not:
- Database version differences
- System library differences
- "Works on Ubuntu but not Mac" issues
- Sharing entire analysis pipeline (not just Python code)

Containers package **everything** - Python, database, OS libraries, the works.

**Q: Isn't this overkill for a simple analysis?**

A: Setup cost is 5-10 minutes. Benefit lasts forever:
- 6 months from now: `docker compose up` still works
- New team member: `docker compose up` works on day 1
- Different laptop/OS: `docker compose up` works everywhere

**Q: What about performance?**

A: Docker has ~2-5% overhead. For research workloads (data analysis, not real-time systems), this is negligible compared to reproducibility benefits.

**Q: Can I run multiple algorithms in parallel?**

A: Yes! Uncomment all algorithm services in docker-compose.yml. They'll all connect to the same database and run simultaneously.

---

## Next Steps for C3 Research

This demo uses beer data for fun, but the pattern applies to real research:

1. **Replace dataset:** Your actual research data (CSV, JSON, whatever)
2. **Replace algorithms:** Your actual analysis scripts (Python, R, Julia, Go...)
3. **Same infrastructure:** Database, orchestration, environment management

The template stays the same. Only the data and algorithms change.

### Real-World C3 Example

```
c3-biodiversity-analysis/
├── docker-compose.yml           # Same pattern
├── base-r/                      # Base image with R instead of Python
│   └── Dockerfile
├── database/                    # PostgreSQL with species data
├── dataset/
│   └── species_observations.csv
└── algorithm-species-diversity/
    ├── Dockerfile               # FROM base-r:latest
    └── analyze.R                # Your actual research code
```

**Key insight:** Once you understand this pattern, you can containerize **any** research workflow.

---

## Troubleshooting

### Database won't start

```bash
# Check logs
docker compose logs database

# Common fix: remove old volume
docker compose down -v
docker compose up
```

### Algorithm can't connect to database

```bash
# Check if database is healthy
docker compose ps

# Should show:
# database  healthy
```

### Want to see inside the database

```bash
# Connect with psql
docker compose exec database psql -U researcher -d beers_db

# Run queries
beers_db=# SELECT beer_style, COUNT(*) FROM beers GROUP BY beer_style;
```

### Rebuild everything from scratch

```bash
# Nuclear option
docker compose down -v
docker system prune -a
docker build -t base-python:latest ./base-python
docker compose up --build
```

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Python Docker Image](https://hub.docker.com/_/python)

---

## License

MIT License - do whatever you want with this demo!

---

## Questions?

Contact: [Your contact info]

Built with 🍺 for C3-UNAM researchers by someone who's tired of "works on my machine" excuses.
