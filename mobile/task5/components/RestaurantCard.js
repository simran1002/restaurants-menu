import React from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';

const AnimatedTouchableOpacity = Animated.createAnimatedComponent(TouchableOpacity);

const { width } = Dimensions.get('window');

const RestaurantCard = ({ restaurant, index }) => {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ scale: scale.value }],
      opacity: opacity.value,
    };
  }, []);

  const handlePressIn = () => {
    scale.value = withSpring(0.95);
    opacity.value = withTiming(0.8);
  };

  const handlePressOut = () => {
    scale.value = withSpring(1);
    opacity.value = withTiming(1);
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <Ionicons key={i} name="star" size={16} color="#FFD700" />
      );
    }

    if (hasHalfStar) {
      stars.push(
        <Ionicons key="half" name="star-half" size={16} color="#FFD700" />
      );
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <Ionicons key={`empty-${i}`} name="star-outline" size={16} color="#FFD700" />
      );
    }

    return stars;
  };

  return (
    <View style={styles.cardContainer}>
      <AnimatedTouchableOpacity
        activeOpacity={1}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        style={[styles.card, animatedStyle]}
      >
        {/* Restaurant Image */}
        <View style={styles.imageContainer}>
          <Image
            source={{ uri: restaurant.image }}
            style={styles.restaurantImage}
            resizeMode="cover"
          />
          <LinearGradient
            colors={['transparent', 'rgba(0,0,0,0.7)']}
            style={styles.imageOverlay}
          />
          
          {/* Floating Elements */}
          <View style={styles.floatingElements}>
            <View style={styles.cuisineBadge}>
              <Ionicons name="restaurant" size={12} color="#ffffff" />
              <Text style={styles.cuisineText}>{restaurant.cuisine}</Text>
            </View>
            
            <View style={styles.ratingBadge}>
              <Ionicons name="star" size={14} color="#FFD700" />
              <Text style={styles.ratingBadgeText}>{restaurant.rating}</Text>
            </View>
          </View>
        </View>

        {/* Card Content */}
        <LinearGradient
          colors={['#ffffff', '#fafbfc']}
          style={styles.cardContent}
        >
          <View style={styles.headerSection}>
            <Text style={styles.restaurantName} numberOfLines={1}>
              {restaurant.name}
            </Text>
            <View style={styles.priceContainer}>
              <Text style={styles.priceRange}>{restaurant.priceRange}</Text>
            </View>
          </View>

          <Text style={styles.description} numberOfLines={2}>
            {restaurant.description}
          </Text>

          <View style={styles.bottomSection}>
            <View style={styles.starsContainer}>
              {renderStars(restaurant.rating)}
            </View>
            
            <View style={styles.deliverySection}>
              <View style={styles.deliveryInfo}>
                <Ionicons name="time" size={16} color="#10B981" />
                <Text style={styles.deliveryTime}>{restaurant.deliveryTime}</Text>
              </View>
              
              <View style={styles.locationInfo}>
                <Ionicons name="location" size={16} color="#6B7280" />
                <Text style={styles.locationText} numberOfLines={1}>
                  {restaurant.address || 'Nearby'}
                </Text>
              </View>
            </View>
          </View>
          
          {/* Action Button */}
          <TouchableOpacity style={styles.actionButton}>
            <LinearGradient
              colors={['#667eea', '#764ba2']}
              style={styles.actionButtonGradient}
            >
              <Text style={styles.actionButtonText}>Order Now</Text>
              <Ionicons name="arrow-forward" size={16} color="#ffffff" />
            </LinearGradient>
          </TouchableOpacity>
        </LinearGradient>
      </AnimatedTouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  cardContainer: {
    marginHorizontal: 16,
    marginBottom: 20,
  },
  card: {
    borderRadius: 24,
    elevation: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.15,
    shadowRadius: 16,
    backgroundColor: '#ffffff',
    overflow: 'hidden',
  },
  imageContainer: {
    position: 'relative',
    height: 200,
  },
  restaurantImage: {
    width: '100%',
    height: '100%',
  },
  imageOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 80,
  },
  floatingElements: {
    position: 'absolute',
    top: 12,
    left: 12,
    right: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  cuisineBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.8)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    backdropFilter: 'blur(10px)',
  },
  cuisineText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '700',
    marginLeft: 4,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  ratingBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.95)',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 16,
    backdropFilter: 'blur(10px)',
  },
  ratingBadgeText: {
    color: '#1F2937',
    fontSize: 12,
    fontWeight: '700',
    marginLeft: 2,
  },
  cardContent: {
    padding: 20,
    borderRadius: 24,
  },
  headerSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  restaurantName: {
    fontSize: 20,
    fontWeight: '800',
    color: '#111827',
    flex: 1,
    letterSpacing: -0.5,
  },
  priceContainer: {
    backgroundColor: '#F3F4F6',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginLeft: 12,
    borderWidth: 1,
    borderColor: '#E5E7EB',
  },
  priceRange: {
    fontSize: 14,
    fontWeight: '700',
    color: '#374151',
  },
  description: {
    fontSize: 15,
    color: '#6B7280',
    marginBottom: 16,
    lineHeight: 22,
    fontWeight: '400',
  },
  bottomSection: {
    marginBottom: 16,
  },
  starsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  deliverySection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  deliveryInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ECFDF5',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#D1FAE5',
  },
  deliveryTime: {
    marginLeft: 4,
    fontSize: 12,
    fontWeight: '600',
    color: '#065F46',
  },
  locationInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    marginLeft: 12,
  },
  locationText: {
    marginLeft: 4,
    fontSize: 12,
    color: '#6B7280',
    fontWeight: '500',
    flex: 1,
  },
  actionButton: {
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#667eea',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  actionButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    paddingHorizontal: 24,
  },
  actionButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
    marginRight: 8,
    letterSpacing: 0.5,
  },
});

export default RestaurantCard;
