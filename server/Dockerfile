FROM python:3
ARG project_dir=/app/

RUN apt-get update
RUN pip install --upgrade pip

WORKDIR $project_dir

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY config ./config
COPY ibm-credentials.env ./
COPY static ./static
COPY app.py ./

ENV IBM_CREDENTIALS_FILE /app/ibm-credentials.env   
CMD ["python", "app.py"]





