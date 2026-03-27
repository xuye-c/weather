# Weather Backend Service

A mini backend project from [PM Accelerator](https://www.linkedin.com/school/pmaccelerator/)

结结巴巴的中文demo视频: [demo](https://drive.google.com/file/d/1r-JeD-clMWV4OyrwKsteyqZOtqeJ64QS/view?usp=sharing)

---

## Overview

This project is a lightweight weather backend service built with Flask. It supports:

- Storing weather data (CRUD operations)
- Fetching real-time weather using OpenWeather API
- Exporting data into multiple formats
- Multi-language response messages (English / Chinese)

The system is designed with a modular architecture to separate concerns such as input handling, database operations, and external API integration.

---

## Project Structure
```plaintext
weather_app/
|-- configs/        # Configuration & message handling
|-- controller/     # Input validation & request routing
|-- db/             # Database layer (CRUD)
|-- service/        # API + business logic
|   |-- export/     # Export system (strategy pattern)
|-- run.py          # Flask entry point
```

### Key Components

- **InputManager**
  - Validates user input
  - Routes requests to backend logic

- **DB Layer**
  - `reader.py`: read operations
  - `writer.py`: write operations
  - `dbManager.py`: database connection

- **Weather API**
  - Fetches real-time weather from OpenWeather

- **Exporter System**
  - Uses abstract base class + concrete exporters
  - Supports extensible export formats

---

## ⚙️ Setup & Run

### 1. Install dependencies

```bash
pip install -r doc/requirements.txt

```
### 2. Run the server
```bash
python weather_app/run.py

```
## Run Tests

Make scripts executable:
```bash
chmod +x scripts/test_*.sh
```
Run all tests:
```bash
./scripts/test_all.sh
```

Run specific test:
```bash
./scripts/test_[task_name].sh
```

## API Usage
Insert / Update Data
```bash
curl -X POST http://127.0.0.1:5000/api/insert \
  -d "city=Beijing" \
  -d "date=2024-01-01" \
  -d "temperature=25"
```
Query Data
```bash
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=Beijing"
```
With date range:
```bash
curl -X POST http://127.0.0.1:5000/api/search \
  -d "city=Beijing"\
  -d "start_date=2024-01-01" \
  -d "end_date=2024-01-10"
```
Delete Data
```bash
curl -X POST http://127.0.0.1:5000/api/delete \
  -d "city=Beijing" \
  -d "date=2024-01-01"
```
Get Real-Time Weather
```bash
curl -X POST http://127.0.0.1:5000/api/weather \
  -d "city=Beijing"
```
Get Google Maps Link

```bash
# GET request (city in URL)
curl -X GET "http://127.0.0.1:5000/api/map/Beijing"

# POST request (city in form data)
curl -X POST http://127.0.0.1:5000/api/map \
  -d "city=Shanghai"

```

Export Data

Export specific city:
```bash
curl -X GET "http://127.0.0.1:5000/api/export/json?city=Beijing"
```
Export all data:
```bash
curl -X GET "http://127.0.0.1:5000/api/export/json"
```
Check supported formats:
```bash
curl -X GET "http://127.0.0.1:5000/api/export/formats"
```
Set Language
```bash
curl -X POST http://127.0.0.1:5000/api/set_language \
  -H "Content-Type: application/json" \
  -d '{"lang": "zh"}'
```
## Design Highlights
* Layered architecture (Controller / Service / DB)
* Strategy pattern for export system
* Separation of concerns for scalability
* Avoidance of hard-coded strings via message manager