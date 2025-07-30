// Real API service connecting to Django backend
// Updated to use the actual Django REST API

const mockRestaurants = [
  {
    id: 1,
    name: 'The Golden Spoon',
    rating: 4.8,
    cuisine: 'Italian',
    image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400',
    description: 'Authentic Italian cuisine with a modern twist',
    priceRange: '$$$',
    deliveryTime: '25-35 min',
  },
  {
    id: 2,
    name: 'Sakura Sushi',
    rating: 4.6,
    cuisine: 'Japanese',
    image: 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400',
    description: 'Fresh sushi and traditional Japanese dishes',
    priceRange: '$$$$',
    deliveryTime: '30-40 min',
  },
  {
    id: 3,
    name: 'Burger Haven',
    rating: 4.4,
    cuisine: 'American',
    image: 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400',
    description: 'Gourmet burgers and craft beer',
    priceRange: '$$',
    deliveryTime: '15-25 min',
  },
  {
    id: 4,
    name: 'Spice Garden',
    rating: 4.7,
    cuisine: 'Indian',
    image: 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400',
    description: 'Aromatic spices and traditional Indian flavors',
    priceRange: '$$',
    deliveryTime: '20-30 min',
  },
  {
    id: 5,
    name: 'Le Petit Bistro',
    rating: 4.9,
    cuisine: 'French',
    image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400',
    description: 'Elegant French dining experience',
    priceRange: '$$$$',
    deliveryTime: '35-45 min',
  },
  {
    id: 6,
    name: 'Taco Fiesta',
    rating: 4.3,
    cuisine: 'Mexican',
    image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400',
    description: 'Vibrant Mexican street food',
    priceRange: '$',
    deliveryTime: '10-20 min',
  },
  {
    id: 7,
    name: 'Dragon Palace',
    rating: 4.5,
    cuisine: 'Chinese',
    image: 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=400',
    description: 'Traditional Chinese dishes with modern presentation',
    priceRange: '$$',
    deliveryTime: '20-30 min',
  },
  {
    id: 8,
    name: 'Mediterranean Breeze',
    rating: 4.6,
    cuisine: 'Mediterranean',
    image: 'https://images.unsplash.com/photo-1544148103-0773bf10d330?w=400',
    description: 'Fresh Mediterranean flavors and healthy options',
    priceRange: '$$$',
    deliveryTime: '25-35 min',
  },
];

// Helper functions for data transformation
const getCuisineType = (restaurantName) => {
  const name = restaurantName.toLowerCase();
  if (name.includes('pizza') || name.includes('italian')) return 'Italian';
  if (name.includes('sushi') || name.includes('japanese')) return 'Japanese';
  if (name.includes('burger') || name.includes('american')) return 'American';
  if (name.includes('spice') || name.includes('indian') || name.includes('curry')) return 'Indian';
  if (name.includes('bistro') || name.includes('french')) return 'French';
  if (name.includes('taco') || name.includes('mexican')) return 'Mexican';
  if (name.includes('dragon') || name.includes('chinese')) return 'Chinese';
  if (name.includes('mediterranean')) return 'Mediterranean';
  return 'International';
};

const getRestaurantImage = (restaurantName) => {
  const cuisine = getCuisineType(restaurantName);
  const imageMap = {
    'Italian': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop',
    'Japanese': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop',
    'American': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=300&fit=crop',
    'Indian': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop',
    'French': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&h=300&fit=crop',
    'Mexican': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop',
    'Chinese': 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=400&h=300&fit=crop',
    'Mediterranean': 'https://images.unsplash.com/photo-1544148103-0773bf10d330?w=400&h=300&fit=crop',
  };
  return imageMap[cuisine] || 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop';
};

const getPriceRange = (rating) => {
  if (rating >= 4.7) return '$$$$';
  if (rating >= 4.3) return '$$$';
  if (rating >= 4.0) return '$$';
  return '$';
};

const getDeliveryTime = () => {
  const times = ['15-25 min', '20-30 min', '25-35 min', '30-40 min', '35-45 min'];
  return times[Math.floor(Math.random() * times.length)];
};

// Simulate API delay and potential errors
const simulateNetworkDelay = (min = 1000, max = 2000) => {
  const delay = Math.random() * (max - min) + min;
  return new Promise(resolve => setTimeout(resolve, delay));
};

