# my-flask-redis
# Flask View Counter App

This project demonstrates a simple Flask application that counts the number of views using Redis as the backend and Docker Compose for container orchestration.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/) installed.

## Project Structure

```
flask-view-counter/
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── Dockerfile # Dockerfile for the Flask app
├── docker-compose.yml # Docker Compose configuration
└── templates/
└── index.html # HTML template
└── README.md # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HassanAmohamed/flask-view-counter
   cd flask-view-counter
   ```

2. **Create a `requirements.txt` file**:
   ```plaintext
   Flask
   redis
   ```
   
3. **Create the `app.py` file**:
   ```python
   import time  # Import the time module for sleep functionality
   import redis  # Import the redis module for interacting with Redis
   from flask import Flask,  render_template   # Import the Flask class from the flask module

   # Initialize a Flask application
   app = Flask(__name__)

   # Create a Redis connection instance, connecting to the Redis server
   cache = redis.Redis(host='redis', port=6379)

   def get_hit_count():
    """Function to increment and return the hit count from Redis."""
    retries = 5  # Set the number of retries for connecting to Redis
    while retries > 0:  # Loop until retries are exhausted
        try:
            # Increment the 'hits' key in Redis and return the new value
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            # If a connection error occurs, decrement retries and wait before retrying
            retries -= 1
            time.sleep(0.5)  # Pause for half a second before retrying
            if retries == 0:  # If no retries are left, raise the exception
                raise exc

   @app.route('/')  # Define the route for the root URL
   def hello():
       """Handler function for the root URL that returns a greeting and hit count."""
       count = get_hit_count()  # Get the current hit count
       # Render the index.html template with the hit count
       return render_template('index.html', count=count)



   if __name__ == '__main__':
       # Run the Flask application on host 0.0.0.0 and port 5000
        app.run(host='0.0.0.0', port=5000)
   
   ```

4. **Create the `Dockerfile`**:
   ```Dockerfile
   # Use the official Python image
   FROM python:3.9

   # Set the working directory
   WORKDIR /app

   # Copy the requirements file
   COPY requirements.txt .

   # Install dependencies
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy the application code
   COPY app.py .

   # Expose the application port
   EXPOSE 5000

   # Start the Flask application
   CMD ["python", "app.py"]
   ```

5. **Create the `docker-compose.yml` file**:
   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       ports:
         - "5000:9000"
       depends_on:
         - redis

     redis:
       image: "redis:alpine"
   ```

## Usage

1. **Build and start the application**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   Open your web browser and go to `http://localhost:9000/`. Refresh the page to see the view count increment.

## Stopping the Application

To stop the application, you can use:
```bash
docker-compose down
```

This command will stop and remove the containers defined in the `docker-compose.yml` file.

