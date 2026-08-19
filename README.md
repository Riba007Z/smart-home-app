# smart-home-app

React app for controlling 1Home server installations with voice control.

## Start backend

```bash
cd backend
source venv/Source/activate
py -m pip install -r requirements
uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile 192.168.64.110-key.pem --ssl-certfile 192.168.64.110.pem
```

## Start frontend

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```
