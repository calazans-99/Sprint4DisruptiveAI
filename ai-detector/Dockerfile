FROM ultralytics/ultralytics:8.3.67
WORKDIR /app
RUN pip install --no-cache-dir opencv-python requests
COPY detect.py .
ENV BACKEND_URL="http://localhost:8000" \
    CONF_THRESH="0.5" \
    CSV_PATH="/app/deteccoes.csv" \
    SOURCE="0"
CMD ["python", "detect.py"]
