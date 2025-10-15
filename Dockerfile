FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-dev

COPY /app /app
COPY /requirements.txt /app/src/

RUN pip install --no-cache-dir -r /app/src/requirements.txt

RUN chmod -R 777 /app

EXPOSE 9001

CMD ["python", "/app/src/face_api.py", "--host", "0.0.0.0", "--port", "9001"]