# Security Recon Platform

**Distributed Full-Stack Security Reconnaissance System**

A scalable, event-driven web platform for automated network reconnaissance. This project came about as an extension of my other network recon application (Lazyfoot). This system performs asynchronous scanning, subdomain enumeration, and DNS analysis, while streaming real-time results to users via WebSockets.

---

## 🚀 Features

* **Network Scanning** — Service and port detection using Nmap
* **Subdomain Enumeration** — Automated discovery using Subfinder
* **DNS Analysis** — Resolution of A, MX, and NS records
* **Asynchronous Processing** — Distributed task execution with Celery + Redis
* **Real-Time Updates** — Live scan progress via WebSockets and Redis pub/sub
* **Persistent Storage** — PostgreSQL-backed scan results
* **RESTful API** — Built with FastAPI
* **Containerized Deployment** — Docker + Docker Compose

---

## Architecture

```
Frontend (React)
        ↓
FastAPI (API Layer)
        ↓
Redis (Broker + Pub/Sub)
        ↓
Celery Workers (Scan Engine)
        ↓
PostgreSQL (Persistent Storage)
```

### Key Design Principles

* **Decoupled services** for scalability and fault isolation
* **Event-driven communication** using Redis pub/sub
* **Asynchronous job execution** for long-running tasks
* **Modular scanning engine** for extensibility

---

## Tech Stack

**Frontend**

* React (JavaScript)

**Backend**

* FastAPI (Python)
* Celery (distributed task queue)
* Redis (message broker + pub/sub)
* PostgreSQL (database)

**Security Tooling**

* Nmap
* Subfinder
* dnspython

**Infrastructure**

* Docker
* Docker Compose

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/recon-platform.git
cd recon-platform
```

---

### 2. Run with Docker

```bash
docker-compose up --build
```

Services:

* API → http://localhost:8000
* PostgreSQL → localhost:5432
* Redis → localhost:6379

---

## API Usage

### Start a Scan

```bash
POST /scan?target=example.com
```

### Get Scan Result

```bash
GET /scan/{scan_id}
```

---

##  WebSocket Usage (Real-Time Updates)

Connect to:

```
ws://localhost:8000/ws/{scan_id}
```

### Example Events

```json
{"scan_id":1,"status":"running"}
{"scan_id":1,"status":"subdomains_done","data":[...]}
{"scan_id":1,"status":"dns_done","data":{...}}
{"scan_id":1,"status":"nmap_done","data":"..."}
{"scan_id":1,"status":"completed","data":{...}}
```

---

## System Design Highlights

* **Distributed Architecture**
  Separate API and worker services enable horizontal scaling and fault tolerance

* **Event-Driven Updates**
  Redis pub/sub allows real-time communication between workers and clients

* **Asynchronous Task Pipeline**
  Celery workers handle long-running scans without blocking API requests

* **Extensible Scanning Engine**
  Modular design allows easy integration of additional reconnaissance tools

---

## Future Improvements

* Authentication and multi-user support
* Structured result parsing and search capabilities
* Cloud deployment (AWS, GCP, or Fly.io)
* Web-based dashboard with advanced visualizations
* Integration with vulnerability scanning tools

---

## 📄 License

MIT License
