FROM python:3.10

WORKDIR code


COPY Makefile pyproject.toml poetry.lock ./
RUN make setup-poetry

ENV PATH=/root/.local/bin:${PATH}
ENV POETRY_VIRTUALENVS_CREATE=false
RUN make install

COPY . .

EXPOSE 8080

ENTRYPOINT ["bash", "entrypoint.sh"]
