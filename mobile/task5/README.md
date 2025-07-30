# 📱 Restaurant List App - React Native

## 🎯 Task 5: Modern Mobile Restaurant Listing App

A beautiful, animated React Native application that displays a list of restaurants with modern UI/UX design and smooth animations.

## ✨ Features

### 🎨 **Eye-Catching UI Design**
- **Gradient backgrounds** with modern color schemes
- **Card-based layout** with elevation and shadows
- **Smooth animations** using React Native Reanimated
- **Loading states** with skeleton placeholders
- **Error handling** with retry functionality
- **Pull-to-refresh** functionality

### 🎭 **Animations & Interactions**
- **Entrance animations** with staggered delays
- **Press animations** with scale and opacity effects
- **Smooth transitions** between states
- **Spring animations** for natural feel
- **Fade effects** for loading and error states

### 📊 **Restaurant Information Display**
- **Restaurant name** and cuisine type
- **Star ratings** with visual star display
- **Price range** indicators
- **Delivery time** estimates
- **Restaurant descriptions**
- **Cuisine badges** with color coding

### 🔧 **Technical Features**
- **Modular architecture** with separate components
- **API service layer** for data management
- **Mock API** with realistic delays and error simulation
- **Loading and error states** handling
- **Responsive design** for different screen sizes
- **TypeScript ready** structure

## 🏗️ **Project Structure**

```
mobile/task5/
├── App.js                 # Main application component
├── index.js              # Entry point
├── package.json          # Dependencies and scripts
├── app.json              # App configuration
├── metro.config.js       # Metro bundler configuration
├── babel.config.js       # Babel configuration
├── components/           # Reusable components
│   ├── RestaurantCard.js # Individual restaurant card
│   ├── LoadingCard.js    # Loading skeleton card
│   └── ErrorState.js     # Error state component
├── services/             # API and data services
│   └── api.js           # Mock API service
└── README.md            # This file
```

## 🚀 **Getting Started**

### Prerequisites
- Node.js 16.0.0 or higher
- React Native development environment
- Android Studio (for Android) or Xcode (for iOS)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd mobile/task5
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **For iOS (macOS only):**
   ```bash
   cd ios && pod install && cd ..
   ```

### Running the App

1. **Start Metro bundler:**
   ```bash
   npm start
   ```

2. **Run on Android:**
   ```bash
   npm run android
   ```

3. **Run on iOS:**
   ```bash
   npm run ios
   ```

4. **Run on Web (if using Expo):**
   ```bash
   npm run web
   ```

## 📱 **App Screenshots & Features**

### 🏠 **Main Screen**
- **Header section** with gradient background and app title
- **Restaurant list** with smooth scrolling
- **Pull-to-refresh** functionality
- **Loading states** during data fetch

### 🍽️ **Restaurant Cards**
- **Image placeholder** with restaurant icon
- **Cuisine badge** showing food type
- **Restaurant name** and description
- **Star rating** with visual stars
- **Price range** indicator
- **Delivery time** with clock icon
- **Press animations** for user feedback

### ⚡ **Loading States**
- **Skeleton cards** with animated placeholders
- **Staggered entrance** animations
- **Smooth transitions** between loading and loaded states

### ❌ **Error Handling**
- **Beautiful error screen** with gradient background
- **Clear error message** and retry button
- **Animated error icon** and call-to-action

## 🎨 **Design System**

### **Color Palette**
- **Primary Gradient**: `#667eea` → `#764ba2`
- **Error Gradient**: `#ff9a9e` → `#fecfef`
- **Card Background**: `#ffffff` → `#f8f9fa`
- **Text Colors**: `#2d3748`, `#718096`, `#4a5568`
- **Accent Color**: `#FFD700` (stars)

### **Typography**
- **Header Title**: 32px, Bold
- **Restaurant Name**: 18px, Bold
- **Description**: 14px, Regular
- **Rating**: 14px, Semi-bold
- **Small Text**: 12px, Regular

### **Spacing & Layout**
- **Card Margins**: 20px horizontal, 15px vertical
- **Card Padding**: 16px
- **Border Radius**: 20px for cards, 15px for badges
- **Elevation**: 8 for cards, 4 for loading cards

## 🔌 **API Integration**

