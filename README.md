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

## Run with docker

```bash
install:
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
docker --version
docker compose version
git clone https://github.com/Riba007Z/smart-home-app.git
cd smart-home-app
cd backend

sudo apt update
sudo apt install mkcert -y
mkcert -install
mkcert <DEVICE_IP>

change frontend/src/config.js ip to device_ip
change extra_hosts ip to 1home ip
change docker_compose.yml ips to device_ip
docker compose build
docker compose up

rebuild after changes
docker compose down
docker compose build
docker compose up -d
```
