.PHONY: dev backend frontend test docker-up docker-down install

dev: docker-up

backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && python -m pytest app/tests/ -v

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

setup:
	cp backend/.env.example backend/.env
	cp frontend/.env.example frontend/.env
