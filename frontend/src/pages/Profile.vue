<template>
  <div class="container mt-5 mb-5">
    <h1 class="mb-4 text-center">{{ title }}</h1>

    <!-- Profile Details Section -->
    <div class="card shadow-lg mb-4">
      <div class="card-header bg-primary text-white">
        Profile Information
      </div>
      <div class="card-body">
        <!-- Editable Profile Fields -->
        <div class="row mb-3">
          <label for="username" class="col-sm-2 col-form-label">Username:</label>
          <div class="col-sm-10">
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="editableProfile.username"
              @input="markAsEdited"
            />
          </div>
        </div>
        <div class="row mb-3">
          <label for="email" class="col-sm-2 col-form-label">Email:</label>
          <div class="col-sm-10">
            <input
              type="email"
              class="form-control"
              id="email"
              v-model="editableProfile.email"
              @input="markAsEdited"
            />
          </div>
        </div>
        <div class="row mb-3">
          <label for="first_name" class="col-sm-2 col-form-label">First Name:</label>
          <div class="col-sm-10">
            <input
              type="text"
              class="form-control"
              id="first_name"
              v-model="editableProfile.first_name"
              @input="markAsEdited"
            />
          </div>
        </div>
        <div class="row mb-3">
          <label for="last_name" class="col-sm-2 col-form-label">Last Name:</label>
          <div class="col-sm-10">
            <input
              type="text"
              class="form-control"
              id="last_name"
              v-model="editableProfile.last_name"
              @input="markAsEdited"
            />
          </div>
        </div>
        <div class="row mb-3">
          <label for="date-of-birth" class="col-sm-2 col-form-label">Date of Birth:</label>
          <div class="col-sm-10">
            <input
              type="date"
              class="form-control"
              id="date-of-birth"
              v-model="editableProfile.date_of_birth"
              @input="markAsEdited"
            />
          </div>
        </div>

        <div class="row mb-3">
          <label for="date-of-birth" class="col-sm-2 col-form-label">Age:</label>
          <div class="col-sm-10">
            <input
              type="text"
              class="form-control"
              id="age"
              :value="age"
              readonly
            />
          </div>
        </div>

        <div class="row mb-3">
          <!-- Error Message -->
          <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
          </div>
        </div>

        <div class="row mb-3">
          <div v-if="successMessage && !isEdited" class="alert alert-success" role="alert">
            {{ successMessage }}
          </div>
        </div>

        <!-- Done Button -->
        <div v-if="isEdited" class="text-end mt-3">
          <button
            class="btn btn-success"
            @click="saveChanges"
          >
            Done
          </button>
        </div>
      </div>
    </div>

     <!-- Change Password Section -->
     <div class="card shadow-lg mt-4 mb-4">
      <div class="card-header bg-warning text-dark">
        Change Password
      </div>
      <div class="card-body">
        <div class="row mb-3">
          <label for="current-password" class="col-sm-2 col-form-label">Current Password:</label>
          <div class="col-sm-10">
            <input
              type="password"
              class="form-control"
              id="current-password"
              v-model="currentPassword"
            />
          </div>
        </div>
        <div class="row mb-3">
          <label for="new-password" class="col-sm-2 col-form-label">New Password:</label>
          <div class="col-sm-10">
            <input
              type="password"
              class="form-control"
              id="new-password"
              v-model="newPassword"
            />
          </div>
        </div>
        <div class="row mb-3">
          <label for="confirm-password" class="col-sm-2 col-form-label">Confirm Password:</label>
          <div class="col-sm-10">
            <input
              type="password"
              class="form-control"
              id="confirm-password"
              v-model="confirmPassword"
            />
          </div>
        </div>
        <div class="text-end">
          <button
            class="btn btn-success"
            @click="changePassword"
          >
            Update Password
          </button>
        </div>
        <div class="row mb-3">
          <!-- Error Message -->
          <div v-if="errorPassword" class="alert alert-danger" role="alert">
            {{ errorPassword }}
          </div>
        </div>
        <div class="row mb-3">
          <div v-if="successPassword" class="alert alert-success" role="alert">
            {{ successPassword }}
          </div>
        </div>
      </div>
    </div>


    <!-- Hobbies Section -->
    <div class="card shadow-lg">
      <div class="card-header bg-secondary text-white">
        Manage Hobbies
      </div>
      <div class="card-body">
        <!-- List of Current Hobbies -->
        <ul class="list-group mb-3">
          <li
            v-for="(hobby, index) in editableProfile.hobbies"
            :key="index"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            {{ hobby }}
            <button
              class="btn btn-danger btn-sm"
              @click="removeHobby(hobby, index)"
            >
              Remove
            </button>
          </li>
        </ul>

        <!-- Add Hobby Section -->
        <div class="mb-3">
          <label for="predefined-hobbies" class="form-label">Add a Hobby:</label>
          <div class="input-group">
            <!-- Dropdown for Predefined Hobbies -->
            <select v-model="selectedHobby" class="form-select" id="predefined-hobbies">
              <option value="">Select a predefined hobby...</option>
              <option v-for="hobby in filteredHobbies" :key="hobby" :value="hobby">
                {{ hobby }}
              </option>
            </select>
            <!-- Input for New Hobby -->
            <input
              type="text"
              v-if="selectedHobby === ''"
              v-model="newHobby"
              class="form-control"
              placeholder="Or type a new hobby"
            />
            <button class="btn btn-primary" @click="addHobby">
              Add Hobby
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted, computed } from "vue";
import { useUserStore } from "../stores/user";
import { useCsrfStore } from "../stores/csrf";
import { checkLoginStatus } from "../utils/auth";


