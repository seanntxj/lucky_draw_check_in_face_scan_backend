FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-dev

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/.deepface && chmod -R 755 /app

EXPOSE 9001

CMD ["python", "/app/src/face_api.py", "--host", "0.0.0.0", "--port", "9001"]