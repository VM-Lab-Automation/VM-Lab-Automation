FROM python:3.6

WORKDIR /app
COPY . .
RUN python setup.py install

ENV FLASK_APP="service_interface"
ENV FLASK_ENV=development

RUN python setup_db.py

ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=8080"]