export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const csrfStore = useCsrfStore();


    const errorMessage = ref(""); // Error message for failed requests
    const successMessage = ref(""); // Success message for successful requests
    const successPassword = ref("");
    const errorPassword = ref("");

    // Reactive state for editable profile and flags

    const editableProfile = reactive({ 
      id: Number(userStore.profile?.id) || 0, 
      username: userStore.profile?.username || "", 
      email: userStore.profile?.email || "", 
      first_name: userStore.profile?.first_name || "", 
      last_name: userStore.profile?.last_name || "", 
      date_of_birth: userStore.profile?.date_of_birth || "", 
      hobbies: userStore.profile?.hobbies || [] 
    });
    const isEdited = ref(false);

    // Hobbies
    const predefinedHobbies = ref<string[]>([]); // Reactive list of predefined hobbies
    const selectedHobby = ref("");
    const newHobby = ref("");


    const age = computed(() => {
      if (editableProfile.date_of_birth) {
        const dob = new Date(editableProfile.date_of_birth);
        const today = new Date();
        let calculatedAge = today.getFullYear() - dob.getFullYear();
        const monthDifference = today.getMonth() - dob.getMonth();
        if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < dob.getDate())) {
          calculatedAge--;
        }
        return calculatedAge;
      }
      return 0; // Default if no date of birth
    });

    // Change Password fields
    const currentPassword = ref("");
    const newPassword = ref("");
    const confirmPassword = ref("");

    const markAsEdited = () => {
      isEdited.value = true; // Set isEdited flag when any field is modified
    };

    const saveChanges = async () => {
      if (editableProfile.date_of_birth) {
        editableProfile.date_of_birth = new Date(editableProfile.date_of_birth).toISOString().split("T")[0];;
      }
      // check editableProfile email is in a valid format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!editableProfile.email || !emailRegex.test(editableProfile.email)) {
        setTimeout(() => {
          errorMessage.value = "";
        }, 3000);
        errorMessage.value = "Please enter a valid email address";
        return;
      }

      if (editableProfile.username === "" || editableProfile.email === "" || editableProfile.first_name === "" || editableProfile.last_name === "" || editableProfile.date_of_birth === "") {
        errorMessage.value = "Please fill in all required fields";
        setTimeout(() => {
          errorMessage.value = "";
        }, 3000);
        return;
      }

      // Save changes to the Pinia store
      const response = await fetch(`/edituser/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfStore.csrfToken, // Use the token from the store
        },
        body: JSON.stringify(editableProfile),
      });
      if (response.ok) {
        userStore.setUser({ ...editableProfile, id: Number(editableProfile.id), age: age.value });
        errorMessage.value = ""; // Clear any previous error message
        successMessage.value = "Profile successfully updated";

        setTimeout(() => {
          successMessage.value = "";
        }, 3000);

        isEdited.value = false; // Reset edit flag
      }
      else {
        const errorData = await response.json();
        errorMessage.value = errorData.error

        setTimeout(() => {
          errorMessage.value = "";
        }, 3000);
      }
    };

    const changePassword = async () => {
      if (newPassword.value !== confirmPassword.value) {
        alert("Passwords do not match");
        return;
      }
      const response = await fetch("/changepassword/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfStore.csrfToken,
        },
        body: JSON.stringify({
          id: userStore.profile?.id || 0,
          current_password: currentPassword.value,
          new_password: newPassword.value,
        }),
      });
      if (response.ok) {
        checkLoginStatus(); // Refresh login status
        csrfStore.updateCsrfToken(); // Refresh CSRF token
        console.log(userStore.profile);
        successPassword.value = "Password successfully updated";

        setTimeout(() => {
          successPassword.value = "";
        }, 3000);

        currentPassword.value = "";
        newPassword.value = "";
        confirmPassword.value = "";
      } else {
        errorPassword.value = "Failed to update password. Please try again.";

        setTimeout(() => {
          errorPassword.value = "";
        }, 3000);
      }
    };

    const addHobby = async () => {
      const hobbyToAdd =
        selectedHobby.value === "" ? newHobby.value.trim() : selectedHobby.value;

      if (hobbyToAdd && !editableProfile.hobbies.includes(hobbyToAdd)) {
        try {
          const response = await fetch("/addhobby/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfStore.csrfToken, // Use the token from the store
            },
            body: JSON.stringify({ hobby: hobbyToAdd, user_id: editableProfile.id }),
          });

          if (response.ok) {
            const data = await response.json();
            editableProfile.hobbies.push(data.hobby); // Update UI with new hobby
            selectedHobby.value = "";
            newHobby.value = "";
          } else {
            console.error("Failed to add hobby:", response.statusText);
          }
        } catch (error) {
          console.error("An error occurred while adding the hobby:", error);
        }
      }
    };

    const removeHobby = async (hobby: string, index: number) => {
      const csrfStore = useCsrfStore();
      const response = await fetch("/addhobby/", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfStore.csrfToken, // Use the token from the store
        },
        body: JSON.stringify({ hobby: hobby, user_id: editableProfile.id }),
      });

      if (response.ok){
        editableProfile.hobbies.splice(index, 1);
      }
    };

    // Fetch predefined hobbies from the server
    const fetchPredefinedHobbies = async () => {
      try {
        const response = await fetch("/hobbies/");
        const data = await response.json();
        predefinedHobbies.value = data.hobbies; // Update reactive predefinedHobbies
      } catch (error) {
        console.error("Failed to fetch predefined hobbies:", error);
      }
    };

    // Filter predefined hobbies to exclude those the user is already subscribed to
    const filteredHobbies = computed(() => {
      // if editableProfile.hobbies is undefined, return all predefined hobbies
      try {
        return predefinedHobbies.value.filter(
          (hobby) => !editableProfile.hobbies.includes(hobby)
        );
      } catch (error) {
        return predefinedHobbies.value;
      }
    });

    // Fetch predefined hobbies on mount
    onMounted(fetchPredefinedHobbies);

    return {
      editableProfile,
      isEdited,
      age,
      filteredHobbies, // Use this for display
      selectedHobby,
      newHobby,
      addHobby,
      removeHobby,
      markAsEdited,
      saveChanges,
      currentPassword,
      newPassword,
      confirmPassword,
      changePassword,
      errorMessage,
      successMessage,
      successPassword,
      errorPassword,
      title: "Profile Page",
    };
  },
});
</script>
