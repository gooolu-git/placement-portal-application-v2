<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const authStore = useAuthStore()

// KPI Metrics Counters
const totalCompanies = ref(0)
const totalStudents = ref(0)
const totalDrives = ref(0)
const totalApplications = ref(0)
const totalApprovedCount = ref(0)

// Tab Array Lists
const pendingCompanies = ref([])
const pendingStudents = ref([])
const pendingPlacementDrives = ref([])

const searchQuery = ref('')
const activeTab = ref('companies')
const isLoading = ref(true)

// Fetch all dashboard stats and pending records
const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    // 1. Fetch unapproved pending users
    const resUnactive = await fetch('http://localhost:5000/admin/unactive-users', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const dataUnactive = await resUnactive.json()
    if (dataUnactive.status === 'success') {
      pendingCompanies.value = dataUnactive.data.filter(u => u.role === 'company')
      pendingStudents.value = dataUnactive.data.filter(u => u.role === 'student')
    }

    // 2. Fetch active approved items for counters
    const resActive = await fetch('http://localhost:5000/admin/users', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const dataActive = await resActive.json()
    if (dataActive.status === 'success') {
      totalApprovedCount.value = dataActive.count
      totalCompanies.value = dataActive.data.filter(u => u.role === 'company').length
      totalStudents.value = dataActive.data.filter(u => u.role === 'student').length
    }

    // 3. Fetch all drives to filter for pending
    const resDrives = await fetch('http://localhost:5000/admin/drives', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const dataDrives = await resDrives.json()
    if (dataDrives.status === 'success') {
      pendingPlacementDrives.value = dataDrives.data.filter(d => d.status === 'pending')
      totalDrives.value = pendingPlacementDrives.value.length
    }
    
  } catch (err) {
    toast.error('Sync Error', 'Could not fetch records from the server.')
  } finally {
    isLoading.value = false
  }
}

// User Actions
const handleUserApproval = async (userId, newStatus) => {
  try {
    const res = await fetch(`http://localhost:5000/admin/approve/${userId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify({ is_approved: newStatus })
    })
    const data = await res.json()
    if (res.ok && data.status === 'success') {
      toast.success('Status Updated', data.action || 'User status updated.')
      pendingCompanies.value = pendingCompanies.value.filter(u => u.id !== userId)
      pendingStudents.value = pendingStudents.value.filter(u => u.id !== userId)
      fetchDashboardData()
    } else {
      toast.error('Operation Failed', data.message || 'Could not update user.')
    }
  } catch (err) {
    toast.error('Network Error', 'Server connection failure.')
  }
}

const handleUserBlacklist = async (userId, blockStatus) => {
  try {
    const res = await fetch(`http://localhost:5000/admin/block/${userId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify({ is_blocked: blockStatus })
    })
    const data = await res.json()
    if (res.ok && data.status === 'success') {
      toast.success('User Flagged', data.action || 'User blacklist rule set.')
      pendingCompanies.value = pendingCompanies.value.filter(u => u.id !== userId)
      pendingStudents.value = pendingStudents.value.filter(u => u.id !== userId)
      fetchDashboardData()
    } else {
      toast.error('Operation Failed', data.message || 'Could not update blacklist configuration.')
    }
  } catch (err) {
    toast.error('Network Error', 'Server connection failure.')
  }
}

