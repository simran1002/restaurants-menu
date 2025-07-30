import React, { useState } from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🍽️ Add New Restaurant</h1>
        <p>Share your favorite restaurant with the community</p>
      </header>
      <main className="App-main">
        <RestaurantForm />
      </main>
    </div>
  );
}

// Restaurant Form Component
function RestaurantForm() {
  // Form state using controlled components
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    phone_number: '',
    rating: ''
  });

  // Form validation errors
  const [errors, setErrors] = useState({});
  
  // Submission state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null); // 'success', 'error', null
  const [submitMessage, setSubmitMessage] = useState('');

  // API base URL
  const API_BASE_URL = 'http://127.0.0.1:8000/api';

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  // Validate form data
  const validateForm = () => {
    const newErrors = {};

    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = 'Restaurant name is required';
    } else if (formData.name.trim().length < 2) {
      newErrors.name = 'Restaurant name must be at least 2 characters';
    }

    // Address validation
    if (!formData.address.trim()) {
      newErrors.address = 'Address is required';
    } else if (formData.address.trim().length < 10) {
      newErrors.address = 'Please provide a complete address (minimum 10 characters)';
    }

    // Phone number validation
    if (!formData.phone_number.trim()) {
      newErrors.phone_number = 'Phone number is required';
    } else {
      // Basic phone number format validation
      const phoneRegex = /^[\+]?[1-9][\d\s\-\(\)]{7,15}$/;
      if (!phoneRegex.test(formData.phone_number.trim())) {
        newErrors.phone_number = 'Please enter a valid phone number';
      }
    }

    // Rating validation
    if (!formData.rating) {
      newErrors.rating = 'Rating is required';
    } else {
      const rating = parseFloat(formData.rating);
      if (isNaN(rating) || rating < 0 || rating > 5) {
        newErrors.rating = 'Rating must be between 0.0 and 5.0';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!validateForm()) {
      setSubmitStatus('error');
      setSubmitMessage('Please fix the errors above and try again.');
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus(null);
    setSubmitMessage('');

    try {
      // Prepare data for API
      const submitData = {
        name: formData.name.trim(),
        address: formData.address.trim(),
        phone_number: formData.phone_number.trim(),
        rating: parseFloat(formData.rating)
      };

      const response = await fetch(`${API_BASE_URL}/restaurants/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submitData)
      });

      const result = await response.json();

      if (response.ok) {
        // Success
        setSubmitStatus('success');
        setSubmitMessage(`🎉 Restaurant "${submitData.name}" has been added successfully!`);
        
        // Reset form
        setFormData({
          name: '',
          address: '',
          phone_number: '',
          rating: ''
        });
        setErrors({});
      } else {
        // API returned an error
        setSubmitStatus('error');
        if (result.errors) {
          // Handle field-specific errors from API
          setErrors(result.errors);
          setSubmitMessage('Please fix the errors and try again.');
        } else {
          setSubmitMessage(result.message || 'Failed to add restaurant. Please try again.');
        }
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setSubmitStatus('error');
      setSubmitMessage('Network error. Please check if the server is running and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Reset form
  const handleReset = () => {
    setFormData({
      name: '',
      address: '',
      phone_number: '',
      rating: ''
    });
    setErrors({});
    setSubmitStatus(null);
    setSubmitMessage('');
  };

  return (
    <div className="form-container">
      <div className="form-card">
        <div className="form-header">
          <h2>🏪 Restaurant Information</h2>
          <p>Please fill in all the details about the restaurant</p>
        </div>

        <form onSubmit={handleSubmit} className="restaurant-form">
          {/* Restaurant Name */}
          <div className="form-group">
            <label htmlFor="name" className="form-label">
              🏪 Restaurant Name *
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className={`form-input ${errors.name ? 'error' : ''}`}
              placeholder="Enter restaurant name"
              maxLength={200}
            />
            {errors.name && <span className="error-message">{errors.name}</span>}
          </div>

          {/* Address */}
          <div className="form-group">
            <label htmlFor="address" className="form-label">
              📍 Address *
            </label>
            <textarea
              id="address"
              name="address"
              value={formData.address}
              onChange={handleInputChange}
              className={`form-textarea ${errors.address ? 'error' : ''}`}
              placeholder="Enter complete address"
              rows={3}
            />
            {errors.address && <span className="error-message">{errors.address}</span>}
          </div>

          {/* Phone Number */}
          <div className="form-group">
            <label htmlFor="phone_number" className="form-label">
              📞 Phone Number *
            </label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleInputChange}
              className={`form-input ${errors.phone_number ? 'error' : ''}`}
              placeholder="e.g., +1-555-0123"
              maxLength={20}
            />
            {errors.phone_number && <span className="error-message">{errors.phone_number}</span>}
          </div>

          {/* Rating */}
          <div className="form-group">
            <label htmlFor="rating" className="form-label">
              ⭐ Rating *
            </label>
            <div className="rating-input-container">
              <input
                type="number"
                id="rating"
                name="rating"
                value={formData.rating}
                onChange={handleInputChange}
                className={`form-input rating-input ${errors.rating ? 'error' : ''}`}
                placeholder="0.0"
                min="0"
                max="5"
                step="0.1"
              />
              <span className="rating-label">out of 5.0</span>
            </div>
            <div className="rating-guide">
              <span className="rating-guide-item">⭐ 1-2: Poor</span>
              <span className="rating-guide-item">⭐ 3: Average</span>
              <span className="rating-guide-item">⭐ 4: Good</span>
              <span className="rating-guide-item">⭐ 5: Excellent</span>
            </div>
            {errors.rating && <span className="error-message">{errors.rating}</span>}
          </div>

          {/* Submit Status Message */}
          {submitMessage && (
            <div className={`submit-message ${submitStatus}`}>
              {submitMessage}
            </div>
          )}

          {/* Form Actions */}
          <div className="form-actions">
            <button
              type="button"
              onClick={handleReset}
              className="btn btn-secondary"
              disabled={isSubmitting}
            >
              🔄 Reset
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="spinner-small"></span>
                  Adding...
                </>
              ) : (
                <>
                  ➕ Add Restaurant
                </>
              )}
            </button>
          </div>
        </form>

        {/* Form Tips */}
        <div className="form-tips">
          <h4>💡 Tips for better results:</h4>
          <ul>
            <li>Use the complete restaurant name as it appears officially</li>
            <li>Provide a detailed address including city and postal code</li>
            <li>Include country code in phone number for international restaurants</li>
            <li>Rate based on overall experience: food, service, and ambiance</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
