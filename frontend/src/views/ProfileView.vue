<template>
  <div class="container py-5 mt-2 bg-light min-vh-100">
    <div class="row justify-content-center">
      <div class="col-lg-7 col-md-9">
        <div class="card border-0 shadow-sm rounded-4 overflow-hidden bg-white">
          
          <!-- Header -->
          <div class="card-header border-0 bg-light p-4">
            <div class="d-flex align-items-center gap-4">
              <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${form.name}`" 
                   class="rounded-circle border border-3 border-white shadow-sm" width="85" height="85">
              <div>
                <h4 class="fw-bold text-dark mb-1">{{ form.name }}</h4>
                <span class="badge bg-primary-subtle text-primary rounded-pill px-3 text-uppercase" style="font-size: 0.65rem;">
                  {{ authStore.userRole }}
                </span>
              </div>
            </div>
          </div>

          <div class="card-body p-4 p-md-5">
            <form @submit.prevent="updateProfile">
              <div class="row g-4">
                
                <!-- Personal Info -->
                <div class="col-12">
                  <h6 class="fw-bold text-uppercase text-secondary mb-3" style="font-size: 0.75rem;">Personal Information</h6>
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label small fw-bold text-muted">Full Name</label>
                      <input v-model="form.name" type="text" class="form-control bg-light border-0 py-2" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label small fw-bold text-muted">Current Resume</label>
                      <a v-if="form.current_resume" :href="form.current_resume" target="_blank" 
                         class="btn btn-outline-primary w-100 py-2 d-flex align-items-center justify-content-center gap-2">
                        <i class="fas fa-file-pdf"></i> View Resume
                      </a>
                      <div v-else class="p-2 border rounded text-muted small text-center">No resume linked</div>
                    </div>
                  </div>
                </div>

                <!-- Resume Update Section -->
                <div v-if="authStore.userRole === 'student'" class="col-12">
                  <label class="form-label small fw-bold text-muted">Update Resume Link (Google Drive)</label>
                  <input v-model="form.resume_link" type="text" class="form-control bg-light border-0 py-2" placeholder="Paste new link here...">
                  <small class="text-muted">Leave empty to keep your existing resume.</small>
                </div>

                <!-- Security -->
                <div class="col-12">
                  <h6 class="fw-bold text-uppercase text-secondary mb-3 mt-2" style="font-size: 0.75rem;">Security & Access</h6>
                  <div class="row g-3 p-3 border rounded-4 border-danger-subtle bg-danger-subtle bg-opacity-10">
                    <div class="col-md-6">
                      <label class="form-label small fw-bold text-muted">New Password</label>
                      <input v-model="form.npassword" type="password" class="form-control bg-white py-2" placeholder="••••••••">
                    </div>
                    <div class="col-md-6">
                      <label class="form-label small fw-bold text-danger">Confirm Identity (Current Password)*</label>
                      <input v-model="form.cpassword" type="password" class="form-control bg-white border-danger py-2" required>
                    </div>
                  </div>
                </div>

                <!-- Footer -->
                <div class="col-12 mt-4">
                  <button type="submit" :disabled="isLoading" class="btn btn-primary rounded-pill px-5 py-2 fw-bold shadow">
                    {{ isLoading ? 'Saving...' : 'Save Profile Changes' }}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const isLoading = ref(false)

const form = reactive({
  name: '',
  username: '',
  npassword: '',
  cpassword: '',
  resume_link: '',
  current_resume: ''
})

const fetchProfile = async () => {
  try {
    const res = await axios.get('http://localhost:5000/profile', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    form.name = res.data.name
    form.username = res.data.username
    form.current_resume = res.data.resume || ''
  } catch (err) {
    console.error("Failed to fetch profile", err)
  }
}

const updateProfile = async () => {
  isLoading.value = true
  try {
    // Build payload
    const payload = {
      name: form.name,
      cpassword: form.cpassword,
      ...(form.npassword && { npassword: form.npassword })
    }

    // Only add resume_link if the user actually typed something
    if (form.resume_link && form.resume_link.trim() !== '') {
      payload.resume_link = form.resume_link
    }
    
    await axios.put('http://localhost:5000/profile', payload, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    
    alert('Profile updated successfully!')
    form.resume_link = '' // Clear input
    fetchProfile() // Refresh data
  } catch (err) {
    alert(err.response?.data?.message || 'Update failed')
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchProfile)
</script>