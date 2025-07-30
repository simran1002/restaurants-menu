import React from 'react';
import { StyleSheet, View } from 'react-native';
import Animated, { FadeIn } from 'react-native-reanimated';

const LoadingCard = ({ index }) => (
  <Animated.View
    entering={FadeIn.delay(index * 50)}
    style={styles.loadingCard}
  >
    <View style={styles.loadingImagePlaceholder} />
    <View style={styles.loadingContent}>
      <View style={styles.loadingTitle} />
      <View style={styles.loadingDescription} />
      <View style={styles.loadingRating} />
    </View>
  </Animated.View>
);

const styles = StyleSheet.create({
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
});

export default LoadingCard;
