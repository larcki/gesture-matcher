Desktop application to record and calculate similarity of two hand gestures recorded with [Leap motion](https://www.ultraleap.com/product/leap-motion-controller/) device.

### Similarity calculation 
The application records the data as an array of 3-dimensional points of each finger and a palm and uses Dynamic Time Warping (DTW) algorithm to calculate the distance of the two recorded data sets. The distance is then converted into a similarity value between 0 and 1.
