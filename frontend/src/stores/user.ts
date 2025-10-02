import { defineStore } from 'pinia';

interface Profile {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    date_of_birth: string;
    hobbies: string[];
    age: number;

}

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: null as Profile | null, // Store the user ID
    loggedIn: false,              // Boolean to track login status
  }),
  actions: {
    setUser(profile: Profile) {
        this.profile = profile;
        this.loggedIn = true;
    },
    clearUser() {
      this.profile = null;
      this.loggedIn = false;
    },
  },
});
