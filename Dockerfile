FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY ./app /app/app
COPY ./.env /app/.env

# Expose the port that the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]