# Use Python 3.8
FROM python:3.8

# Set working directory inside the container
WORKDIR /app


# Copy only requirements first (for caching layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files (but we will override them with volume mounting)
COPY . .

# Expose Flask's default port
EXPOSE 5000

# Start Flask in development mode with auto-reload
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debugger"]
