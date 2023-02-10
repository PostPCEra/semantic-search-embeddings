FROM python:latest
COPY main.py app/
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3", "main.py"]