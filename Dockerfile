FROM python:3.11-slim-bullseye

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC Driver 18 (stable for Debian 11)
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# App directory
WORKDIR /app

# Copy project
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

# Expose Render port
EXPOSE 10000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]