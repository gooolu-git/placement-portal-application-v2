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
const activeTab = ref('companies') // 'companies' | 'students' | 'drives'
const isLoading = ref(true)

// Fetch all dashboard stats and pending records from your backend updates
const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    // 1. Fetch unapproved pending users (Uses updated unactive-users payload key)
    const resUnactive = await fetch('http://localhost:5000/admin/unactive-users', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const dataUnactive = await resUnactive.json()
    if (dataUnactive.status === 'success') {
      // Filter array lists reactively by user role
      pendingCompanies.value = dataUnactive.data.filter(u => u.role === 'company')
      pendingStudents.value = dataUnactive.data.filter(u => u.role === 'student')
    }

    // 2. Fetch active approved items to compute counters
    const resActive = await fetch('http://localhost:5000/admin/users', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const dataActive = await resActive.json()
    if (dataActive.status === 'success') {
      totalApprovedCount.value = dataActive.count
      totalCompanies.value = dataActive.data.filter(u => u.role === 'company').length
      totalStudents.value = dataActive.data.filter(u => u.role === 'student').length
    }

    // Placeholder counters for Drives and Applications
    totalDrives.value = pendingPlacementDrives.value.length
    totalApplications.value = 0
    pendingPlacementDrives.value = []
    
  } catch (err) {
    toast.error('Sync Error', 'Could not fetch records from the server.')
  } finally {
    isLoading.value = false
  }
}

// User Action Pipeline
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
      // Immediate structural array filtering without page refreshes
      pendingCompanies.value = pendingCompanies.value.filter(u => u.id !== userId)
      pendingStudents.value = pendingStudents.value.filter(u => u.id !== userId)
      fetchDashboardData() // Recalculate summary metrics row
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
      fetchDashboardData() // Recalculate summary metrics row
    } else {
      toast.error('Operation Failed', data.message || 'Could not update blacklist configuration.')
    }
  } catch (err) {
    toast.error('Network Error', 'Server connection failure.')
  }
}

// Reactive Filters Matching Text Queries
const filteredCompanies = computed(() => {
  return pendingCompanies.value.filter(u => 
    u.company_profile?.company_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    u.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    String(u.id).includes(searchQuery.value)
  )
})

const filteredStudents = computed(() => {
  return pendingStudents.value.filter(u => 
    u.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    u.student_profile?.department?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    String(u.id).includes(searchQuery.value)
  )
})

