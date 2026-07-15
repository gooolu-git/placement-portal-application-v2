<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const route = useRoute()
const authStore = useAuthStore()
const driveData = ref(null)

const fetchDrive = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/admin/drive/${route.params.id}`, { 
      headers: { 'Authorization': `Bearer ${authStore.token}` } 
    })
    driveData.value = res.data.data
  } catch (err) { 
    console.error(err)
    alert("Error fetching drive details") 
  }
}

const toggleApproval = async () => {
  try {
    await axios.patch(`http://localhost:5000/admin/drive/approve/${route.params.id}`, {}, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    fetchDrive() // Refresh data
  } catch (err) { alert(err.response?.data?.message || "Action failed") }
}

onMounted(fetchDrive)
</script>

<template>
  <div v-if="driveData" class="container py-4 mt-5">
    
    <!-- Partner Overview -->
    <div class="card shadow-sm border-0 rounded-4 p-4 mb-4">
      <div class="d-flex justify-content-between align-items-start mb-4 border-start border-primary border-4 ps-3">
        <h5 class="fw-bold text-dark mb-0">Partner Overview</h5>
      </div>
      
      <div class="row align-items-center">
        <div class="col-md-2 text-center">
          <img :src="`https://api.dicebear.com/7.x/identicon/svg?seed=${driveData.company_details.company_name}`" 
               class="rounded-circle border border-3 p-1 bg-white shadow-sm" width="90">
        </div>
        <div class="col-md-10">
          <h4 class="fw-bold text-dark mb-1">{{ driveData.company_details.company_name }}</h4>
          <div class="d-flex gap-4 text-muted small">
            <span><i class="fas fa-user-tie me-1 text-primary"></i> HR: {{ driveData.company_details.hr_contact || 'N/A' }}</span>
            <span><i class="fas fa-globe me-1 text-primary"></i> {{ driveData.company_details.website }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="row g-4">
      <div class="col-lg-8">
        <div class="card shadow-sm border-0 rounded-4 overflow-hidden">
          <div class="card-header bg-white py-3 border-0 px-4">
            <h5 class="fw-bold m-0">Applicants List ({{ driveData.total_applicants }})</h5>
          </div>
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light small text-uppercase text-muted">
                <tr>
                  <th class="px-4">Student</th>
                  <th>Department</th>
                  <th>CGPA</th>
                  <th>Resume</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in driveData.applicants" :key="app.application_id">
                  <td class="px-4">
                    <div class="fw-bold">{{ app.student_details.name }}</div>
                  </td>
                  <td>{{ app.student_details.department || 'N/A' }}</td>
                  <td>
                    <span class="badge bg-light text-dark border">{{ app.student_details.cgpa || '0.0' }}</span>
                  </td>
                  <td>
                    <a v-if="app.student_details.resume" :href="app.student_details.resume" target="_blank" class="text-primary fw-bold small">
                      <i class="fas fa-file-pdf me-1"></i>View
                    </a>
                    <span v-else class="text-muted small">N/A</span>
                  </td>
                  <td>
                    <span class="badge rounded-pill" :class="app.status === 'Selected' ? 'bg-success-subtle text-success' : 'bg-primary-subtle text-primary'">
                      {{ app.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="col-lg-4">
        <div class="card shadow-sm border-0 rounded-4 p-4">
          <h6 class="text-uppercase fw-bold text-muted small mb-3">Drive Status</h6>
          <span :class="['badge rounded-pill px-3 py-2 mb-3 d-inline-block', driveData.drive_details.status === 'Approved' ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning']">
            {{ driveData.drive_details.status }}
          </span>
          <button @click="toggleApproval" class="btn btn-outline-primary w-100 rounded-pill fw-bold">
            Toggle Drive Status
          </button>
        </div>
      </div>
    </div>
  </div>
</template>