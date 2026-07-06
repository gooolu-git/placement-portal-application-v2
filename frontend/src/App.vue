<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue' // We will build this navbar component next
import NotificationToast from '@/components/NotificationToast.vue'
</script>

<template>
  <div style="font-family: 'Inter', sans-serif; background-color: #f8fafc; min-height: 100vh;">
    <!-- Global Dynamic Navbar -->
    <Navbar />
    <NotificationToast/>

    <!-- Main Content Dynamic Placeholder -->
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Global styling rules can reside here */
body {
  margin: 0;
  padding: 0;
}
</style>