FROM python:3.11-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app
# Copy project files
COPY pyproject.toml ./
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    curl \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy the source code and data directory into the container
COPY ./src /app/src
COPY ./data /app/data


# Install Python dependencies defined in pyproject.toml in editable mode (-e flag)
# Make sure your pyproject.toml correctly specifies your dependencies.
RUN pip install --no-cache-dir -e .


# Set the working directory to app/src
WORKDIR /app/src

# Expose ports
# Local development Streamlit default
EXPOSE 8501  
# Cloud Run expected port
EXPOSE 8080  

CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
# Command to run your Streamlit app
# --server.port takes the value from the $PORT environment variable (for cloud env like Cloud Run)
# --server.address=0.0.0.0 makes the app accessible from outside the container
# CMD ["streamlit", "run", "app.py", "--server.port", "$PORT", "--server.address", "0.0.0.0"]
