import axios from 'axios';
import { useUserStore } from '../stores/user';

export async function checkLoginStatus() {
  const userStore = useUserStore();

  try {
    const response = await axios.get('/api/check-login/'); // Adjust the endpoint as per your backend
    if (response.status === 200 && response.data.loggedIn) {
      const profile = response.data.profile  
      userStore.setUser(profile); // Store the profile in Pinia
      
    } else {
      userStore.clearUser(); // Clear the user state if not logged in
    }
  } catch (error) {
    console.error('Error checking login status:', error);
    userStore.clearUser(); // Handle errors by resetting the user state
  }
}
