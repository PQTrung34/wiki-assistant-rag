# Wiki RAG

1 Project nhỏ để tìm hiểu về RAG Pipeline

# Installation
## 1. Clone project
```bash
git clone https://github.com/PQTrung34/wiki-assistant-rag.git
cd wiki-assistant-rag
```

## 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate       # Đối với Linux/macOS
venv\Scripts\activate          # Đối với Windows
```

## 3. Cài đặt thư viện/dependencies
```bash
pip install -r requirements.txt
```

## 4. Chạy chương trình
```bash
uvicorn app.api.app:app --reload
```

Mặc định chương trình sẽ chạy tại: [localhost](http://localhost:8000)