<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const user = ref(null)
const newPassword = ref('')
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

const updateProfile = async () => {
  try {
    const payload = {
      name: user.value.name,
      username: user.value.username,
      department: user.value.student_profile.department,
      cgpa: user.value.student_profile.cgpa
    }
    if (newPassword.value) payload.new_password = newPassword.value

    const res = await fetch(`http://localhost:5000/admin/edit_user/${user.value.id}`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (res.ok) {
      toast.success('Success', 'Profile updated successfully.')
      newPassword.value = ''
    }
  } catch (err) { toast.error('Error', 'Update failed.') }
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
    const res = await fetch(`http://localhost:5000/admin/blacklist/${user.value.id}`, {
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
  <div v-else-if="user" class="container py-4 mt-5 bg-light ">
    <div class="row g-4">
      <!-- Left Column -->
      <div class="col-lg-8">
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4 bg-white">
          <div class="d-flex justify-content-between align-items-start mb-4 border-start border-primary border-4 ps-3">
            <h5 class="fw-bold text-dark mb-0">Student Overview</h5>
            <div class="text-muted fw-bold text-uppercase" style="font-size: 0.7rem; letter-spacing: 0.05em;">Academic Profile</div>
          </div>
          <div class="row align-items-center">
            <div class="col-md-3 text-center text-md-start mb-3 mb-md-0">
              <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.username}`" class="rounded-circle border border-3 p-1 bg-white shadow-sm" width="110">
            </div>
            <div class="col-md-9">
              <div class="d-flex justify-content-between flex-wrap gap-2">
                <div>
                  <h4 class="fw-bold text-dark mb-1">{{ user.name }}</h4>
                  <div class="d-flex flex-wrap gap-3 mb-3 text-muted small">
                    <span><i class="fas fa-id-card me-1 text-primary"></i> ID: {{ user.id }}</span>
                    <span><i class="fas fa-graduation-cap me-1 text-primary"></i> {{ user.student_profile?.department || 'N/A' }}</span>
                  </div>
                </div>
                <a v-if="user.student_profile?.resume" :href="`/uploads/${user.student_profile.resume}`" target="_blank" class="btn btn-sm btn-outline-dark rounded-pill px-3 fw-bold shadow-sm">
                  <i class="fas fa-file-pdf me-2 text-danger"></i>View Resume
                </a>
              </div>
              <div class="d-flex align-items-center gap-3">
                <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 rounded-pill fw-bold">
                  <i class="fas fa-chart-line me-1"></i> CGPA: {{ user.student_profile?.cgpa || '0.00' }}
                </span>
                <span class="fw-bold px-3 py-1 rounded-pill border small" :class="user.is_blacklisted ? 'bg-danger-subtle text-danger border-danger-subtle' : user.is_approved ? 'bg-success-subtle text-success border-success-subtle' : 'bg-warning-subtle text-warning border-warning-subtle'">
                  <i class="fas me-1" :class="user.is_blacklisted ? 'fa-ban' : user.is_approved ? 'fa-check-circle' : 'fa-clock'"></i>
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
            <span class="badge bg-light text-dark border rounded-pill px-3">{{ user.student_profile?.applications?.length || 0 }} Drives</span>
          </div>
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light text-uppercase text-secondary" style="font-size: 0.7rem;">
              <tr><th class="py-3 px-3">Job Title & Company</th><th>Date Applied</th><th>Status</th><th class="text-end px-3">Action</th></tr>
            </thead>
            <tbody>
              <tr v-for="app in user.student_profile?.applications" :key="app.id" class="border-bottom">
                <td class="py-3 px-3">
                  <div class="fw-bold text-dark">{{ app.target_drive?.job_title }}</div>
                  <div class="text-muted small">{{ app.target_drive?.company_name }}</div>
                </td>
                <td>{{ new Date(app.applied_on).toLocaleDateString() }}</td>
                <td><span class="badge bg-info-subtle text-info border border-info-subtle">{{ app.status }}</span></td>
                <td class="text-end px-3"><router-link :to="`/admin/drive/${app.drive_id}`" class="btn btn-sm btn-outline-primary rounded-pill px-3">Drive Info</router-link></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
          <h6 class="fw-bold text-dark mb-4 text-uppercase" style="font-size: 0.75rem;"><i class="fas fa-user-shield me-2 text-primary"></i>Admin Controls</h6>
          <form @submit.prevent="updateProfile">
            <div class="mb-3"><label class="small fw-bold text-secondary">Full Name</label><input v-model="user.name" class="form-control bg-light border-0 py-2 shadow-none" required></div>
            <div class="mb-3"><label class="small fw-bold text-secondary">Username</label><input v-model="user.username" class="form-control bg-light border-0 py-2 shadow-none" required></div>
            <div class="row g-2 mb-3">
              <div class="col-7"><label class="small fw-bold text-secondary">Dept</label><input v-model="user.student_profile.department" class="form-control bg-light border-0 py-2 shadow-none"></div>
              <div class="col-5"><label class="small fw-bold text-secondary">CGPA</label><input type="number" step="0.01" v-model="user.student_profile.cgpa" class="form-control bg-light border-0 py-2 shadow-none"></div>
            </div>
            <div class="mb-4"><label class="small fw-bold text-danger">Reset Password</label><input type="password" v-model="newPassword" class="form-control bg-light border-0 py-2 shadow-none" placeholder="Leave blank to skip"></div>
            <button class="btn btn-primary w-100 rounded-pill fw-bold py-2 shadow-sm"><i class="fas fa-save me-2"></i> Save Changes</button>
          </form>
          <div class="pt-3 border-top mt-2 d-flex gap-2">
            <button v-if="!user.is_approved && !user.is_blacklisted" @click="approveUser" class="btn btn-outline-success border-2 btn-sm w-100 rounded-pill fw-bold">Verify</button>
            <button @click="toggleBlacklist" class="btn border-2 btn-sm w-100 rounded-pill fw-bold" :class="user.is_blacklisted ? 'btn-outline-success' : 'btn-outline-danger'">
              {{ user.is_blacklisted ? 'Unblock' : 'Blacklist' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="text-center mt-4"><router-link to="/admin/dashboard" class="btn btn-sm btn-outline-secondary rounded-pill px-5 fw-bold"><i class="fas fa-arrow-left me-2"></i> Return to Admin Console</router-link></div>
  </div>
</template>