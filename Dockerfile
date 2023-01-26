FROM python:3.10.6-buster

WORKDIR /workdir

RUN pip install fastapi uvicorn

COPY service service

CMD ["uvicorn", "service.app:app", "--host=0.0.0.0", "--port=5000"]
