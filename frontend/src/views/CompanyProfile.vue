<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const company = ref(null)
const isLoading = ref(true)

const fetchDetails = async () => {
  isLoading.value = true
  try {
    const res = await fetch(`http://localhost:5000/admin/company/${route.params.id}`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const json = await res.json()
    if (json.status === 'success') {
      company.value = json.data
    }
  } catch (err) {
    toast.error('Error', 'Failed to load profile')
  } finally {
    isLoading.value = false
  }
}

// Stats Calculation for Engagement Card
const totalSelections = computed(() => {
  if (!company.value?.drives) return 0
  return company.value.drives.reduce((acc, d) => {
    return acc + (d.applications?.filter(a => a.status === 'Selected').length || 0)
  }, 0)
})

const updateProfile = async () => {
  // Add your API call here for POST /admin/update_profile/<id>
  toast.success('Success', 'Profile updated.')
}

const toggleBlacklist = async () => {
  // Add your API call here for POST /admin/blacklist_company/<id>
  toast.success('Status', 'Partner status updated.')
  fetchDetails()
}

onMounted(fetchDetails)
</script>

<template>
  <div v-if="isLoading" class="text-center py-5">Loading...</div>
  <div v-else-if="company" class="container py-4 mt-2 bg-light mt-5">
    <div class="row g-4">
      <!-- Left Column -->
      <div class="col-lg-8">
        <!-- Partner Overview -->
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4 bg-white">
          <div class="d-flex justify-content-between align-items-start mb-4 border-start border-primary border-4 ps-3">
            <h5 class="fw-bold text-dark mb-0">Partner Overview</h5>
            <div class="text-muted fw-bold text-uppercase" style="font-size: 0.7rem; letter-spacing: 0.05em;">Company Profile</div>
          </div>
          <div class="row align-items-center">
            <div class="col-md-3 text-center">
              <img :src="`https://api.dicebear.com/7.x/identicon/svg?seed=${company.company_profile?.company_name}`" class="rounded-circle border border-3 p-1 bg-white shadow-sm" width="110">
            </div>
            <div class="col-md-9">
              <h4 class="fw-bold text-dark mb-1">{{ company.company_profile?.company_name || company.name }}</h4>
              <div class="d-flex flex-wrap gap-3 mb-3 text-muted small">
                <span><i class="fas fa-hashtag me-1 text-primary"></i> ID: {{ company.id }}</span>
                <span><i class="fas fa-user-tie me-1 text-primary"></i> HR: {{ company.company_profile?.hr_contact || 'N/A' }}</span>
              </div>
              <div class="d-flex align-items-center gap-3">
                <a v-if="company.company_profile?.website" :href="company.company_profile.website" target="_blank" class="btn btn-sm btn-light border rounded-pill px-3 fw-bold text-primary">
                  <i class="fas fa-external-link-alt me-1"></i> Visit Website
                </a>
                <span class="fw-bold px-3 py-1 rounded-pill border small" 
                      :class="company.is_blacklisted ? 'bg-danger-subtle text-danger border-danger-subtle' : 
                              company.is_approved ? 'bg-success-subtle text-success border-success-subtle' : 'bg-warning-subtle text-warning border-warning-subtle'">
                  <i class="fas me-1" :class="company.is_blacklisted ? 'fa-ban' : company.is_approved ? 'fa-check-circle' : 'fa-clock'"></i>
                  {{ company.is_blacklisted ? 'Blacklisted' : company.is_approved ? 'Verified Partner' : 'Pending Approval' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Drives Table -->
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
          <div class="d-flex justify-content-between align-items-center mb-4 border-start border-primary border-4 ps-3">
            <h5 class="fw-bold text-dark mb-0">Recruitment Drives</h5>
            <span class="badge bg-primary-subtle text-primary rounded-pill px-3">{{ company.drives?.length || 0 }} Total Drives</span>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr class="text-uppercase text-secondary" style="font-size: 0.7rem;">
                  <th class="py-3 px-3">Job Title</th>
                  <th class="py-3">Deadline</th>
                  <th class="py-3">Status</th>
                  <th class="text-center py-3">Applicants</th>
                  <th class="text-end py-3 px-3">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="drive in company.drives" :key="drive.id" class="border-bottom">
                  <td class="py-3 px-3">
                    <div class="fw-bold text-dark">{{ drive.job_title }}</div>
                  </td>
                  <td>{{ drive.deadline }}</td>
                  <td><span class="badge bg-primary-subtle text-primary">{{ drive.status }}</span></td>
                  <td class="text-center">{{ drive.applications?.length || 0 }}</td>
                  <td class="text-end px-3">
                    <router-link :to="`/admin/drive/${drive.id}`" class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-bold">Manage</router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="col-lg-4">
        <!-- Stats Card -->
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4 bg-white text-center">
          <h6 class="fw-bold text-dark mb-4 text-uppercase" style="font-size: 0.75rem;">Engagement Stats</h6>
          <div class="row g-3">
            <div class="col-6">
              <div class="p-3 bg-light rounded-4 border">
                <div class="h3 fw-bold text-primary mb-0">{{ company.drives?.length || 0 }}</div>
                <small class="text-muted fw-bold" style="font-size: 0.6rem;">POSTINGS</small>
              </div>
            </div>
            <div class="col-6">
              <div class="p-3 bg-light rounded-4 border">
                <div class="h3 fw-bold text-success mb-0">{{ totalSelections }}</div>
                <small class="text-muted fw-bold" style="font-size: 0.6rem;">SELECTIONS</small>
              </div>
            </div>
          </div>
        </div>

        <!-- Admin Controls -->
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
          <h6 class="fw-bold text-dark mb-4 text-uppercase"><i class="fas fa-user-shield me-2 text-primary"></i>Admin Controls</h6>
          <form @submit.prevent="updateProfile">
            <div class="mb-3">
              <label class="small fw-bold text-secondary">Company Legal Name</label>
              <input v-model="company.company_profile.company_name" class="form-control bg-light border-0 py-2">
            </div>
            <div class="mb-3">
              <label class="small fw-bold text-secondary">HR Contact Person</label>
              <input v-model="company.company_profile.hr_contact" class="form-control bg-light border-0 py-2">
            </div>
            <div class="mb-3">
              <label class="small fw-bold text-danger">Reset Password</label>
              <input type="password" class="form-control bg-light border-0 py-2" placeholder="Keep blank to skip">
            </div>
            <button class="btn btn-primary w-100 rounded-pill fw-bold">Update Records</button>
          </form>
          <div class="mt-3 border-top pt-3">
            <button @click="toggleBlacklist" class="btn w-100 rounded-pill fw-bold" :class="company.is_blacklisted ? 'btn-outline-success' : 'btn-outline-danger'">
              {{ company.is_blacklisted ? 'Unblock Partner' : 'Block Partner' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="text-center mt-4">
      <router-link to="/admin/dashboard" class="btn btn-sm btn-outline-secondary rounded-pill px-5 fw-bold">Return to Directory</router-link>
    </div>
  </div>
</template>