// Real API functions connecting to Django backend
export const restaurantAPI = {
  // Fetch all restaurants from Django API
  getRestaurants: async () => {
    const apiUrl = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.RESTAURANTS}`;
    console.log('🔄 Attempting to fetch restaurants from:', apiUrl);
    
    try {
      // Create a timeout promise
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Connection timeout - Django server may not be running')), API_CONFIG.TIMEOUT)
      );
      
      // Create the fetch promise with additional headers for mobile
      const fetchPromise = fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Cache-Control': 'no-cache',
          'User-Agent': 'ExpoApp/1.0',
        },
      });
      
      // Race between fetch and timeout
      const response = await Promise.race([fetchPromise, timeoutPromise]);
      console.log('📡 Response status:', response.status, response.statusText);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('📊 Raw Django API data:', data.length, 'restaurants received');
      
      // Transform Django API response to match mobile app format
      const transformedData = data.map((restaurant, index) => ({
        id: restaurant.id || index + 1,
        name: restaurant.name || 'Unknown Restaurant',
        rating: restaurant.rating || 4.0,
        cuisine: getCuisineType(restaurant.name), // Determine cuisine from name
        image: getRestaurantImage(restaurant.name), // Get appropriate image
        description: restaurant.address || `Delicious ${getCuisineType(restaurant.name)} cuisine`,
        priceRange: getPriceRange(restaurant.rating),
        deliveryTime: getDeliveryTime(),
        address: restaurant.address || 'Address not available',
        phone_number: restaurant.phone_number || 'Phone not available',
      }));
      
      console.log('✅ Successfully transformed', transformedData.length, 'restaurants from Django API');
      
      return {
        success: true,
        data: transformedData,
        message: `🎆 Connected to Django API • Loaded ${transformedData.length} restaurants`
      };
    } catch (error) {
      console.error('Django API Error:', error);
      console.log('Falling back to mock data');
      
      // Determine error type for better user messaging
      let errorMessage = 'Django API unavailable';
      if (error.message.includes('timeout')) {
        errorMessage = 'Connection timeout - using offline data';
      } else if (error.message.includes('Network request failed')) {
        errorMessage = 'Network error - using offline data';
      } else if (error.message.includes('HTTP')) {
        errorMessage = 'Server error - using offline data';
      }
      
      // Enhanced fallback with better mock data
      return {
        success: true,
        data: mockRestaurants,
        message: `📱 ${errorMessage} • Showing ${mockRestaurants.length} restaurants`
      };
    }
  },

  // Fetch restaurant by ID
  getRestaurantById: async (id) => {
    await simulateNetworkDelay(500, 1000);
    
    const restaurant = mockRestaurants.find(r => r.id === id);
    
    if (!restaurant) {
      throw new Error(`Restaurant with ID ${id} not found`);
    }
    
    return {
      success: true,
      data: restaurant,
      message: 'Restaurant fetched successfully'
    };
  },

  // Search restaurants by name or cuisine
  searchRestaurants: async (query) => {
    await simulateNetworkDelay(800, 1500);
    
    const filteredRestaurants = mockRestaurants.filter(restaurant =>
      restaurant.name.toLowerCase().includes(query.toLowerCase()) ||
      restaurant.cuisine.toLowerCase().includes(query.toLowerCase())
    );
    
    return {
      success: true,
      data: filteredRestaurants,
      message: `Found ${filteredRestaurants.length} restaurants`
    };
  },

  // Get restaurants by cuisine
  getRestaurantsByCuisine: async (cuisine) => {
    await simulateNetworkDelay();
    
    const filteredRestaurants = mockRestaurants.filter(restaurant =>
      restaurant.cuisine.toLowerCase() === cuisine.toLowerCase()
    );
    
    return {
      success: true,
      data: filteredRestaurants,
      message: `Found ${filteredRestaurants.length} ${cuisine} restaurants`
    };
  },

  // Get top rated restaurants
  getTopRatedRestaurants: async (limit = 5) => {
    await simulateNetworkDelay();
    
    const sortedRestaurants = [...mockRestaurants]
      .sort((a, b) => b.rating - a.rating)
      .slice(0, limit);
    
    return {
      success: true,
      data: sortedRestaurants,
      message: `Top ${limit} restaurants fetched successfully`
    };
  }
};

// Real API configuration (for connecting to Django backend)
export const API_CONFIG = {
  BASE_URL: process.env.EXPO_PUBLIC_API_URL || 'http://127.0.0.1:8000/api',
  ENDPOINTS: {
    RESTAURANTS: '/restaurants/',
    RESTAURANT_STATS: '/restaurants/stats/',
  },
  TIMEOUT: 5000, // Reduced timeout for faster fallback
};

// Real API functions (commented out - use when connecting to Django backend)

export const realRestaurantAPI = {
  getRestaurants: async () => {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.RESTAURANTS}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: API_CONFIG.TIMEOUT,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return {
        success: true,
        data: data,
        message: 'Restaurants fetched successfully'
      };
    } catch (error) {
      throw new Error(`Failed to fetch restaurants: ${error.message}`);
    }
  },
  
  // Add other real API methods here...
};


export default restaurantAPI;
