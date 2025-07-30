# 📱 Expo Setup Guide for Android Studio Virtual Device

## 🚀 Quick Setup

### Prerequisites
- **Node.js** (v16 or higher)
- **Android Studio** with virtual device configured
- **Expo CLI** installed globally

### 1. Install Expo CLI
```bash
npm install -g expo-cli
```

### 2. Install Project Dependencies
```bash
cd mobile/task5
npm install
```

### 3. Start Expo Development Server
```bash
# Option 1: Use the provided script (recommended)
.\start-android.bat
# or
.\start-android.ps1

# Option 2: Manual start
$env:NODE_ENV="development"; npx expo start
```

### 4. Run on Android Virtual Device

#### Option A: Using Expo CLI
1. Start your Android Studio virtual device
2. In the Expo CLI terminal, press `a` to run on Android
3. The app will automatically install and launch

#### Option B: Using Android Command
```bash
npm run android
# or
expo start --android
```

## 🔧 Android Studio Virtual Device Setup

### 1. Create Virtual Device
1. Open Android Studio
2. Go to **Tools** → **AVD Manager**
3. Click **Create Virtual Device**
4. Choose a device (e.g., Pixel 4)
5. Select Android API level (recommended: API 30+)
6. Click **Finish**

### 2. Start Virtual Device
1. In AVD Manager, click the **Play** button next to your device
2. Wait for the device to boot completely

### 3. Verify ADB Connection
```bash
adb devices
```
You should see your virtual device listed.

## 📦 Dependencies Included

### Core Expo Dependencies
- `expo` ~49.0.15
- `expo-status-bar` ~1.6.0
- `expo-linear-gradient` ~12.3.0

### React Native & Animation
- `react-native` 0.72.6
- `react-native-reanimated` ~3.3.0
- `react-native-gesture-handler` ~2.12.0
- `react-native-vector-icons` ^9.2.0

## 🎯 Features

### ✅ What Works
- **Beautiful animated restaurant list**
- **Smooth entrance animations**
- **Pull-to-refresh functionality**
- **Loading states with skeleton cards**
- **Error handling with retry**
- **Modern gradient UI design**
- **Cross-platform compatibility**

### 🎨 UI Components
- **RestaurantCard**: Animated cards with press feedback
- **LoadingCard**: Skeleton loading placeholders
- **ErrorState**: Beautiful error screen with retry
- **Mock API**: Realistic data with delays

## 🚀 Running Commands

### Development
```bash
# Start Expo development server
npm start

# Run on Android (with device/emulator running)
npm run android

# Run on iOS (macOS only)
npm run ios

# Run on web browser
npm run web
```

### Debugging
```bash
# Open developer menu in app
# Shake device or press Ctrl+M (Windows) / Cmd+D (Mac)

# View logs
expo logs
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "Expo CLI not found"
```bash
npm install -g expo-cli
```

#### 2. "No Android devices/emulators found"
- Start Android Studio virtual device
- Check `adb devices` shows your device
- Restart Expo development server

#### 3. "Metro bundler issues"
```bash
# Clear Metro cache
expo start -c
```

#### 4. "Dependencies not compatible"
```bash
# Clear node modules and reinstall
rm -rf node_modules
npm install
```

#### 5. "NODE_ENV=prod is invalid" Error
```bash
# Set correct NODE_ENV before starting
$env:NODE_ENV="development"; npx expo start

# Or use the provided scripts
.\start-android.bat
.\start-android.ps1
```

#### 6. "Cannot find module 'metro-core'" Error
```bash
# Install missing Metro dependencies
npm install metro metro-core metro-config metro-resolver --save-dev

# Then restart
npm install
$env:NODE_ENV="development"; npx expo start
```

#### 7. "Cannot find module '@react-native/metro-config'" Error
```bash
# Update metro.config.js to use Expo metro config
# Replace the import with:
# const { getDefaultConfig } = require('expo/metro-config');
# const config = getDefaultConfig(__dirname);
# module.exports = config;
```

#### 8. Web Dependencies Missing Error
```bash
# If you see: "It looks like you're trying to use web support but don't have the required dependencies"
# Install web dependencies:
npx expo install react-native-web@~0.19.6 react-dom@18.2.0

# Fix all dependency versions:
npx expo install --fix

# Install additional Expo utilities:
npx expo install expo-font expo-constants
```

### Android Studio Issues

#### 1. Virtual Device Won't Start
- Ensure virtualization is enabled in BIOS
- Allocate sufficient RAM to virtual device
- Use x86_64 system images for better performance

#### 2. ADB Not Working
```bash
# Restart ADB server
adb kill-server
adb start-server
```

## 📱 App Features

### Restaurant List
- **8 diverse restaurants** with different cuisines
- **Star ratings** with visual representation
- **Price indicators** ($, $$, $$$, $$$$)
- **Cuisine badges** for easy categorization
- **Estimated delivery times**

### Animations
- **Staggered entrance** animations (100ms delays)
- **Press feedback** with scale and opacity
- **Spring animations** for natural feel
- **Smooth transitions** between states

### User Experience
- **Pull-to-refresh** to reload data
- **Loading states** with skeleton cards
- **Error handling** with retry button
- **Responsive design** for all screen sizes

## 🎉 Success!

Once everything is set up, you should see:
1. **Expo development server** running in terminal
2. **QR code** for easy device connection
3. **Restaurant app** launching on your virtual device
4. **Beautiful animated list** of restaurants

The app demonstrates modern React Native development with:
- ✅ Expo managed workflow
- ✅ Beautiful UI/UX design
- ✅ Smooth animations
- ✅ Production-ready code
- ✅ Cross-platform compatibility

## 📞 Need Help?

If you encounter any issues:
1. Check the **troubleshooting section** above
2. Ensure all **prerequisites** are installed
3. Verify **Android virtual device** is running
4. Check **Expo CLI** is properly installed

**Happy coding!** 🚀📱✨
