# Start from python:3.8-alpine base image
FROM python:3.8-alpine

# Adding git, bash and openssh to the image
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

# Make dir app
RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/

RUN pip install -r requirements.txt

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Expose port 8080 to the outside world
EXPOSE 5000

# Run the executable
CMD ["python", "app.py"]