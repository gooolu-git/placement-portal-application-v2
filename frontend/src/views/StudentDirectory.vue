<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const authStore = useAuthStore()
const students = ref([])
const searchQuery = ref('')
const isLoading = ref(true)

const fetchStudents = async () => {
  isLoading.value = true
  try {
    const res = await fetch('http://localhost:5000/admin/users', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const response = await res.json()
    if (response.status === 'success') {
      students.value = response.data.filter(u => u.role === 'student')
    }
  } catch (err) {
    toast.error('Error', 'Could not load records.')
  } finally {
    isLoading.value = false
  }
}

// Mirroring the 'blacklist_user' POST logic from your Jinja
const toggleBlockStatus = async (user_id, status) => {
  try {
    const res = await fetch(`http://localhost:5000/admin/block/${user_id}`, {
      method: 'PATCH',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}` 
      },
      body: JSON.stringify({ is_blocked: status })
    })
    if (res.ok) {
      toast.success('Success', 'Status updated.')
      fetchStudents()
    }
  } catch (err) {
    toast.error('Error', 'Operation failed.')
  }
}

const filteredStudents = computed(() => {
  return students.value.filter(u => 
    u.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    u.id.toString().includes(searchQuery.value) ||
    u.student_profile?.department?.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

onMounted(fetchStudents)
</script>

<template>
  <div class="container py-4 mt-5 bg-light">
    <!-- Header with Search -->
    <div class="row g-4 mb-4 align-items-center">
      <div class="col-lg-7">
        <div class="border-start border-primary border-4 ps-3">
          <h2 class="fw-bold text-dark mb-1">Student <span class="text-primary">Directory</span></h2>
          <p class="text-secondary mb-0 small text-uppercase fw-bold" style="letter-spacing: 1px;">
            Administrative Access & Talent Management
          </p>
        </div>
      </div>
      <div class="col-lg-5">
        <div class="input-group shadow-sm rounded-pill overflow-hidden border bg-white">
          <span class="input-group-text bg-white border-0 ps-3">
            <i class="fas fa-search text-muted"></i>
          </span>
          <input v-model="searchQuery" type="text" class="form-control border-0 py-2 shadow-none small" 
                 placeholder="Search Name, ID, or Department...">
          <button v-if="searchQuery" @click="searchQuery = ''" class="btn btn-white border-0 text-muted">
            <i class="fas fa-times-circle"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden bg-white">
      <div class="table-responsive">
        <table class="table align-middle mb-0">
          <thead class="table-light">
            <tr class="text-uppercase text-secondary" style="font-size: 0.7rem; letter-spacing: 0.05em;">
              <th class="ps-4 py-3 border-0">Student Profile</th>
              <th class="py-3 border-0">Department</th>
              <th class="py-3 border-0">Academic CGPA</th>
              <th class="py-3 border-0">Access Status</th>
              <th class="text-end pe-4 py-3 border-0">Management</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredStudents" :key="user.id" class="border-bottom">
              <td class="ps-4 py-3">
                <div class="d-flex align-items-center">
                  <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.username}`"
                       class="rounded-circle border border-2 p-1 bg-light me-3" width="45" height="45">
                  <div>
                    <div class="fw-bold text-dark" style="font-size: 0.9rem;">{{ user.name }}</div>
                    <div class="text-muted" style="font-size: 0.7rem;">ID: #{{ user.id }} | @{{ user.username }}</div>
                  </div>
                </div>
              </td>
              <td>
                <span class="fw-medium text-secondary small">
                  {{ user.student_profile?.department || 'Not Assigned' }}
                </span>
              </td>
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="progress flex-grow-1" style="height: 6px; width: 60px; background-color: #f1f5f9;">
                    <div class="progress-bar bg-primary rounded-pill" 
                         role="progressbar" 
                         :style="{ width: `${(user.student_profile?.cgpa || 0) * 10}%` }"></div>
                  </div>
                  <span class="fw-bold text-primary small" style="min-width: 25px;">{{ user.student_profile?.cgpa || '0.0' }}</span>
                </div>
              </td>
              <td>
                <span class="badge rounded-pill px-3 border" style="font-size: 0.65rem;"
                  :class="user.is_blacklisted ? 'bg-danger-subtle text-danger border-danger-subtle' : 
                          user.is_approved ? 'bg-success-subtle text-success border-success-subtle' : 
                          'bg-warning-subtle text-warning border-warning-subtle'">
                  <i class="fas me-1" :class="user.is_blacklisted ? 'fa-ban' : user.is_approved ? 'fa-check-circle' : 'fa-clock'"></i>
                  {{ user.is_blacklisted ? 'BLOCKED' : user.is_approved ? 'VERIFIED' : 'PENDING' }}
                </span>
              </td>
              <td class="text-end pe-4">
                <div class="d-flex justify-content-end gap-2">
                  <router-link :to="`/admin/student/${user.id}`" class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-bold">
                    <i class="fas fa-edit me-1"></i> Manage
                  </router-link>
                  <button v-if="user.is_blacklisted" @click="toggleBlockStatus(user.id, false)" class="btn btn-success btn-sm rounded-pill px-3 fw-bold shadow-sm">
                    <i class="fas fa-unlock me-1"></i> Restore
                  </button>
                </div>
              </td>
            </tr>
            <!-- Empty State -->
            <tr v-if="filteredStudents.length === 0">
              <td colspan="5" class="text-center py-5">
                <div class="text-secondary opacity-25 mb-3"><i class="fas fa-users-slash fa-4x"></i></div>
                <h5 class="text-muted fw-bold">No Records Found</h5>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>