FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 5000
CMD gunicorn --bind :5000 --workers 2 --threads 8 'earthdaily:create_app()'

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
