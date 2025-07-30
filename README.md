# Venturessky Full Stack Developer Test

Complete implementation of all tasks for the Venturessky Full Stack Developer coding test.

## Project Structure

```
vsky_fullstack_exam/
├── backend/           # Section 1: Django REST API (Tasks 1-2)
├── frontend/          # Section 2: React Components (Tasks 3-4)
├── mobile/           # Section 3: React Native App (Task 5)
├── database/         # Section 4: PostgreSQL Queries
└── protocols/        # Section 5: MQTT, gRPC, Redis (Tasks 7-9)
```

## How to Run

### Backend (Tasks 1-2)

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API available at: <http://127.0.0.1:8000/api/restaurants/>

### Frontend (Tasks 3-4)

```bash
# Task 3 - Restaurant List
cd frontend/task3
npm install
npm start

# Task 4 - Restaurant Form
cd frontend/task4
npm install
npm start
```

### Mobile (Task 5)

```bash
cd mobile
npm install
npx expo start
```

### Database (Task 6)

SQL query located in: `database/query.txt`

### Protocols (Tasks 7-9)

```bash
cd protocols
pip install -r requirements.txt

# Task 7 - MQTT
python task7/mqtt.py

# Task 8 - gRPC
python task8/grpc.py

# Task 9 - Redis
python task9/redis.py
```

## Task Status

✅ All tasks completed successfully

- **Section 1**: Django API with Restaurant model and data processing
- **Section 2**: React components with hooks and form handling
- **Section 3**: React Native mobile app with restaurant list
- **Section 4**: Optimized PostgreSQL query for top restaurants
- **Section 5**: MQTT, gRPC, and Redis implementations

## Testing

Use the included `postman_collection.json` to test all API endpoints.
