import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🍽️ Restaurant Directory</h1>
        <p>Discover amazing restaurants in your area</p>
      </header>
      <main className="App-main">
        <RestaurantList />
      </main>
    </div>
  );
}

// Restaurant List Component
function RestaurantList() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  // API base URL - adjust this to match your Django server
  const API_BASE_URL = 'http://127.0.0.1:8000/api';

  // Fetch restaurants from API
  const fetchRestaurants = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE_URL}/restaurants/`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Handle both custom API response format and standard format
      const restaurantData = data.data || data.results || data;
      
      if (Array.isArray(restaurantData)) {
        setRestaurants(restaurantData);
      } else {
        throw new Error('Invalid data format received from API');
      }
      
    } catch (err) {
      console.error('Error fetching restaurants:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch restaurants on component mount and when retrying
  useEffect(() => {
    fetchRestaurants();
  }, [retryCount]);

  // Retry function
  const handleRetry = () => {
    setRetryCount(prev => prev + 1);
  };

  // Loading state
  if (loading) {
    return (
      <div className="restaurant-list-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading restaurants...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="restaurant-list-container">
        <div className="error-message">
          <h3>❌ Oops! Something went wrong</h3>
          <p>Error: {error}</p>
          <div className="error-actions">
            <button onClick={handleRetry} className="retry-button">
              🔄 Try Again
            </button>
            <p className="error-help">
              Make sure the Django server is running at {API_BASE_URL}
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Empty state
  if (restaurants.length === 0) {
    return (
      <div className="restaurant-list-container">
        <div className="empty-state">
          <h3>🍽️ No restaurants found</h3>
          <p>No restaurants are currently available.</p>
          <button onClick={handleRetry} className="retry-button">
            🔄 Refresh
          </button>
        </div>
      </div>
    );
  }

  // Success state - display restaurants
  return (
    <div className="restaurant-list-container">
      <div className="restaurant-list-header">
        <h2>🏪 Available Restaurants ({restaurants.length})</h2>
        <button onClick={handleRetry} className="refresh-button">
          🔄 Refresh
        </button>
      </div>
      
      <div className="restaurant-grid">
        {restaurants.map((restaurant) => (
          <RestaurantCard key={restaurant.id} restaurant={restaurant} />
        ))}
      </div>
    </div>
  );
}

// Individual Restaurant Card Component
function RestaurantCard({ restaurant }) {
  // Generate star rating display
  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
      stars.push(<span key={i} className="star full">⭐</span>);
    }
    
    // Half star
    if (hasHalfStar) {
      stars.push(<span key="half" className="star half">⭐</span>);
    }
    
    // Empty stars
    const remainingStars = 5 - Math.ceil(rating);
    for (let i = 0; i < remainingStars; i++) {
      stars.push(<span key={`empty-${i}`} className="star empty">☆</span>);
    }
    
    return stars;
  };

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="restaurant-card">
      <div className="restaurant-card-header">
        <h3 className="restaurant-name">{restaurant.name}</h3>
        <div className="restaurant-rating">
          <div className="stars">
            {renderStars(parseFloat(restaurant.rating))}
          </div>
          <span className="rating-number">({restaurant.rating})</span>
        </div>
      </div>
      
      <div className="restaurant-details">
        <div className="detail-item">
          <span className="detail-icon">📍</span>
          <span className="detail-text">{restaurant.address}</span>
        </div>
        
        <div className="detail-item">
          <span className="detail-icon">📞</span>
          <span className="detail-text">{restaurant.phone_number}</span>
        </div>
        
        {restaurant.created_at && (
          <div className="detail-item">
            <span className="detail-icon">📅</span>
            <span className="detail-text">Added: {formatDate(restaurant.created_at)}</span>
          </div>
        )}
      </div>
      
      <div className="restaurant-actions">
        <button className="action-button primary">
          📞 Call Now
        </button>
        <button className="action-button secondary">
          📍 Get Directions
        </button>
      </div>
    </div>
  );
}

export default App;
