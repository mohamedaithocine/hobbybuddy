<template>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Similar Users</h1>

        <!-- Filter Section -->
        <div class="card p-3 mb-4">
            <div class="row">
                <div class="col-md-6">
                    <label for="minAge" class="form-label"><strong>Min Age:</strong></label>
                    <input 
                        type="number" 
                        id="minAge" 
                        v-model="minAge" 
                        @change="fetchUsers" 
                        class="form-control"
                        placeholder="Enter minimum age" 
                    />
                </div>
                <div class="col-md-6">
                    <label for="maxAge" class="form-label"><strong>Max Age:</strong></label>
                    <input 
                        type="number" 
                        id="maxAge" 
                        v-model="maxAge" 
                        @change="fetchUsers" 
                        class="form-control"
                        placeholder="Enter maximum age" 
                    />
                </div>
            </div>
        </div>

        <!-- Users List -->
        <div class="list-group">
            <div 
                v-for="user in users" 
                :key="user.user" 
                class="list-group-item list-group-item-action mb-3"
            >
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h5 class="mb-1">{{ user.user }}</h5>
                        <p class="mb-1">
                            <strong>Common Hobbies:</strong> {{ formatHobbies(user.common_hobbies_list) }}
                        </p>
                    </div>
                    <button 
                        @click="sendFriendRequest(user.user)" 
                        class="btn btn-primary"
                        :disabled="sentRequests.has(user.user)"
                    >
                        {{ sentRequests.has(user.user) ? 'Friend Request Sent' : 'Send Friend Request' }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Pagination -->
        <div class="d-flex justify-content-between mt-4 mb-5">
            <button 
                @click="prevPage" 
                :disabled="page === 1" 
                class="btn btn-secondary"
            >
                Previous
            </button>
            <button 
                @click="nextPage" 
                :disabled="page === numPages" 
                class="btn btn-secondary"
            >
                Next
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useCsrfStore } from "../stores/csrf";
import { useUserStore } from "../stores/user";


// Define types for the users and responses
interface User {
    user: string;
    common_hobbies_list: string[];
}

interface UsersResponse {
    users: User[];
    num_pages: number;
}

export default defineComponent({
    setup() {
        const users = ref<User[]>([]);
        const page = ref<number>(1);
        const minAge = ref<number>(15);
        const maxAge = ref<number>(20);
        const numPages = ref<number>(1);
        const sentRequests = ref(new Set<string>());
        const userStore = useUserStore();


        const fetchUsers = async (): Promise<void> => {
            const params = new URLSearchParams({
                page: page.value.toString(),
                min_age: minAge.value.toString(),
                max_age: maxAge.value.toString(),
            });

            try {
                const response = await fetch(`/get_similar_users/?${params.toString()}`);
                if (!response.ok) {
                    throw new Error(`Failed to fetch users: ${response.statusText}`);
                }
                const data: UsersResponse = await response.json();
                users.value = data.users;
                numPages.value = data.num_pages;

                const sentResponse = await fetch(`/users/${userStore.profile?.id}/friend_requests_by_user/`);
                if (!sentResponse.ok) {
                    throw new Error(`Failed to fetch friend requests: ${sentResponse.statusText}`);
                }
                const sentData = await sentResponse.json();
                console.log(sentData);
                sentRequests.value = new Set(
                    sentData.sent_requests.map((request: { friend_request_to: { username: string } }) => request.friend_request_to.username)
                );
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        };

        const sendFriendRequest = async (username: string): Promise<void> => {
            try {
                const csrfStore = useCsrfStore();
                const response = await fetch(`/send_friend_request/${username}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfStore.csrfToken,
                    },
                });

                const data = await response.json();
                if (response.ok) {
                    sentRequests.value.add(username);
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.error("Error sending friend request:", error);
            }
        };

        const prevPage = (): void => {
            if (page.value > 1) {
                page.value--;
                fetchUsers();
            }
        };

        const nextPage = (): void => {
            if (page.value < numPages.value) {
                page.value++;
                fetchUsers();
            }
        };

        const formatHobbies = (hobbies: string[] | undefined): string => {
            if (!hobbies || hobbies.length === 0) {
                return "None";
            }
            return hobbies.join(", ");
        };

        // Fetch users on component mount
        fetchUsers();

        return {
            users,
            page,
            minAge,
            maxAge,
            numPages,
            fetchUsers,
            sendFriendRequest,
            prevPage,
            nextPage,
            formatHobbies,
            sentRequests,
        };
    },
});
</script>

