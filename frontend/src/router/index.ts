// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/Hobbies.vue';
import Profile from '../pages/Profile.vue';
import SimilarUsersPage from '../pages/SimilarUsersPage.vue';
import FriendsPage from '../pages/Friends.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/', name: 'Profile Page', component: Profile },
        { path: '/', name: 'Similar Users Page', component: SimilarUsersPage },
        { path: '/', name: 'Friends Page', component: FriendsPage }
    ]
})

export default router