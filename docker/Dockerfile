FROM python:3.10-slim

RUN pip install --upgrade pip
COPY requirements.txt /opt/build_todolist/requirements.txt
RUN pip install -r /opt/build_todolist/requirements.txt

COPY docker/entrypoint.sh /opt/build_todolist/entrypoint.sh

WORKDIR /opt/todolist

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PYTHON_PATH=/opt/todolist

RUN groupadd --system service && useradd --system -g service api

#RUN pip install --upgrade pip
#COPY requirements.txt /opt/todolist
#RUN pip install -r requirements.txt

#RUN pip install "poetry==1.1.13"
#COPY poetry.lock pyproject.toml ./
#RUN poetry config virtualenvs.create false \
#    && poetry install --no-dev --no-ansi --no-root

COPY todolist/ /opt/todolist
#COPY docker/entrypoint.sh ./entrypoint.sh
#COPY docker/entrypoint.sh /opt/todolist

USER api

ENTRYPOINT ["bash", "../build_todolist/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000