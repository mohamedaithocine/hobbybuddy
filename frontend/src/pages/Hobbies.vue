<template>
  <div class="h1">
    {{ title }}
        
  </div>
  
</template>

<script lang="ts">
    import { defineComponent } from "vue";

    export default defineComponent({
        data() {
            return {
                title: "Logged in successfully! Please select an option from the navigation bar.",
            }
        },

    })
</script>

<style scoped>
</style>
