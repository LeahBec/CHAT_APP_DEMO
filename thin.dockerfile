# set base image (host OS)
FROM python:3.8-slim as builder
RUN update-ca-certificates
# set the working directory in the container
WORKDIR /code
# copy the dependencies file to the working directory
COPY requirements.txt .
ENV FLASK_ENV development
ENV ROOMS_DIR='ROOMS'
# install dependencies
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
# copy the content of the local src directory to the working directory
FROM builder as run
ENV FLASK_ENV development
COPY . .
# command to run on container start
CMD [ "python", "./chatApp.py" ]