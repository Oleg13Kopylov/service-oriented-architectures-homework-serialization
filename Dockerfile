FROM python:latest
WORKDIR /application
COPY . .
RUN ["pip", "install" , "--no-cache-dir", "-r", "requirements.txt"]