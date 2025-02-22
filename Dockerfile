FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py"]