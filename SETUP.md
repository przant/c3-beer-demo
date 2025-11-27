# Setup Guide - C3 Beer Demo

Quick reference for running the demo locally or sharing with José Luis.

## Prerequisites Check

```bash
# Check Docker is installed
docker --version
# Expected: Docker version 20.x or higher

# Check Docker Compose is installed
docker compose version
# Expected: Docker Compose version v2.x or higher
```

If you don't have Docker installed: https://docs.docker.com/get-docker/

---

## First Time Setup

### 1. Clone or Download This Repository

```bash
# If pushing to GitHub first
git clone https://github.com/your-username/c3-beer-demo.git
cd c3-beer-demo

# Or if working locally
cd c3-beer-demo
```

### 2. Build the Base Image

This is the foundation that all algorithms will use:

```bash
docker build -t base-python:latest ./base-python
```

**What this does:**
- Downloads Python 3.11 slim image (~200 MB)
- Installs PostgreSQL client tools
- Installs pandas and psycopg2
- Creates reusable base (takes ~2-3 minutes first time)

**Output should end with:**
```
Successfully built [image-id]
Successfully tagged base-python:latest
```

### 3. Run the First Algorithm (Average ABV)

```bash
docker compose up
```

**What happens:**
1. Builds database image with PostgreSQL
2. Builds avg-abv algorithm image (inherits from base-python)
3. Starts database container
4. Loads beers.csv into database
5. Runs analysis
6. Shows results in terminal

**Expected output (abbreviated):**
```
database_1  | PostgreSQL init process complete
avg-abv_1   | Waiting for database...
avg-abv_1   | Database is ready!
avg-abv_1   | 
avg-abv_1   | ============================================================
avg-abv_1   | AVERAGE ABV BY BEER STYLE
avg-abv_1   | ============================================================
avg-abv_1   |      beer_style  avg_abv  beer_count
avg-abv_1   |     Barleywine    11.00           1
avg-abv_1   |  Imperial Stout    10.50           1
avg-abv_1   |          Tripel     9.00           1
avg-abv_1   | ...
avg-abv_1   | ✅ Analysis complete!
```

### 4. Cleanup

```bash
# Stop containers (keeps database data)
docker compose down

# Stop and remove everything including data
docker compose down -v
```

---

## Running Different Algorithms

### Switch to Top Breweries Analysis

1. Edit `docker-compose.yml`:

```yaml
# Comment out avg-abv service (add # at start of each line)
# avg-abv:
#   build: ./algorithm-avg-abv
#   ...

# Uncomment top-breweries service (remove # from lines)
top-breweries:
  build: ./algorithm-top-breweries
  ...
```

2. Run again:

```bash
docker compose up --build
```

The `--build` flag ensures Docker rebuilds with the new algorithm.

---

## Verification Checklist

✅ **Base image built successfully**
```bash
docker images | grep base-python
# Should show: base-python  latest  [id]  [time]  [size]
```

✅ **Containers running**
```bash
docker compose ps
# Should show database as "healthy"
```

✅ **Data loaded correctly**
```bash
docker compose exec database psql -U researcher -d beers_db -c "SELECT COUNT(*) FROM beers;"
# Should show: 60 rows
```

---

## Common Issues

### Issue: "Cannot connect to Docker daemon"

**Fix:**
```bash
# Start Docker Desktop (GUI)
# Or start Docker service (Linux)
sudo systemctl start docker
```

### Issue: "Port 5432 already in use"

**Cause:** You have PostgreSQL running locally

**Fix Option 1** (stop local PostgreSQL):
```bash
# Ubuntu/Debian
sudo systemctl stop postgresql

# macOS
brew services stop postgresql
```

**Fix Option 2** (change port in docker-compose.yml):
```yaml
ports:
  - "5433:5432"  # Use 5433 instead
```

### Issue: "base-python:latest not found"

**Fix:** Build the base image first:
```bash
docker build -t base-python:latest ./base-python
```

### Issue: Database initialization failed

**Fix:** Remove old data and start fresh:
```bash
docker compose down -v
docker compose up
```

---

## Demo Flow for José Luis

### Scenario 1: Show Layer Reuse

1. Build base image (show it takes ~2-3 minutes)
2. Build first algorithm (show it's fast - uses cached base)
3. Build second algorithm (show it's also fast - same cached base)

**Point:** We don't rebuild Python environment each time!

### Scenario 2: Show Algorithm Swapping

1. Run avg-abv analysis (show results)
2. Edit docker-compose.yml to switch algorithms
3. Run top-breweries analysis (show different results)
4. **Point:** Same infrastructure, different analysis - that's the template pattern!

### Scenario 3: Show Reproducibility

1. Run analysis, note results
2. `docker compose down -v` (destroy everything)
3. `docker compose up` (rebuild from scratch)
4. Results identical
5. **Point:** 6 months from now, same command, same results!

---

## Pushing to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - C3 beer containerization demo"

# Connect to GitHub repo
git remote add origin https://github.com/your-username/c3-beer-demo.git
git branch -M main
git push -u origin main
```

Then share the link with José Luis!

---

## Quick Commands Reference

```bash
# Build base image
docker build -t base-python:latest ./base-python

# Run demo
docker compose up

# Run with rebuild
docker compose up --build

# Stop (keep data)
docker compose down

# Stop and remove data
docker compose down -v

# See logs
docker compose logs

# See running containers
docker compose ps

# Connect to database
docker compose exec database psql -U researcher -d beers_db

# Rebuild everything from scratch
docker compose down -v
docker system prune -a  # Optional: clean all Docker cache
docker build -t base-python:latest ./base-python
docker compose up --build
```

---

## Next Steps After Demo

Once José Luis understands the pattern:

1. **Real dataset:** Replace beers.csv with actual research data
2. **Real algorithm:** Replace analyze.py with actual analysis code
3. **Different language:** Create base-r/ or base-julia/ for other languages
4. **Multiple algorithms:** Uncomment multiple services to run in parallel

The pattern stays the same - just swap the data and code!
