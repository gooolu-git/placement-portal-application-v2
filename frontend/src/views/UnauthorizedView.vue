<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleGoHome = () => {
  // If not logged in, take them to login page
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  // If logged in, safely redirect to their matching dashboard role
  if (authStore.userRole === 'admin') {
    router.push('/admin/dashboard')
  } else if (authStore.userRole === 'company') {
    router.push('/company/dashboard')
  } else {
    router.push('/student/dashboard')
  }
}
</script>

<template>
  <div class="container py-5 text-center">
    <div class="row justify-content-center align-items-center" style="min-height: 70vh;">
      <div class="col-12 col-md-6 col-lg-5">
        
        <!-- Warning Icon -->
        <div class="mb-4">
          <i class="fa-solid fa-triangle-exclamation text-warning display-1"></i>
        </div>

        <!-- Error Messages -->
        <h1 class="fw-bold text-dark mb-2">403 - Access Denied</h1>
        <p class="text-muted mb-4">
          Oops! You don't have the permission clearance required to view this dashboard page.
        </p>

        <!-- Redirect CTA Action Button -->
        <div class="d-grid gap-2 col-8 mx-auto">
          <button @click="handleGoHome" class="btn btn-primary btn-lg fw-bold shadow-sm">
            Return to My Workspace
          </button>
        </div>

      </div>
    </div>
  </div>
</template>