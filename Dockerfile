FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-dev

# Creates directory within your Docker image
RUN mkdir -p /app/src/
# Placeholder 
RUN mkdir -p /app/data/
RUN mkdir -p /app/model/

COPY /src /app/src/
COPY requirements.txt /app/src/
COPY /faces_optimized /faces_optimized

RUN pip install --no-cache-dir -r /app/src/requirements.txt

RUN chmod -R 777 /app

EXPOSE 9001

CMD ["python", "/app/src/face_api.py", "--host", "0.0.0.0", "--port", "9001"]