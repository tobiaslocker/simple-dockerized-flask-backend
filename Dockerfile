FROM gcr.io/google-appengine/python

RUN apt-get update && apt-get install -y build-essential

RUN virtualenv /env -p python3.7

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

EXPOSE 8080

CMD gunicorn -b :$PORT main:app --timeout 600 --log-level DEBUG
