FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r api/requirements.txt
RUN pip install --no-cache-dir \
    streamlit \
    requests \
    plotly \
    shap \
    watchdog

EXPOSE 8000
EXPOSE 8501