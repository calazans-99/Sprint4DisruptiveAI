# Sprint 4 – IA (Visão Computacional) – Mottu

Marcus Vinicius de Souza Calazans — RM556620
Lucas Abud Berbel — RM557957

Este repositório implementa o **fluxo completo** para a sprint 4 de **Disruptive Architectures (IoT/IOB & Generative IA)** baseado no seu script YOLO: captura → detecção → **persistência em backend** → **dashboard**.

## Componentes

- **ai-detector/**: detector com YOLOv8 (Ultralytics) que grava CSV e envia eventos para o backend via HTTP.
- **backend/**: API FastAPI + SQLite (endpoints `/health`, `/events`, `/stats`).
- **dashboard/**: Streamlit com métricas e gráfico de dispersão dos pontos (cx, cy).
- **simulator/**: gerador de eventos sintéticos para testes sem câmera.

## Rodando local com Docker Compose

```bash
docker compose up -d --build
# dashboard: http://localhost:8501
# backend:   http://localhost:8000/health
```

> **Detector com câmera** não sobe bem em cloud PaaS; rode localmente apontando o `BACKEND_URL` para o backend publicado, ou use `simulator/generate_events.py` para efeitos de demo.

### Detector local (Python puro)

```bash
cd ai-detector
python -m pip install -r requirements.txt
set BACKEND_URL=http://localhost:8000  # PowerShell (Windows) | export BACKEND_URL=...
python detect.py
```

### Simulador de eventos

```bash
cd simulator
python generate_events.py
```

## Endpoints do Backend

- `GET /health` – health check
- `POST /events` – cria evento (payload: timestamp,label,conf,x1,y1,x2,y2,cx,cy,evento)
- `GET /events?limit=100` – lista recentes
- `GET /stats` – totais (esquerda/direita, por label)

## Azure DevOps (Sprint 4 – DevOps)

- **CI**: build e testes (se aplicável) e publicar artefato (imagens Docker).
- **CD**: deploy de **backend** e **dashboard** em **Azure Web App for Containers** ou **ACI**, usando imagens do **ACR**.
- O detector pode ser rodado localmente (ou em VM/Edge) apontando para o backend publicado.

## Observações de Entrega (conforme PDF oficial da Sprint 4)

- Entregar **PDF com links** (GitHub, YouTube, Azure DevOps).
- **Pipelines CI/CD** conectadas ao GitHub e gerando artefatos/deploy.
- **Banco em Nuvem** válido (aqui usamos SQLite para simplicidade; substitua por Azure SQL/PostgreSQL se desejar).
- **Vídeo** demonstrando push → pipeline → deploy → dashboard → CRUD/consulta no banco (via endpoints).

Boa Sprint! 🚀
