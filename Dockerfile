FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "face_api.py", "--host", "0.0.0.0", "--port", "8080"]