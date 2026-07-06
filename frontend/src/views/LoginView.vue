<script setup>
import { ref, computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast' // Added toast utility

const router = useRouter()
const authStore = useAuthStore()

// Form Input States
const username = ref('')
const password = ref('')

// Feedback States
const passwordError = ref('')
const isLoading = ref(false)

// Explicit @input handler for password validation
const validatePass = () => {
  if (!password.value) {
    passwordError.value = ''
    return
  }
  if (password.value.length < 6) {
    passwordError.value = 'Password must be at least 6 characters long.'
  } else {
    passwordError.value = ''
  }
}

// Disable login button if constraints aren't met
const isFormInvalid = computed(() => {
  return !username.value || !password.value || password.value.length < 6
})

// Handle Login Submission
const handleLogin = async () => {
  if (isFormInvalid.value) return

  isLoading.value = true

  try {
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (!response.ok || data.status === 'error') {
      throw new Error(data.message || 'Invalid username or password')
    }

    // Trigger global success toast
    toast.success('Login Successful', 'Redirecting to your dashboard...')
    
    // Commit to Pinia store (saves token and profile object globally)
    authStore.login(data.user, data.token)

    // Dynamic redirection based on user role
    setTimeout(() => {
      if (data.user.role === 'admin') {
        router.push('/admin/dashboard')
      } else if (data.user.role === 'company') {
        router.push('/company/dashboard')
      } else {
        router.push('/student/dashboard')
      }
    }, 1500)

  } catch (err) {
    // Trigger global error toast
    toast.error('Login Failed', err.message)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="container py-5">
    <!-- Back to Home Link -->
    <div class="row justify-content-center mb-4">
      <div class="col-12 col-md-8 mt-5 col-lg-5">
        <RouterLink to="/" class="text-decoration-none small fw-bold ">
          &larr; Back to Home
        </RouterLink>
      </div>
    </div>

    <div class="row justify-content-center">
      <div class="col-12 col-md-8 col-lg-5">
        
        <div class="card shadow-sm border-0">
          <div class="card-body p-4 p-md-5">
              
            <div class="text-center mb-4">
              <h2 class="fw-bold">Welcome Back</h2>
              <p class="text-muted small">Please enter your credentials to continue</p>
            </div>

            <!-- Removed original local alert tags so the background doesn't jump -->

            <form @submit.prevent="handleLogin">
              <!-- Username input -->
              <div class="mb-3">
                <label class="form-label small fw-bold text-secondary">Username</label>
                <input v-model="username" type="text" class="form-control form-control-lg" placeholder="Enter username" required>
              </div>

              <!-- Password input with length validator -->
              <div class="mb-4">
                <div class="d-flex justify-content-between">
                  <label class="form-label small fw-bold text-secondary">Password</label>
                  <a href="#" class="small text-decoration-none">Forgot?</a>
                </div>
                <input v-model="password" @input="validatePass" type="password" class="form-control form-control-lg" placeholder="••••••••" required>
                <div v-if="passwordError" class="text-danger form-text small mt-1 fw-semibold">
                  {{ passwordError }}
                </div>
              </div>

              <!-- Action button -->
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary btn-lg fw-bold" :disabled="isLoading || isFormInvalid">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  Sign In
                </button>
              </div>
            </form>

            <!-- Bottom Redirect Link -->
            <div class="text-center mt-4">
              <p class="small text-muted mb-0">
                Don't have an account? 
                <RouterLink to="/register" class="text-primary fw-bold text-decoration-none">Create Account</RouterLink>
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>