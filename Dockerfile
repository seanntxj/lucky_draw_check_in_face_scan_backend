FROM python:3.11

RUN apt-get update && apt-get install -y libgl1-mesa-dev

# Creates directory within your Docker image
RUN mkdir -p /app/src/
# Placeholder 
RUN mkdir -p /app/data/
RUN mkdir -p /app/model/

COPY . /app/src/

RUN pip install --no-cache-dir -r /app/src/requirements.txt

RUN chgrp -R 65534 /app && \
    chmod -R 777 /app

EXPOSE 8080

CMD ["python", "face_api.py", "--host", "0.0.0.0", "--port", "8080"]