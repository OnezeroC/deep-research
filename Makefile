.PHONY: install install-backend install-frontend dev-backend dev-frontend dev build test clean

install: install-backend install-frontend

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload

dev-frontend:
	cd frontend && npm run dev

dev:
	@echo "Start both in separate terminals:"
	@echo "  Terminal 1: make dev-backend"
	@echo "  Terminal 2: make dev-frontend"

build:
	cd frontend && npm run build

test:
	cd backend && python -m pytest tests/ -v

clean:
	rm -rf backend/data
	rm -rf frontend/dist
