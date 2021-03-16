FROM python:3.9

ENV DockerHOME=/usr/src/app
WORKDIR $DockerHOME  

RUN pip install pipenv

COPY Pipfile ./
RUN pipenv install

COPY . $DockerHOME  

EXPOSE 8000

CMD [ "pipenv", "run",  "python", "manage.py", "runserver", "0.0.0.0:8000" ]