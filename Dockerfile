FROM python:3.7-alpine

# Set the working directory
WORKDIR /app

# Set environment variables without spaces around the equals sign
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install build dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

# Copy requirements file and install dependencies
COPY  requirements.txt  requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["flask", "run"]
