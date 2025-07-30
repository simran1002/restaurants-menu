import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  FlatList,
  SafeAreaView,
  RefreshControl,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
} from 'react-native-reanimated';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

// Import components
import RestaurantCard from './components/RestaurantCard';
import LoadingCard from './components/LoadingCard';
import ErrorState from './components/ErrorState';

// Import API service
import { restaurantAPI } from './services/api';



const App = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const headerOpacity = useSharedValue(0);
  const headerTranslateY = useSharedValue(-50);

  const headerAnimatedStyle = useAnimatedStyle(() => {
    return {
      opacity: headerOpacity.value,
      transform: [{ translateY: headerTranslateY.value }],
    };
  });

  // Fetch restaurants using API service
  const fetchRestaurants = async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      setError(false);

      const response = await restaurantAPI.getRestaurants();
      
      if (response.success) {
        setRestaurants(response.data);
        console.log('✅', response.message);
      } else {
        throw new Error(response.message || 'Failed to fetch restaurants');
      }
    } catch (err) {
      console.error('❌ Failed to fetch restaurants:', err.message);
      setError(true);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchRestaurants();
    
    // Animate header with slight delay to avoid warnings
    const animateHeader = () => {
      headerOpacity.value = withTiming(1, { duration: 800 });
      headerTranslateY.value = withSpring(0);
    };
    
    const timer = setTimeout(animateHeader, 100);
    return () => clearTimeout(timer);
  }, []);

  const handleRefresh = () => {
    fetchRestaurants(true);
  };

  const handleRetry = () => {
    fetchRestaurants();
  };

  const renderRestaurant = ({ item, index }) => (
    <RestaurantCard restaurant={item} index={index} />
  );

  const renderLoadingItem = ({ item, index }) => (
    <LoadingCard index={index} />
  );

  const ListHeader = () => (
    <Animated.View style={[styles.header, headerAnimatedStyle]}>
      <LinearGradient
        colors={['#667eea', '#764ba2', '#f093fb']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.headerGradient}
      >
        <View style={styles.headerContent}>
          <View style={styles.headerTextContainer}>
            <Text style={styles.headerTitle}>🍽️ Discover</Text>
            <Text style={styles.headerSubtitle}>Amazing restaurants near you</Text>
            <View style={styles.statsContainer}>
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>{restaurants.length}</Text>
                <Text style={styles.statLabel}>Restaurants</Text>
              </View>
              <View style={styles.statDivider} />
              <View style={styles.statItem}>
                <Text style={styles.statNumber}>4.5★</Text>
                <Text style={styles.statLabel}>Avg Rating</Text>
              </View>
            </View>
          </View>
          
          <View style={styles.headerIconContainer}>
            <View style={styles.headerIcon}>
              <Ionicons name="restaurant" size={28} color="#ffffff" />
            </View>
          </View>
        </View>
        
        {/* Decorative elements */}
        <View style={styles.decorativeCircle1} />
        <View style={styles.decorativeCircle2} />
      </LinearGradient>
    </Animated.View>
  );

  if (error && !refreshing) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="light-content" backgroundColor="#667eea" />
        <ListHeader />
        <ErrorState onRetry={handleRetry} />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#667eea" />
      
      <FlatList
        data={loading ? Array(6).fill({}) : restaurants}
        renderItem={loading ? renderLoadingItem : renderRestaurant}
        keyExtractor={(item, index) => loading ? `loading-${index}` : `restaurant-${item.id}`}
        ListHeaderComponent={ListHeader}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={handleRefresh}
            colors={['#667eea']}
            tintColor="#667eea"
          />
        }
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  listContainer: {
    paddingBottom: 30,
  },
  header: {
    marginBottom: 24,
  },
  headerGradient: {
    paddingHorizontal: 24,
    paddingVertical: 40,
    borderBottomLeftRadius: 32,
    borderBottomRightRadius: 32,
    position: 'relative',
    overflow: 'hidden',
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    zIndex: 2,
  },
  headerTextContainer: {
    flex: 1,
  },
  headerTitle: {
    fontSize: 36,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 8,
    letterSpacing: -1,
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#ffffff',
    opacity: 0.95,
    marginBottom: 20,
    fontWeight: '500',
  },
  statsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
    backdropFilter: 'blur(10px)',
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 18,
    fontWeight: '800',
    color: '#ffffff',
  },
  statLabel: {
    fontSize: 12,
    color: '#ffffff',
    opacity: 0.8,
    marginTop: 2,
    fontWeight: '500',
  },
  statDivider: {
    width: 1,
    height: 30,
    backgroundColor: 'rgba(255,255,255,0.3)',
    marginHorizontal: 16,
  },
  headerIconContainer: {
    marginLeft: 16,
  },
  headerIcon: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    padding: 16,
    borderRadius: 20,
    backdropFilter: 'blur(10px)',
  },
  decorativeCircle1: {
    position: 'absolute',
    top: -50,
    right: -30,
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: 'rgba(255,255,255,0.1)',
    zIndex: 1,
  },
  decorativeCircle2: {
    position: 'absolute',
    bottom: -40,
    left: -20,
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255,255,255,0.05)',
    zIndex: 1,
  },
  // Loading and Error styles
  loadingCard: {
    marginHorizontal: 20,
    marginBottom: 15,
    backgroundColor: '#ffffff',
    borderRadius: 20,
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    overflow: 'hidden',
  },
  loadingImagePlaceholder: {
    height: 120,
    backgroundColor: '#e2e8f0',
  },
  loadingContent: {
    padding: 16,
  },
  loadingTitle: {
    height: 20,
    backgroundColor: '#e2e8f0',
    borderRadius: 4,
    marginBottom: 8,
    width: '70%',
  },
  loadingDescription: {
    height: 16,
    backgroundColor: '#e2e8f0',
    borderRadius: 4,
    marginBottom: 12,
    width: '90%',
  },
  loadingRating: {
    height: 16,
    backgroundColor: '#e2e8f0',
    borderRadius: 4,
    width: '40%',
  },
  errorContainer: {
    flex: 1,
    margin: 20,
    borderRadius: 20,
    overflow: 'hidden',
  },
  errorGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  errorTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    marginTop: 20,
    marginBottom: 10,
    textAlign: 'center',
  },
  errorMessage: {
    fontSize: 16,
    color: '#ffffff',
    textAlign: 'center',
    opacity: 0.9,
    lineHeight: 24,
    marginBottom: 30,
  },
  retryButton: {
    borderRadius: 25,
    overflow: 'hidden',
  },
  retryGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  retryText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
});

export default App;