// Drive Action
const handleDriveApproval = async (driveId) => {
  try {
    const res = await fetch(`http://localhost:5000/admin/drive/approve/${driveId}`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    const data = await res.json()
    if (res.ok && data.status === 'success') {
      toast.success('Drive Approved', data.message || 'Drive status updated.')
      pendingPlacementDrives.value = pendingPlacementDrives.value.filter(d => d.id !== driveId)
      totalDrives.value = pendingPlacementDrives.value.length
    } else {
      toast.error('Operation Failed', data.message || 'Could not approve drive.')
    }
  } catch (err) {
    toast.error('Network Error', 'Server connection failure.')
  }
}

// Reactive Filters
const filteredCompanies = computed(() => pendingCompanies.value.filter(u => 
  u.company_profile?.company_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
  u.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
  String(u.id).includes(searchQuery.value)
))

const filteredStudents = computed(() => pendingStudents.value.filter(u => 
  u.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
  u.student_profile?.department?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
  String(u.id).includes(searchQuery.value)
))

const filteredDrives = computed(() => pendingPlacementDrives.value.filter(d => 
  d.job_title?.toLowerCase().includes(searchQuery.value.toLowerCase())
))

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
      <div class="col-lg-5 mt-3 mt-lg-0">
        <div class="input-group shadow-sm">
          <span class="input-group-text bg-white border-end-0"><i class="fa-solid fa-magnifying-glass text-secondary"></i></span>
          <input v-model="searchQuery" type="text" class="form-control border-start-0 py-2 shadow-none" placeholder="Search name, ID, or contact...">
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="row g-3 mb-5">
      <div class="col-md-3"><div class="card border-0 border-start border-primary border-4 shadow-sm h-100 bg-white p-3"><div class="text-muted small fw-bold text-uppercase">Total Companies</div><h3 class="fw-bold mb-0 text-dark">{{ totalCompanies }}</h3></div></div>
      <div class="col-md-3"><div class="card border-0 border-start border-info border-4 shadow-sm h-100 bg-white p-3"><div class="text-muted small fw-bold text-uppercase">Students</div><h3 class="fw-bold mb-0 text-dark">{{ totalStudents }}</h3></div></div>
      <div class="col-md-3"><div class="card border-0 border-start border-warning border-4 shadow-sm h-100 bg-white p-3"><div class="text-muted small fw-bold text-uppercase">Total Drives</div><h3 class="fw-bold mb-0 text-dark">{{ totalDrives }}</h3></div></div>
      <div class="col-md-3"><div class="card border-0 border-start border-success border-4 shadow-sm h-100 bg-white p-3"><div class="text-muted small fw-bold text-uppercase">Applications</div><h3 class="fw-bold mb-0 text-dark">{{ totalApplications }}</h3></div></div>
    </div>

    <!-- Approvals Card -->
    <div class="card border-0 shadow-sm overflow-hidden bg-white rounded-3">
      <div class="bg-light px-4 py-3 border-bottom d-flex justify-content-between align-items-center">
        <h6 class="fw-bold mb-0 text-dark"><i class="fa-solid fa-clock me-2 text-warning"></i>Pending Approvals</h6>
        <span class="badge bg-primary rounded-pill px-3">Verified Users: {{ totalApprovedCount }}</span>
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
          <div v-if="activeTab === 'companies'" class="table-responsive rounded-3 border">
            <table class="table align-middle mb-0">
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
          <div v-if="activeTab === 'students'" class="table-responsive rounded-3 border">
            <table class="table align-middle mb-0">
              <thead class="table-light"><tr><th class="py-3 px-4">Name</th><th>Dept</th><th>CGPA</th><th>Action</th></tr></thead>
              <tbody>
                <tr v-for="user in filteredStudents" :key="user.id">
                  <td class="px-4 fw-bold">{{ user.name }}</td>
                  <td>{{ user.student_profile?.department }}</td>
                  <td>{{ user.student_profile?.cgpa || '0.0' }}</td>
                  <td>
                    <button @click="handleUserApproval(user.id, true)" class="btn btn-success btn-sm rounded-pill px-3 me-2">Verify</button>
                    <button @click="handleUserBlacklist(user.id, true)" class="btn btn-outline-dark btn-sm rounded-pill px-3">Blacklist</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Drives -->
          <div v-if="activeTab === 'drives'" class="table-responsive rounded-3 border">
            <table class="table align-middle mb-0">
              <thead class="table-light"><tr><th class="py-3 px-4">Drive</th><th>Deadline</th><th>Action</th></tr></thead>
              <tbody>
                <tr v-for="drive in filteredDrives" :key="drive.id">
                  <td class="px-4 fw-bold">{{ drive.job_title }}</td>
                  <td>{{ drive.deadline }}</td>
                  <td>
                    <button @click="handleDriveApproval(drive.id)" class="btn btn-warning btn-sm rounded-pill px-3 text-white">Approve</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>