@echo off
echo 🚀 Starting Restaurant List App with Expo...
echo.

echo ✅ Step 1: Installing dependencies...
call npm install

echo.
echo ✅ Step 2: Setting environment and starting Expo development server...
set NODE_ENV=development
echo.
echo 📱 Instructions:
echo   1. Make sure your Android Studio virtual device is running
echo   2. Press 'a' in the Expo CLI to run on Android
echo   3. Or scan the QR code with Expo Go app on your phone
echo.

call npx expo start

pause