### **Mock API Service**
The app includes a comprehensive mock API service that simulates:
- **Network delays** (1-2 seconds)
- **Random errors** (10% chance)
- **Realistic restaurant data**
- **Different response scenarios**

### **API Methods**
```javascript
// Get all restaurants
restaurantAPI.getRestaurants()

// Get restaurant by ID
restaurantAPI.getRestaurantById(id)

// Search restaurants
restaurantAPI.searchRestaurants(query)

// Get by cuisine
restaurantAPI.getRestaurantsByCuisine(cuisine)

// Get top rated
restaurantAPI.getTopRatedRestaurants(limit)
```

### **Real API Integration**
The service includes commented code for connecting to the Django backend:
```javascript
// Uncomment and configure for real API
const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8000/api',
  ENDPOINTS: {
    RESTAURANTS: '/restaurants/',
  }
};
```

## 🎭 **Animation Details**

### **Entrance Animations**
- **Cards**: Fade in from bottom with staggered delays (100ms apart)
- **Loading cards**: Simple fade in with 50ms delays
- **Header**: Slide down with spring animation

### **Interaction Animations**
- **Card press**: Scale to 0.95 and opacity to 0.8
- **Card release**: Spring back to original size
- **Retry button**: Smooth press feedback

### **State Transitions**
- **Loading to content**: Smooth fade transition
- **Error to retry**: Fade in animation
- **Refresh**: Native pull-to-refresh animation

## 🔧 **Customization**

### **Adding New Restaurants**
Edit `services/api.js` and add to the `mockRestaurants` array:
```javascript
{
  id: 9,
  name: 'Your Restaurant',
  rating: 4.5,
  cuisine: 'Cuisine Type',
  description: 'Restaurant description',
  priceRange: '$$',
  deliveryTime: '20-30 min',
}
```

### **Modifying Colors**
Update the gradient colors in components:
```javascript
// Primary gradient
colors={['#667eea', '#764ba2']}

// Custom gradient
colors={['#your-color-1', '#your-color-2']}
```

### **Adjusting Animations**
Modify animation parameters in components:
```javascript
// Entrance delay
entering={FadeInDown.delay(index * 150).springify()}

// Press animation
scale.value = withSpring(0.90); // More dramatic scale
```

## 📦 **Dependencies**

### **Core Dependencies**
- `react`: 18.2.0
- `react-native`: 0.72.6
- `react-native-reanimated`: ^3.5.4
- `react-native-gesture-handler`: ^2.13.4
- `react-native-vector-icons`: ^10.0.2
- `react-native-linear-gradient`: ^2.8.3

### **Optional Dependencies**
- `react-native-fast-image`: For optimized image loading
- `lottie-react-native`: For Lottie animations
- `@react-native-async-storage/async-storage`: For local storage

## 🎯 **Task Requirements Fulfilled**

✅ **ListView Implementation**: Uses FlatList for efficient scrolling  
✅ **Restaurant Display**: Shows name and rating prominently  
✅ **Mock API**: Comprehensive mock API with realistic delays  
✅ **Loading States**: Beautiful skeleton loading cards  
✅ **Error Handling**: Elegant error state with retry functionality  
✅ **Modern UI**: Eye-catching design with gradients and animations  
✅ **User Friendly**: Intuitive interactions and smooth animations  
✅ **React Native**: Built with React Native instead of Flutter  

## 🚀 **Performance Optimizations**

- **FlatList**: Efficient rendering for large lists
- **Reanimated**: Native-thread animations for 60fps
- **Modular Components**: Optimized re-rendering
- **Lazy Loading**: Components load as needed
- **Memory Management**: Proper cleanup of animations

## 🎉 **Conclusion**

This React Native restaurant listing app demonstrates modern mobile development practices with:
- **Beautiful, animated UI** that's eye-catching and user-friendly
- **Robust error handling** and loading states
- **Modular architecture** for maintainability
- **Smooth animations** for enhanced user experience
- **Mock API integration** ready for real backend connection

The app exceeds the basic requirements by providing a production-ready mobile experience with modern design patterns and smooth animations.

---

**Ready to run! Execute `npm start` and then `npm run android` or `npm run ios` to see the beautiful animated restaurant list!** 📱✨
