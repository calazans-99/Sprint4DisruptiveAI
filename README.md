# 🧠 Sprint 4 – Disruptive Architectures: IA e Visão Computacional

## 🎯 Tema: Detecção de Motos com YOLOv8 e Análise em Tempo Real

Projeto desenvolvido para a **Sprint 4** da FIAP – disciplina **Disruptive Architectures (IA, IoT & Edge Computing)**, integrando **Visão Computacional**, **Backend Inteligente** e **Dashboard Analítico**.

---

## 👥 Integrantes

| Nome                        | RM      | Turma   |
|-----------------------------|----------|----------|
| **Marcus Vinicius de Souza Calazans** | 556620 | 2TDS-PH |
| **Lucas Abud Berbel**              | 557957 | 2TDS-PH |

---

## 🔗 Links de Entrega

- 📘 **GitHub (código completo):** [https://github.com/calazans-99/Sprint4DisruptiveAI](https://github.com/calazans-99/Sprint4DisruptiveAI)
- 🎥 **Vídeo de Apresentação (YouTube):** [https://youtu.be/NivIaqoZQ0c](https://youtu.be/NivIaqoZQ0c)
- ⚙️ **Pipeline CI/CD (Azure DevOps):** *link para pipeline do grupo*
- ☁️ **Aplicação publicada (Azure Web App):** *URL do backend e dashboard publicados*

---

## 🧩 Descrição da Solução

O sistema realiza **detecção em tempo real de motos** utilizando o modelo **YOLOv8 (Ultralytics)** conectado a uma **API Backend FastAPI**, que armazena eventos detectados e expõe endpoints REST para consulta.  
Um **dashboard em Streamlit** exibe estatísticas e visualizações, permitindo acompanhar o fluxo de veículos de forma clara e interativa.

### Fluxo de funcionamento

1. **Captura de vídeo** via webcam ou stream;
2. **YOLOv8** detecta objetos do tipo *motorbike* ou *motorcycle*;
3. Cada detecção gera um **evento JSON** com coordenadas e nível de confiança;
4. O evento é enviado ao **backend FastAPI**, que grava os dados no banco (SQLite/Azure SQL);
5. O **dashboard Streamlit** consome os endpoints e apresenta gráficos e métricas em tempo real.

---

## 🏗️ Arquitetura do Sistema

```text
📦 Sprint4DisruptiveAI
├── ai-detector/          # YOLOv8 + OpenCV – captura e detecção de motos
├── backend/              # FastAPI + SQLite (API REST)
├── dashboard/            # Streamlit – dashboard analítico
├── simulator/            # Gera eventos sintéticos para testes
├── docker-compose.yml    # Orquestra backend + dashboard
└── README.md
```

---

## 🧠 Tecnologias Utilizadas

| Categoria          | Tecnologias |
|--------------------|-------------|
| **IA/Detecção**    | Python, YOLOv8 (Ultralytics), OpenCV |
| **Backend**        | FastAPI, SQLite, SQLAlchemy |
| **Dashboard**      | Streamlit, Matplotlib, Pandas |
| **DevOps**         | Docker, Azure App Service, Azure DevOps (CI/CD) |
| **Infraestrutura** | Azure Container Registry, Web App for Containers |

---

## ⚙️ Backend API (FastAPI)

### Endpoints principais
| Método | Endpoint | Descrição |
|---------|-----------|-----------|
| `GET` | `/health` | Health check |
| `POST` | `/events` | Cria evento de detecção |
| `GET` | `/events` | Lista eventos recentes |
| `GET` | `/stats` | Estatísticas (totais, esquerda/direita, por label) |

---

## 📊 Dashboard (Streamlit)

O painel apresenta:
- **Status do backend**
- **Métricas gerais:** total de detecções, motos à esquerda/direita
- **Tabela de eventos recentes**
- **Gráfico de dispersão (cx, cy)** com linha de “gate” (divisória do frame)

---

## 🤖 Detector (YOLOv8)

O script `detect.py` usa **Ultralytics YOLOv8n** para detecção local via webcam ou arquivo.

```bash
cd ai-detector
pip install -r requirements.txt
python detect.py
```

> Para rodar sem câmera, utilize o simulador de eventos (`simulator/generate_events.py`).

---

## 🧪 Testes Locais com Docker Compose

```bash
docker compose up -d --build
```

- Backend: http://localhost:8000  
- Dashboard: http://localhost:8501  
- Detector (opcional, rodar localmente com acesso à câmera)

---

## ☁️ Deploy em Nuvem (Azure)

1. **Build e push das imagens** para o Azure Container Registry (ACR)
2. **Deploy automático** via pipeline YAML no Azure DevOps
3. **Backend e Dashboard** publicados em Web App for Containers
4. **Detector** rodando localmente ou em edge device, apontando para o backend da nuvem

---

## 🧾 Requisitos Atendidos (PDF Oficial FIAP)

| Requisito | Implementação |
|------------|----------------|
| 0️⃣ PDF com links e dados | Este README + PDF de entrega |
| 1️⃣ Descrição da solução | Seção completa acima |
| 2️⃣ Diagrama | Apresentado no relatório PDF |
| 3️⃣ Detalhamento dos componentes | Descrito por módulos (IA, Backend, Dashboard, CI/CD) |
| 💾 Banco em Nuvem | Pode usar Azure SQL, PostgreSQL ou SQLite (para demo) |
| ☁️ Deploy em Azure | Backend + Dashboard publicados via Azure DevOps |
| 🎥 Vídeo da Sprint | Demonstra push → pipeline → deploy → dashboard funcionando |

---

## 🧬 Diagrama da Arquitetura

```text
 ┌───────────────┐
 │   Webcam / RTSP│
 └───────┬────────┘
         │ Frames
         ▼
 ┌────────────────────────┐
 │  YOLOv8 Detector (AI)  │
 │ detect.py              │
 └────────┬───────────────┘
          │ Eventos JSON
          ▼
 ┌────────────────────────┐
 │ Backend (FastAPI)      │
 │ /events /stats /health │
 └────────┬───────────────┘
          │ API REST
          ▼
 ┌────────────────────────┐
 │ Dashboard (Streamlit)  │
 │ Visualização e Métricas│
 └────────────────────────┘
```

---

## 🏁 Conclusão

O projeto demonstra a aplicação prática de **Visão Computacional** integrada a **arquitetura em nuvem e pipelines DevOps**, seguindo os pilares de **Disruptive Architectures**:

- Automação ponta a ponta (IA + Backend + Front + Cloud);
- Modularidade e reusabilidade via containers;
- Monitoramento e análise de dados em tempo real.

---

**FIAP – 2TDS-PH**  
_Disruptive Architectures – Sprint 4 (2025 – 2º semestre)_  
🚀 *Marcus Calazans* | *Lucas Abud Berbel*
