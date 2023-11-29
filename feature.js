// Function to calculate the distance between two points using the Haversine formula
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the Earth in kilometers
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * (Math.PI / 180)) *
        Math.cos(lat2 * (Math.PI / 180)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = R * c;
    return distance * 1000; // Convert to meters
  }
  
  // Function to check if the user is inside the geofence
  function checkGeofence(position) {
    const fenceLatitude = 18.885732529262775; // Latitude of the geofence
    const fenceLongitude = 81.34207844448035; // Longitude of the geofence
    const userLatitude = position.coords.latitude;
    const userLongitude = position.coords.longitude;
  
    console.log('User Location - Latitude:', userLatitude);
    console.log('User Location - Longitude:', userLongitude);
  
    const distance = calculateDistance(
      fenceLatitude,
      fenceLongitude,
      userLatitude,
      userLongitude
    );

    const studentId = prompt('Enter your student ID:');

    if (distance <= 1000) {
      // User is inside the geofence
      console.log('User is inside the geofence.');
  
      // Get the student ID from the user
      // const studentId = prompt('Enter your student ID:');
      if (studentId) {
        // Store the user's current location and geolocation status message in the Firestore Realtime Database
  
        database.ref('students/'+studentId+'/GeoLocation_Details').set({
          latitude: userLatitude,
          longitude: userLongitude,
          geolocationStatus: 'User is inside the geofence.'
        })
        .then(data=>console.log(data))
        .catch(err=>console.log(err))
        
      } else {
        console.log('Invalid student ID.');
      }
    } else {
      // User is outside the geofence
      if (studentId) {
        // Store the user's current location and geolocation status message in the Firestore Realtime Database

        database.ref('students/'+studentId+'/GeoLocation_Details').set({
          latitude: userLatitude,
          longitude: userLongitude,
          geolocationStatus: 'User is outside the geofence.'
        })
        .then(data=>console.log(data))
        .catch(err=>console.log(err))

      } else {
        console.log('Invalid student ID.');
      }
    }
  }
  
  // Function to handle the geolocation error
  function handleLocationError(error) {
    switch (error.code) {
      case error.PERMISSION_DENIED:
        console.log('User denied the request for Geolocation.');
        break;
      case error.POSITION_UNAVAILABLE:
        console.log('Location information is unavailable.');
        break;
      case error.TIMEOUT:
        console.log('The request to get user location timed out.');
        break;
      case error.UNKNOWN_ERROR:
        console.log('An unknown error occurred.');
        break;
    }
  }
  
  // Function to get the user's current location
  function getCurrentLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        checkGeofence,
        handleLocationError
      );
    } else {
      console.log('Geolocation is not supported by this browser.');
    }
  }