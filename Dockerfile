# Use official Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (leverages Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command
ENTRYPOINT ["python", "src/main.py"]
CMD ["--input", "input", "--persona", "persona.txt", "--job", "job.txt", "--model", "model", "--output", "output/result.json"]
