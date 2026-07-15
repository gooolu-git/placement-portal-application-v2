<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const authStore = useAuthStore()

// KPI Metrics
const totalCompanies = ref(0)
const totalStudents = ref(0)
const totalApprovedDrives = ref(0)
const totalApplications = ref(0)
const totalApprovedCount = ref(0)

// Data Lists
const pendingCompanies = ref([])
const pendingStudents = ref([])
const pendingPlacementDrives = ref([])

const searchQuery = ref('')
const activeTab = ref('companies')
const isLoading = ref(true)

const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    const headers = { 'Authorization': `Bearer ${authStore.token}` }
    const [resUnactive, resActive, resDrives] = await Promise.all([
      fetch('http://localhost:5000/admin/unactive-users', { headers }),
      fetch('http://localhost:5000/admin/users', { headers }),
      fetch('http://localhost:5000/admin/drives', { headers })
    ])

    const dataUnactive = await resUnactive.json()
    const dataActive = await resActive.json()
    const dataDrives = await resDrives.json()

    if (dataUnactive.status === 'success') {
      pendingCompanies.value = dataUnactive.data.filter(u => u.role === 'company')
      pendingStudents.value = dataUnactive.data.filter(u => u.role === 'student')
    }
    if (dataActive.status === 'success') {
      totalApprovedCount.value = dataActive.count
      totalCompanies.value = dataActive.data.filter(u => u.role === 'company').length
      totalStudents.value = dataActive.data.filter(u => u.role === 'student').length
    }
    if (dataDrives.status === 'success') {
      pendingPlacementDrives.value = dataDrives.data.filter(d => d.status === 'pending')
      totalApprovedDrives.value = dataDrives.data.filter(d => d.status === 'Approved').length
      totalApplications.value = dataDrives.applicationcount
    }
  } catch (err) {
    toast.error('Sync Error', 'Could not fetch records.')
  } finally {
    isLoading.value = false
  }
}

const handleUserApproval = async (userId, status) => {
  try {
    const res = await fetch(`http://localhost:5000/admin/approve/${userId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authStore.token}` },
      body: JSON.stringify({ is_approved: status })
    })
    if (res.ok) { fetchDashboardData() }
  } catch (err) { toast.error('Error', 'Action failed.') }
}

const handleUserBlacklist = async (userId, status) => { /* Logic Implementation */ }

const handleDriveApproval = async (driveId) => {
  try {
    const res = await fetch(`http://localhost:5000/admin/drive/approve/${driveId}`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) { fetchDashboardData() }
  } catch (err) { toast.error('Error', 'Action failed.') }
}

const filteredCompanies = computed(() => pendingCompanies.value.filter(u => (u.company_profile?.company_name || u.name)?.toLowerCase().includes(searchQuery.value.toLowerCase())))
const filteredStudents = computed(() => pendingStudents.value.filter(u => u.name?.toLowerCase().includes(searchQuery.value.toLowerCase())))
const filteredDrives = computed(() => pendingPlacementDrives.value.filter(d => d.job_title?.toLowerCase().includes(searchQuery.value.toLowerCase())))

onMounted(fetchDashboardData)
</script>

