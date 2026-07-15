<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const user = ref(null)
const isLoading = ref(true)

const fetchStudent = async () => {
  isLoading.value = true
  try {
    const res = await fetch(`http://localhost:5000/admin/student/${route.params.id}`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const json = await res.json()
    if (json.status === 'success') user.value = json.data
  } catch (err) {
    toast.error('Error', 'Failed to load profile')
  } finally {
    isLoading.value = false
  }
}



const approveUser = async () => {
  try {
    const res = await fetch(`http://localhost:5000/admin/approve/${user.value.id}`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_approved: true })
    })
    if (res.ok) { toast.success('Success', 'User verified.'); fetchStudent(); }
  } catch (err) { toast.error('Error', 'Action failed.') }
}

const toggleBlacklist = async () => {
  try {
    const res = await fetch(`http://localhost:5000/admin/block/${user.value.id}`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_blocked: !user.value.is_blacklisted })
    })
    if (res.ok) { toast.success('Status', 'Blacklist status updated.'); fetchStudent(); }
  } catch (err) { toast.error('Error', 'Action failed.') }
}

onMounted(fetchStudent)
</script>

<template>
  <div v-if="isLoading" class="text-center py-5">Loading...</div>

  <!-- Centered container -->
  <div v-else-if="user" class="container py-4 mt-5 d-flex justify-content-center">
    <div class="row g-4 w-100 justify-content-center">
      <div class="col-lg-8">
        <!-- Student Overview -->
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4 bg-white">
          <div class="d-flex justify-content-between align-items-start mb-4 border-start border-primary border-4 ps-3">
            <h5 class="fw-bold text-dark mb-0">Student Overview</h5>
            <!-- Action Buttons Added Here -->
            <div class="d-flex flex-column gap-2">
              <div class="d-flex gap-1">
                <button v-if="!user.is_approved" @click="approveUser"
                  class="btn btn-sm btn-success rounded-pill px-3">Verify User</button>
                <button @click="toggleBlacklist"
                  :class="user.is_blacklisted ? 'btn-outline-success' : 'btn-outline-danger'"
                  class="btn btn-sm rounded-pill px-3">
                  {{ user.is_blacklisted ? 'Unblock User' : 'Blacklist User' }}
                </button>
              </div>

              <!-- View Resume Button -->
              <a v-if="user.student_profile?.resume" :href="user.student_profile.resume" target="_blank"
                class="btn btn-sm btn-outline-secondary rounded-pill px-3">
                <i class="fas fa-file-alt me-2"></i>View Resume
              </a>
            </div>
          </div>

          <div class="row align-items-center">
            <div class="col-md-3 text-center text-md-start mb-3 mb-md-0">
              <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.username}`"
                class="rounded-circle border border-3 p-1 bg-white shadow-sm" width="110">
            </div>
            <div class="col-md-9">
              <h4 class="fw-bold text-dark mb-1">{{ user.name }}</h4>
              <div class="d-flex flex-wrap gap-3 mb-3 text-muted small">
                <span><i class="fas fa-id-card me-1 text-primary"></i> ID: {{ user.id }}</span>
                <span><i class="fas fa-graduation-cap me-1 text-primary"></i> {{ user.student_profile?.department ||
                  'N/A' }}</span>
              </div>
              <div class="d-flex align-items-center gap-3">
                <span class="badge bg-primary-subtle text-primary border px-3 py-2 rounded-pill fw-bold">
                  CGPA: {{ user.student_profile?.cgpa || '0.00' }}
                </span>
                <span class="fw-bold px-3 py-1 rounded-pill border small"
                  :class="user.is_blacklisted ? 'bg-danger-subtle text-danger' : user.is_approved ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'">
                  {{ user.is_blacklisted ? 'Blocked' : user.is_approved ? 'Verified' : 'Pending' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Applications Table -->
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
          <div class="d-flex justify-content-between mb-4 border-start border-primary border-4 ps-3">
            <h5 class="fw-bold text-dark mb-0">Application History</h5>
          </div>
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-uppercase text-secondary" style="font-size: 0.7rem;">
              <tr>
                <th>Job Title</th>
                <th>Date</th>
                <th>Status</th>
                <th class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in user.student_profile?.applications" :key="app.id">
                <td>
                  <div class="fw-bold">{{ app.target_drive?.job_title }}</div>
                  <div class="text-muted small">{{ app.target_drive?.company_name }}</div>
                </td>
                <td>{{ new Date(app.applied_on).toLocaleDateString() }}</td>
                <td><span class="badge bg-info-subtle text-info">{{ app.status }}</span></td>
                <td class="text-end"><router-link :to="`/admin/drive/${app.drive_id}`"
                    class="btn btn-sm btn-outline-primary rounded-pill">Info</router-link></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="text-center mt-4">
          <router-link to="/admin/dashboard" class="btn btn-sm btn-outline-secondary rounded-pill px-5">Back to
            Console</router-link>
        </div>
      </div>
    </div>
  </div>
</template>