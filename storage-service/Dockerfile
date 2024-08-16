FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

COPY . /app

RUN pip install -e .

RUN mkdir -p /app/media

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 80

CMD ["gunicorn", "storage_service.wsgi:application", "--bind", "0.0.0.0:80"]
