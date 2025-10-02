<template>
  <div>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-light bg-primary">
      <div class="container-fluid">
        <router-link class="nav-link text-white fw-bold" :to="{ name: 'Similar Users Page' }">
          HobbieBobbie
        </router-link>
        <div>
          <ul class="navbar-nav d-flex flex-row">
            <li class="nav-item">
              <router-link class="nav-link text-white fw-bold me-3" :to="{ name: 'Profile Page' }">
                Profile
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link text-white fw-bold me-3" :to="{ name: 'Similar Users Page' }">
                Similar Users
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link text-white fw-bold me-3" :to="{ name: 'Friends Page' }">
                Friends
              </router-link>
            </li>
          </ul>
        </div>
        <a class="btn btn-danger" href="/logout">Logout</a>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="container pt-4">
      <RouterView class="flex-shrink-0" />
    </main>
  </div>
</template>


<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { RouterView } from "vue-router";
import { checkLoginStatus } from "./utils/auth";
import { useCsrfStore } from "./stores/csrf";

function getCookie(name: string): string | undefined {
  let value = '; ' + document.cookie;
  let parts = value.split('; ' + name + '=');
  if (parts.length === 2) return parts.pop()?.split(';').shift();
}

export default defineComponent({
  components: { RouterView },
  setup() {
    onMounted(() => {
      checkLoginStatus();
    });
  },
  async mounted() {
    const csrfStore = useCsrfStore();

    // Retrieve the CSRF token from cookies
    const csrfToken = getCookie('csrftoken');  // Change 'csrftoken' if your token cookie name is different

    if (csrfToken) {
      // Set the CSRF token in the store
      csrfStore.setCsrfToken(csrfToken);
    }
  },
});
</script>