const filteredDrives = computed(() => {
  return pendingPlacementDrives.value.filter(d => 
    d.job_title?.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

onMounted(() => {
  fetchDashboardData()
})
</script>

<template>
  <div class="container py-5 mt-5 bg-light ">
    <!-- Header Controls Grid -->
    <div class="row mb-5 align-items-center">
      <div class="col-lg-7">
        <h2 class="fw-bold text-dark mb-1">Admin <span class="text-primary">Console</span></h2>
        <p class="text-secondary mb-0">Overview of portal activity and pending approvals.</p>
      </div>
      <div class="col-lg-5 mt-3 mt-lg-0">
        <div class="position-relative">
          <div class="input-group shadow-sm">
            <span class="input-group-text bg-white border-end-0">
              <i class="fa-solid fa-magnifying-glass text-secondary"></i>
            </span>
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control border-start-0 py-2 shadow-none" 
              placeholder="Search name, ID, or contact..."
            />
            <button 
              v-if="searchQuery" 
              @click="searchQuery = ''" 
              class="btn btn-white border-start-0 text-muted d-flex align-items-center"
            >
              <i class="fa-solid fa-circle-xmark"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats Cards Summary Block -->
    <div class="row g-3 mb-5">
      <div class="col-md-3">
        <div class="card border-0 border-start border-primary border-4 shadow-sm h-100 bg-white">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <div class="text-muted small fw-bold text-uppercase label-spacing">Total Companies</div>
              <h3 class="fw-bold mb-0 text-dark">{{ totalCompanies }}</h3>
            </div>
            <i class="fa-solid fa-building text-primary opacity-25 fs-2"></i>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 border-start border-info border-4 shadow-sm h-100 bg-white">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <div class="text-muted small fw-bold text-uppercase label-spacing">Students</div>
              <h3 class="fw-bold mb-0 text-dark">{{ totalStudents }}</h3>
            </div>
            <i class="fa-solid fa-user-graduate text-info opacity-25 fs-2"></i>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 border-start border-warning border-4 shadow-sm h-100 bg-white">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <div class="text-muted small fw-bold text-uppercase label-spacing">Total Drives</div>
              <h3 class="fw-bold mb-0 text-dark">{{ totalDrives }}</h3>
            </div>
            <i class="fa-solid fa-bullhorn text-warning opacity-25 fs-2"></i>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 border-start border-success border-4 shadow-sm h-100 bg-white">
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <div class="text-muted small fw-bold text-uppercase label-spacing">Applications</div>
              <h3 class="fw-bold mb-0 text-dark">{{ totalApplications }}</h3>
            </div>
            <i class="fa-solid fa-file-lines text-success opacity-25 fs-2"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Registration Approvals Card Wrapper -->
    <div class="card border-0 shadow-sm overflow-hidden bg-white rounded-3">
      <div class="bg-light px-4 py-3 border-bottom d-flex justify-content-between align-items-center">
        <h6 class="fw-bold mb-0 text-dark">
          <i class="fa-solid fa-clock me-2 text-warning"></i>Pending Approvals
        </h6>
        <span class="badge bg-primary rounded-pill px-3">Verified Users: {{ totalApprovedCount }}</span>
      </div>
      
      <!-- Interactive Underlined Nav Tabs -->
      <ul class="nav nav-underline px-4 pt-2 border-bottom" role="tablist">
        <li class="nav-item">
          <button 
            @click="activeTab = 'companies'" 
            :class="['nav-link fw-bold py-3 px-4 border-0 bg-transparent', activeTab === 'companies' ? 'active' : '']"
            type="button"
          >
            Companies ({{ filteredCompanies.length }})
          </button>
        </li>
        <li class="nav-item">
          <button 
            @click="activeTab = 'students'" 
            :class="['nav-link fw-bold py-3 px-4 border-0 bg-transparent', activeTab === 'students' ? 'active' : '']"
            type="button"
          >
            Students ({{ filteredStudents.length }})
          </button>
        </li>
        <li class="nav-item">
          <button 
            @click="activeTab = 'drives'" 
            :class="['nav-link fw-bold py-3 px-4 border-0 bg-transparent', activeTab === 'drives' ? 'active' : '']"
            type="button"
          >
            Drives ({{ filteredDrives.length }})
          </button>
        </li>
      </ul>

      <!-- Central Table Canvas -->
      <div class="card-body p-4">
        <div v-if="isLoading" class="text-center py-5">
          <div class="spinner-border text-primary spinner-border-sm" role="status"></div>
          <p class="text-muted small mt-2">Loading verification logs...</p>
        </div>

        <template v-else>
          <!-- CATEGORY MODULE 1: COMPANIES -->
          <div v-if="activeTab === 'companies'" class="table-responsive rounded-3 border">
            <table class="table align-middle mb-0">
              <thead class="table-light">
                <tr class="small text-uppercase text-secondary tracking-wider">
                  <th class="py-3 px-4">Company Details</th>
                  <th class="py-3">HR Contact</th>
                  <th class="py-3">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredCompanies" :key="user.id">
                  <td class="px-4">
                    <div class="d-flex align-items-center">
                      <img :src="`https://api.dicebear.com/7.x/identicon/svg?seed=${user.company_profile?.company_name || 'Corp'}`" class="rounded-circle border border-2 p-1 me-3" width="40" />
                      <div>
                        <div class="fw-bold text-dark">{{ user.company_profile?.company_name || user.name }}</div>
                        <div class="small text-muted">ID: {{ user.id }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="small text-secondary">{{ user.company_profile?.hr_contact || 'No contact registered' }}</td>
                  <td>
                    <div class="d-flex gap-2">
                      <button @click="handleUserApproval(user.id, true)" class="btn btn-primary btn-sm rounded-pill px-3 fw-bold">Approve</button>
                      <button @click="handleUserBlacklist(user.id, true)" class="btn btn-outline-danger btn-sm rounded-pill px-3 fw-bold">Reject</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="!filteredCompanies.length">
                  <td colspan="3" class="text-center py-5 text-muted small">No pending company requests.</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- CATEGORY MODULE 2: STUDENTS -->
          <div v-if="activeTab === 'students'" class="table-responsive rounded-3 border">
            <table class="table align-middle mb-0">
              <thead class="table-light">
                <tr class="small text-uppercase text-secondary tracking-wider">
                  <th class="py-3 px-4">Student Name</th>
                  <th class="py-3">Department</th>
                  <th class="py-3">CGPA</th>
                  <th class="py-3">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredStudents" :key="user.id">
                  <td class="px-4">
                    <div class="d-flex align-items-center">
                      <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name}`" class="rounded-circle border border-2 p-1 me-3" width="40" />
                      <div>
                        <div class="fw-bold text-dark">{{ user.name }}</div>
                        <div class="small text-muted">User Id: {{ user.id }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="small text-secondary">{{ user.student_profile?.department || 'Unassigned' }}</td>
                  <td>
                    <div class="d-flex align-items-center">
                      <div class="progress me-2 rounded-pill" style="height: 6px; width: 80px;">
                        <div 
                          class="progress-bar bg-primary" 
                          role="progressbar" 
                          :style="{ width: `${(user.student_profile?.cgpa || 0) * 10}%` }"
                        ></div>
                      </div>
                      <span class="fw-bold text-primary small">{{ user.student_profile?.cgpa || '0.0' }}</span>
                    </div>
                  </td>
                  <td>
                    <div class="d-flex gap-2">
                      <button @click="handleUserApproval(user.id, true)" class="btn btn-success btn-sm rounded-pill px-3 fw-bold">Verify</button>
                      <button @click="handleUserBlacklist(user.id, true)" class="btn btn-outline-dark btn-sm rounded-pill px-3 fw-bold">Blacklist</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="!filteredStudents.length">
                  <td colspan="4" class="text-center py-5 text-muted small">No pending student requests.</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- CATEGORY MODULE 3: DRIVES -->
          <div v-if="activeTab === 'drives'" class="table-responsive rounded-3 border">
            <table class="table align-middle mb-0">
              <thead class="table-light">
                <tr class="small text-uppercase text-secondary tracking-wider">
                  <th class="py-3 px-4">Drive</th>
                  <th class="py-3">Company Id</th>
                  <th class="py-3">Deadline</th>
                  <th class="py-3">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="drive in filteredDrives" :key="drive.id">
                  <td class="px-4"><div class="fw-bold text-dark">{{ drive.job_title }}</div></td>
                  <td class="small text-secondary">{{ drive.company_id }}</td>
                  <td class="small text-danger fw-bold">{{ drive.deadline }}</td>
                  <td>
                    <div class="d-flex gap-2">
                      <button class="btn btn-warning btn-sm rounded-pill px-3 fw-bold text-white">Approve</button>
                      <button class="btn btn-outline-danger btn-sm rounded-pill px-3 fw-bold">Reject</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="!filteredDrives.length">
                  <td colspan="4" class="text-center py-5 text-muted small">No pending drive requests.</td>
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
.label-spacing {
  font-size: 0.7rem; 
  letter-spacing: 0.5px;
}
.tracking-wider {
  letter-spacing: 0.05em;
}
.nav-link {
  color: #6c757d;
  transition: color 0.2s ease-in-out;
}
.nav-link:hover {
  color: #0d6efd;
}
.nav-link.active {
  color: #0d6efd !important;
  border-bottom: 2px solid #0d6efd !important;
}
</style>