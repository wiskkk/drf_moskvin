# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/innowise_tech_sup

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev rust cargo

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/innowise_tech_sup/entrypoint.sh
RUN chmod +x /usr/src/innowise_tech_sup/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/innowise_tech_sup/entrypoint.sh"]
