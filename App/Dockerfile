FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirement file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY App/ ./App/
COPY run.py .

# Expose port
EXPOSE 5000

# Command to run the app
CMD ["python", "App/run.py"]

