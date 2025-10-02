import { defineStore } from "pinia";

export const useCsrfStore = defineStore("csrf", {
  state: () => ({
    csrfToken: "",
  }),
  actions: {
    setCsrfToken(token: string) {
      this.csrfToken = token;
    },
    updateCsrfToken: async function() {
      try {
        const response = await fetch('/get-csrf-token/');
        if (response.ok) {
          const data = await response.json();
          this.setCsrfToken(data.csrfToken);
        } else {
          console.error('Failed to fetch new CSRF token');
        }
      } catch (error) {
        console.error('Error fetching new CSRF token:', error);
      }
    },
  },
});
