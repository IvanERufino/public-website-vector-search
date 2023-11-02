FROM python:3.9
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN mkdir -p /code
WORKDIR /code
COPY . /code/

ENV PROJECT_ID "your-project-id"
ENV REGION "your-region"

EXPOSE 8080
ENTRYPOINT ["gunicorn", "main:app", "--workers=4", "--worker-class=uvicorn.workers.UvicornWorker", "--timeout=36000","--bind=0.0.0.0:8080"]