<template>
  <div class="container py-5 mt-5 bg-light">
    <!-- Header -->
    <div class="row mb-5 align-items-center">
      <div class="col-lg-7">
        <h2 class="fw-bold text-dark mb-1">Admin <span class="text-primary">Console</span></h2>
        <p class="text-secondary mb-0">Overview of portal activity and pending approvals.</p>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="row g-3 mb-5">
      <div class="col-md-3">
        <div class="card border-0 shadow-sm p-3 border-start border-primary border-4">
          <div class="text-muted small fw-bold text-uppercase">Companies</div>
          <h3 class="fw-bold">{{ totalCompanies }}</h3>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm p-3 border-start border-info border-4">
          <div class="text-muted small fw-bold text-uppercase">Students</div>
          <h3 class="fw-bold">{{ totalStudents }}</h3>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm p-3 border-start border-warning border-4">
          <div class="text-muted small fw-bold text-uppercase">Approved Drives</div>
          <h3 class="fw-bold">{{ totalApprovedDrives }}</h3>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm p-3 border-start border-success border-4">
          <div class="text-muted small fw-bold text-uppercase">Applications</div>
          <h3 class="fw-bold">{{ totalApplications }}</h3>
        </div>
      </div>
    </div>

    <!-- Approvals Card -->
    <div class="card border-0 shadow-sm overflow-hidden bg-white rounded-3">
      <div class="bg-light px-4 py-3 border-bottom d-flex justify-content-between align-items-center">
        <h6 class="fw-bold mb-0 text-dark"><i class="fa-solid fa-clock me-2 text-warning"></i>Pending Approvals</h6>
        <span class="badge bg-primary rounded-pill px-3">Verified Users: {{ totalApprovedCount - 1 }}</span>
      </div>

      <ul class="nav nav-underline px-4 pt-2 border-bottom">
        <li class="nav-item"><button @click="activeTab = 'companies'" :class="['nav-link fw-bold py-3 px-4 border-0', activeTab === 'companies' ? 'active' : '']">Companies ({{ filteredCompanies.length }})</button></li>
        <li class="nav-item"><button @click="activeTab = 'students'" :class="['nav-link fw-bold py-3 px-4 border-0', activeTab === 'students' ? 'active' : '']">Students ({{ filteredStudents.length }})</button></li>
        <li class="nav-item"><button @click="activeTab = 'drives'" :class="['nav-link fw-bold py-3 px-4 border-0', activeTab === 'drives' ? 'active' : '']">Drives ({{ filteredDrives.length }})</button></li>
      </ul>

      <div class="card-body p-4">
        <div v-if="isLoading" class="text-center py-5">Loading logs...</div>
        <template v-else>
          <!-- Companies -->
          <div v-if="activeTab === 'companies'" class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light"><tr><th class="py-3 px-4">Company</th><th>HR Contact</th><th>Action</th></tr></thead>
              <tbody>
                <tr v-for="user in filteredCompanies" :key="user.id">
                  <td class="px-4 fw-bold">{{ user.company_profile?.company_name || user.name }}</td>
                  <td>{{ user.company_profile?.hr_contact || 'N/A' }}</td>
                  <td>
                    <button @click="handleUserApproval(user.id, true)" class="btn btn-primary btn-sm rounded-pill px-3 me-2">Approve</button>
                    <button @click="handleUserBlacklist(user.id, true)" class="btn btn-outline-danger btn-sm rounded-pill px-3">Reject</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Students -->
          <div v-if="activeTab === 'students'" class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr><th class="py-3 px-4">Name</th><th>Dept</th><th style="min-width: 180px;">CGPA</th><th>Action</th></tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredStudents" :key="user.id">
                  <td class="px-4 fw-bold">{{ user.name }}</td>
                  <td>{{ user.student_profile?.department || 'N/A' }}</td>
                  <td class="pe-5">
                    <div class="d-flex align-items-center gap-3">
                      <div class="progress flex-grow-1" style="height: 6px; width: 80px; background-color: #f1f5f9;">
                        <div class="progress-bar bg-primary rounded-pill" role="progressbar" :style="{ width: `${(user.student_profile?.cgpa || 0) * 10}%` }"></div>
                      </div>
                      <span class="fw-bold text-primary small" style="min-width: 30px;">{{ user.student_profile?.cgpa || '0.0' }}</span>
                    </div>
                  </td>
                  <td>
                    <button @click="handleUserApproval(user.id, true)" class="btn btn-success btn-sm rounded-pill px-3 me-2">Verify</button>
                    <button @click="handleUserBlacklist(user.id, true)" class="btn btn-outline-dark btn-sm rounded-pill px-3">Blacklist</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Drives -->
          <div v-if="activeTab === 'drives'" class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light"><tr><th class="py-3 px-4">Drive</th><th>Deadline</th><th>Action</th></tr></thead>
              <tbody>
                <tr v-for="drive in filteredDrives" :key="drive.id">
                  <td class="px-4 fw-bold">{{ drive.job_title }}</td>
                  <td>{{ drive.deadline }}</td>
                  <td><button @click="handleDriveApproval(drive.id)" class="btn btn-warning btn-sm rounded-pill px-3 text-white">Approve</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.table { border: none !important; }
.table thead th { border: none !important; }
.table tbody td { border-bottom: 1px solid #f8f9fa !important; }
</style>