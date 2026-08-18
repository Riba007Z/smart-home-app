# smart-home-app

react app for controlling 1home server instalations with voice controll

#start backend
$cd backend
<<<<<<< HEAD
$source venv/Source/activate
$uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile 192.168.64.110-key.pem --ssl-certfile 192.168.64.110.pem
=======
$source venv/Scripts/activate
$uvicorn main:app --host 0.0.0.0

>>>>>>> a2f161640cf19b3867fa7a2cf1a8eac4fc07c310

#start frontend
$cd frontend
$npm run dev -- --host 0.0.0.0
