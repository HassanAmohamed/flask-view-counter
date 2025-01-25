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


