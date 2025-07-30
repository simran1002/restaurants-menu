Write-Host "🚀 Starting Restaurant List App with Expo..." -ForegroundColor Green
Write-Host ""

Write-Host "✅ Step 1: Installing dependencies..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "✅ Step 2: Setting environment and starting Expo development server..." -ForegroundColor Yellow
$env:NODE_ENV = "development"
Write-Host ""
Write-Host "📱 Instructions:" -ForegroundColor Cyan
Write-Host "  1. Make sure your Android Studio virtual device is running" -ForegroundColor White
Write-Host "  2. Press 'a' in the Expo CLI to run on Android" -ForegroundColor White
Write-Host "  3. Or scan the QR code with Expo Go app on your phone" -ForegroundColor White
Write-Host ""

npx expo start

Read-Host "Press Enter to continue..."
