<script setup>
import { ref, computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()

// Form States
const form = ref({
  name: '',
  username: '',
  email: '',
  password: '',
  role: 'student', // default selection
  department: '',
  cgpa: '',
  company_name: '',
  hr_contact: '',
  website: '',
  resume_b64: null,
  resume_name: ''
})

const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

// Inline Explicit Validation Messages
const passwordError = ref('')
const usernameMessage = ref('')
const isUsernameAvailable = ref(false)
const emailMessage = ref('')
const isEmailAvailable = ref(false)

// 1. Validate Password Length via @input
const validatePass = () => {
  if (!form.value.password) {
    passwordError.value = ''
    return
  }
  if (form.value.password.length < 6) {
    passwordError.value = 'Password must be at least 6 characters long.'
  } else {
    passwordError.value = 'Password satisfies structural constraints.'
  }
}

// 2. Check Username Availability via @input
const checkUsername = async () => {
  const username = form.value.username.trim()
  if (username.length < 3) {
    usernameMessage.value = ''
    isUsernameAvailable.value = false
    return
  }
  
  try {
    const res = await fetch('http://localhost:5000/uniqueusername', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username })
    })
    const data = await res.json()
    if (data.message === 'available') {
      usernameMessage.value = 'Username is available!'
      isUsernameAvailable.value = true
    } else {
      usernameMessage.value = 'Username is already taken.'
      isUsernameAvailable.value = false
    }
  } catch (err) {
    console.error('Error validating username:', err)
  }
}

// 3. Check Email Availability via @input
const checkEmail = async () => {
  const email = form.value.email.trim()
  if (!email.includes('@')) {
    emailMessage.value = ''
    isEmailAvailable.value = false
    return
  }

  try {
    const res = await fetch('http://localhost:5000/uniquemail', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    })
    const data = await res.json()
    if (data.message === 'available') {
      emailMessage.value = 'Email is available!'
      isEmailAvailable.value = true
    } else {
      emailMessage.value = 'Email is already registered.'
      isEmailAvailable.value = false
    }
  } catch (err) {
    console.error('Error validating email:', err)
  }
}

// 4. Form Submission Guard
const isFormInvalid = computed(() => {
  if (!form.value.name || !form.value.username || !form.value.email || form.value.password.length < 6) return true
  if (!isUsernameAvailable.value || !isEmailAvailable.value) return true
  return false
})

// Handle PDF File Conversion to Base64
const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (file.type !== 'application/pdf') {
    errorMessage.value = 'Please upload a valid PDF file.'
    event.target.value = '' // Reset input field
    return
  }

  form.value.resume_name = file.name

  const reader = new FileReader()
  reader.onload = () => {
    // Extract base64 payload from data URI string
    const base64String = reader.result.split(',')[1]
    form.value.resume_b64 = base64String
    errorMessage.value = ''
  }
  reader.readAsDataURL(file)
}

