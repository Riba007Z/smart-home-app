# smart-home-app
react app for controlling 1home server instalations with voice controll


#start backend
$cd backend
$source venv/Source/activate
$uvicorn main:app --host 0.0.0.0


#start frontend
$cd frontend
$npm run dev -- --host 0.0.0.0
