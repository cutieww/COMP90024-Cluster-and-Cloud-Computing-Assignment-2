FROM python:3.11.3-alpine3.17

# Set the working directory
WORKDIR /app

# Copy the contents of the current directory to the container
COPY . /app

# Install bash and the required packages
RUN pip install -r requirements.txt

#RUN . ./secrets.sh
# Run the secrets.sh script and then main.py when the container starts
CMD ["python", "main.py"]