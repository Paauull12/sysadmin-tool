FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install -e .

EXPOSE 80

CMD ["gunicorn", "display_service.wsgi:application", "--bind", "0.0.0.0:5000"]
