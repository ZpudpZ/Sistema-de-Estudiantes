FROM amancevice/pandas:2.1.4-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    grep -vE "pandas|numpy|pyarrow" requirements.txt > req_light.txt && \
    pip install --no-cache-dir -r req_light.txt

COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]