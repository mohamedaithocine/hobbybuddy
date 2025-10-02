<template>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Your Friends</h1>

        <!-- Accepted Friends -->
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h2 class="h5">Accepted Friends</h2>
            </div>
            <div class="card-body">
                <div v-if="friends.length > 0">
                    <ul class="list-group">
                        <li v-for="friend in friends" :key="friend.id" class="list-group-item d-flex justify-content-between align-items-center">
                            <span>
                                <strong>Friend:</strong>
                                {{ friend.friend_request_from.id == user_id
                                    ? friend.friend_request_to.username
                                    : friend.friend_request_from.username }}
                            </span>
                            <button 
                                @click="removeFriend(friend.id)" 
                                class="btn btn-warning btn-sm"
                            >
                                Remove Friend
                            </button>
                        </li>
                    </ul>
                </div>
                <div v-else>
                    <p class="text-muted">You have no friends 😭😭</p>
                </div>
            </div>
        </div>

        <!-- Received Friend Requests -->
        <div class="card mb-4">
            <div class="card-header bg-success text-white">
                <h2 class="h5">Friend Requests Received</h2>
            </div>
            <div class="card-body">
                <div v-if="receivedRequests.length > 0">
                    <ul class="list-group">
                        <li v-for="request in receivedRequests" :key="request.id" class="list-group-item d-flex justify-content-between align-items-center">
                            <span>
                                <strong>From:</strong> {{ request.friend_request_from.username }}
                            </span>
                            <div>
                                <button 
                                    @click="acceptFriend(request.id)" 
                                    class="btn btn-success btn-sm me-2"
                                >
                                    Accept
                                </button>
                                <button 
                                    @click="rejectFriend(request.id)" 
                                    class="btn btn-danger btn-sm"
                                >
                                    Reject
                                </button>
                            </div>
                        </li>
                    </ul>
                </div>
                <div v-else>
                    <p class="text-muted">You have no pending friend requests.</p>
                </div>
            </div>
        </div>

        <!-- Sent Friend Requests -->
        <div class="card mb-5">
            <div class="card-header bg-info text-white">
                <h2 class="h5">Friend Requests Sent</h2>
            </div>
            <div class="card-body">
                <div v-if="sentRequests.length > 0">
                    <ul class="list-group">
                        <li v-for="request in sentRequests" :key="request.id" class="list-group-item">
                            <p>
                                <strong>To:</strong> {{ request.friend_request_to.username }}
                            </p>
                            <p class="text-muted mb-0">Status: Pending</p>
                        </li>
                    </ul>
                </div>
                <div v-else>
                    <p class="text-muted">You have not sent any friend requests yet.</p>
                </div>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
// This loads it from the global store
import { useUserStore } from "../stores/user";
import { useCsrfStore } from "../stores/csrf";

export default {
    data() {
        const userStore = useUserStore();
        return {
            friends: Array<{ id: number; friend_request_from: { id: number; username: string }; friend_request_to: { id: number; username: string } }>(), // List of friends fetched from the backend
            receivedRequests: Array<{ id: number; friend_request_from: { username: string } }>(), // Friend requests received by the user
            sentRequests: Array<{ id: number; friend_request_to: { username: string } }>(), // Friend requests sent by the user
            user_id: userStore.profile?.id, // Logged-in user's ID
        };
    },
    methods: {
        async fetchFriends() {
            try {
                const response = await fetch(`/users/${this.user_id}/friends/`);
                const data = await response.json();
                this.friends = data.friends;
            } catch (error) {
                console.error("Error fetching friends:", error);
            }
        },
        async fetchFriendRequests() {
            // Fetch friend requests received
            try {
                const receivedResponse = await fetch(`/users/${this.user_id}/friend_requests_to_user/`);
                const receivedData = await receivedResponse.json();
                this.receivedRequests = receivedData.received_requests;
            } catch (error) {
                console.error("Error fetching received friend requests:", error);
            }

            // Fetch friend requests sent
            try {
                const sentResponse = await fetch(`/users/${this.user_id}/friend_requests_by_user/`);
                const sentData = await sentResponse.json();
                this.sentRequests = sentData.sent_requests;
            } catch (error) {
                console.error("Error fetching sent friend requests:", error);
            }
        },
        async acceptFriend(friendId: number) {
            const csrfStore = useCsrfStore(); // Access CSRF token from the store
            try {
                const response = await fetch(`/friends/${friendId.toString()}/accept/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfStore.csrfToken, // Include CSRF token
                    },
                });
                if (response.ok) {
                    this.fetchFriendRequests(); // Refresh the friend requests list
                    this.fetchFriends(); // Refresh the friend list
                } else {
                    const data = await response.json();
                    alert(data.error || "Failed to accept friend request.");
                }
            } catch (error) {
                console.error("Error accepting friend request:", error);
            }
        },
        async rejectFriend(friendId: number) {
            const csrfStore = useCsrfStore(); // Access CSRF token from the store
            try {
                const response = await fetch(`/friends/${friendId.toString()}/reject/`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfStore.csrfToken, // Include CSRF token
                    },
                });
                if (response.ok) {
                    this.fetchFriendRequests(); // Refresh the friend requests list
                } else {
                    const data = await response.json();
                    alert(data.error || "Failed to reject friend request.");
                }
            } catch (error) {
                console.error("Error rejecting friend request:", error);
            }
        },
        async removeFriend(friendId: number) {
            const csrfStore = useCsrfStore(); // Access CSRF token from the store
            try {
                const response = await fetch(`/friends/${friendId.toString()}/remove/`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfStore.csrfToken, // Include CSRF token
                    },
                });
                if (response.ok) {
                    this.fetchFriends(); // Refresh the friend list
                } else {
                    const data = await response.json();
                    alert(data.error || "Failed to remove friend.");
                }
            } catch (error) {
                console.error("Error removing friend:", error);
            }
        },
    },
    mounted() {
        this.fetchFriends(); // Fetch friends when the component is mounted
        this.fetchFriendRequests(); // Fetch friend requests when the component is mounted
    },
};
</script>
