# pull official base image
FROM python:3.11.3-alpine3.17

# set working directory
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "main.py"]
