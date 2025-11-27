FROM base-python:latest

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the analysis script
COPY analyze.py .

# Run the analysis when container starts
CMD ["python", "analyze.py"]
