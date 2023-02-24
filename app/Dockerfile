# start by pulling the python image
FROM python:3.11.0-bullseye

ENV PYTHONUNBUFFERED True

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

EXPOSE 8080

# configure the container to run in an executed manner

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app