// Form Submission Method
const handleSubmit = async () => {
  if (isFormInvalid.value) return

  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  const payload = {
    name: form.value.name,
    username: form.value.username,
    email: form.value.email,
    password: form.value.password,
    role: form.value.role
  }

  if (form.value.role === 'student') {
    payload.department = form.value.department
    payload.cgpa = form.value.cgpa
    payload.resume_b64 = form.value.resume_b64
    payload.resume_name = form.value.resume_name
  } else if (form.value.role === 'company') {
    payload.company_name = form.value.company_name
    payload.hr_contact = form.value.hr_contact
    payload.website = form.value.website
  }

  try {
    const response = await fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    const data = await response.json()

    if (!response.ok || data.status === 'error') {
      throw new Error(data.message || 'Registration failed')
    }

    successMessage.value = 'Registration successful! Redirecting to login...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)

  } catch (err) {
    errorMessage.value = err.message
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="container py-2">
    <div class="row justify-content-center">
      <div class="col-12 col-md-8 col-lg-6">
        
        <div class="card shadow-sm border-0">
          <div class="card-body p-4 p-md-5">
              
            <div class="text-center mb-4">
              <h2 class="fw-bold">Create Account</h2>
              <p class="text-muted">Join the placement network today</p>
            </div>

            <!-- Response Alert Messages -->
            <div v-if="errorMessage" class="alert alert-danger" role="alert">
              <i class="fa-solid fa-triangle-exclamation me-2"></i> {{ errorMessage }}
            </div>
            <div v-if="successMessage" class="alert alert-success" role="alert">
              <i class="fa-solid fa-circle-check me-2"></i> {{ successMessage }}
            </div>

            <form @submit.prevent="handleSubmit">                        
              <div class="row g-3 mb-3">
                <div class="col-md-6">
                  <label class="form-label small fw-bold">Full Name</label>
                  <input v-model="form.name" type="text" class="form-control" placeholder="John Doe" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label small fw-bold">Username</label>
                  <input v-model="form.username" @input="checkUsername" type="text" class="form-control" placeholder="johndoe123" required>
                  <div v-if="usernameMessage" :class="isUsernameAvailable ? 'text-success' : 'text-danger'" class="form-text small mt-1 fw-semibold">
                    {{ usernameMessage }}
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label small fw-bold">Email Address</label>
                <input v-model="form.email" @input="checkEmail" type="email" class="form-control" placeholder="name@institute.edu" required>
                <div v-if="emailMessage" :class="isEmailAvailable ? 'text-success' : 'text-danger'" class="form-text small mt-1 fw-semibold">
                  {{ emailMessage }}
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label small fw-bold">Password</label>
                <input v-model="form.password" @input="validatePass" type="password" class="form-control" placeholder="••••••••" required>
                <div v-if="passwordError" :class="form.password.length >= 6 ? 'text-success' : 'text-danger'" class="form-text small mt-1 fw-semibold">
                  {{ passwordError }}
                </div>
              </div>

              <div class="mb-4">
                <label class="form-label small fw-bold">Register As</label>
                <select v-model="form.role" class="form-select">
                  <option value="student">Student</option>
                  <option value="company">Company Representative</option>
                </select>
              </div>

              <hr class="my-4 text-secondary opacity-25">

              <!-- Dynamic Student Fields -->
              <div v-if="form.role === 'student'">
                <div class="row g-3 mb-3">
                  <div class="col-md-6">
                    <label class="form-label small fw-bold">Department</label>
                    <input v-model="form.department" type="text" class="form-control" placeholder="e.g. Computer Science">
                  </div>
                  <div class="col-md-6">
                    <label class="form-label small fw-bold">Current CGPA</label>
                    <input v-model="form.cgpa" type="number" step="0.01" class="form-control" placeholder="0.00">
                  </div>
                </div>
                <div class="mb-4">
                  <label class="form-label small fw-bold">Upload Resume (PDF)</label>
                  <input @change="handleFileChange" type="file" class="form-control" accept=".pdf">
                </div>
              </div>

              <!-- Dynamic Company Fields -->
              <div v-if="form.role === 'company'">
                <div class="mb-3">
                  <label class="form-label small fw-bold">Company Name</label>
                  <input v-model="form.company_name" type="text" class="form-control" placeholder="Tech Corp Inc." :required="form.role === 'company'">
                </div>
                <div class="row g-3 mb-4">
                  <div class="col-md-6">
                    <label class="form-label small fw-bold">HR Contact</label>
                    <input v-model="form.hr_contact" type="text" class="form-control" placeholder="+1234567890">
                  </div>
                  <div class="col-md-6">
                    <label class="form-label small fw-bold">Website URL</label>
                    <input v-model="form.website" type="url" class="form-control" placeholder="https://company.com">
                  </div>
                </div>
              </div>

              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary btn-lg" :disabled="isLoading || isFormInvalid">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  Register Now
                </button>
                <RouterLink to="/login" class="btn btn-link text-decoration-none">Already have an account? Login</RouterLink>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>