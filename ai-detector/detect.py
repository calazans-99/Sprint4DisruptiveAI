import os, sys, subprocess, time, csv
from datetime import datetime
import json
import cv2
import requests
from ultralytics import YOLO

def ensure(pkgs):
    for pkg in pkgs:
        pip_name = "opencv-python" if pkg == "cv2" else pkg
        try:
            __import__(pkg if pkg != "cv2" else "cv2")
        except Exception:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

if os.getenv("SELF_MANAGE_DEPS","0") == "1":
    ensure(["ultralytics", "cv2", "requests"])

MODEL_WEIGHTS = os.getenv("MODEL_WEIGHTS", "yolov8n.pt")
CONF_THRESH = float(os.getenv("CONF_THRESH", "0.5"))
CSV_PATH = os.getenv("CSV_PATH", "deteccoes.csv")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
SOURCE = os.getenv("SOURCE", "0") 

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure_csv(path):
    new = not os.path.exists(path)
    f = open(path, "a", newline="", encoding="utf-8")
    writer = csv.writer(f)
    if new:
        writer.writerow(["timestamp", "label", "conf", "x1", "y1", "x2", "y2", "cx", "cy", "evento"])
    return f, writer

def post_event(payload):
    try:
        r = requests.post(f"{BACKEND_URL}/events", json=payload, timeout=3)
        r.raise_for_status()
    except Exception as e:
        print(f"[WARN] Falha ao postar evento no backend: {e}")

model = YOLO(MODEL_WEIGHTS)

src = 0
if SOURCE.isdigit():
    src = int(SOURCE)
else:
    src = SOURCE

cap = cv2.VideoCapture(src)
if not cap.isOpened():
    print("Erro ao acessar a fonte de vídeo.")
    sys.exit(1)

csv_file, csv_writer = ensure_csv(CSV_PATH)
points = []

W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
GATE_X = W // 2

print("Detecção de motos em tempo real (pressione 'e' para sair)")
print(f"Backend: {BACKEND_URL} | CSV: {CSV_PATH} | CONF_THRESH: {CONF_THRESH}")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)[0]

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])

            if label.lower() in ["motorbike", "motorcycle"] and conf > CONF_THRESH:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                evento = "moto_esquerda" if cx < GATE_X else "moto_direita"

                row = {
                    "timestamp": now_str(),
                    "label": label,
                    "conf": round(conf, 2),
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "cx": cx, "cy": cy,
                    "evento": evento
                }

                csv_writer.writerow(list(row.values()))
                csv_file.flush()

                post_event(row)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 255), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 2)
                cv2.circle(frame, (cx, cy), 3, (0, 200, 255), -1)
                points.append((cx, cy))

        cv2.line(frame, (GATE_X, 0), (GATE_X, H), (255, 255, 255), 2)

        cv2.imshow("Deteccao de Motos", frame)
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    csv_file.close()
