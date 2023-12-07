FROM python:3.9

WORKDIR code

COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
COPY entrypoint.sh entrypoint.sh

RUN pip install -r requirements.txt

COPY app app

EXPOSE 8080

ENTRYPOINT ["bash", "entrypoint.sh"]
