import React from 'react';
import { StyleSheet, Text, TouchableOpacity } from 'react-native';
import Animated, { FadeIn } from 'react-native-reanimated';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

const ErrorState = ({ onRetry }) => (
  <Animated.View entering={FadeIn} style={styles.errorContainer}>
    <LinearGradient
      colors={['#ff9a9e', '#fecfef']}
      style={styles.errorGradient}
    >
      <Ionicons name="alert-circle-outline" size={60} color="#ffffff" />
      <Text style={styles.errorTitle}>Oops! Something went wrong</Text>
      <Text style={styles.errorMessage}>
        Unable to load restaurants. Please check your connection and try again.
      </Text>
      <TouchableOpacity style={styles.retryButton} onPress={onRetry}>
        <LinearGradient
          colors={['#667eea', '#764ba2']}
          style={styles.retryGradient}
        >
          <Ionicons name="refresh" size={20} color="#ffffff" />
          <Text style={styles.retryText}>Try Again</Text>
        </LinearGradient>
      </TouchableOpacity>
    </LinearGradient>
  </Animated.View>
);

const styles = StyleSheet.create({
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

export default ErrorState;
