<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const user = ref({});
const drives = ref([]);
const appliedDriveIds = ref([]);
const searchQuery = ref('');

const fetchDashboard = async () => {
  try {
    const token = localStorage.getItem('token');
    // Using the API endpoint created previously
    const res = await axios.get(`http://localhost:5000/student/dashboard?search=${searchQuery.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    drives.value = res.data.drives;
    appliedDriveIds.value = res.data.applied_drive_ids;
    // Assuming you have a user info endpoint or store user data on login
    user.value = JSON.parse(localStorage.getItem('user')); 
  } catch (err) {
    console.error("Error loading dashboard:", err);
  }
};

// Filter logic mirroring your Jinja logic
const unappliedDrives = computed(() => {
  return drives.value.filter(d => !appliedDriveIds.value.includes(d.id));
});

const applyToDrive = async (driveId) => {
  try {
    const token = localStorage.getItem('token');
    await axios.post(`http://localhost:5000/student/apply/${driveId}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    fetchDashboard(); // Refresh list to remove the applied drive
  } catch (err) {
    alert(err.response?.data?.message || "Application failed");
  }
};

onMounted(fetchDashboard);
</script>

<template>
  <div class="container py-4 mt-5 bg-light">
    <!-- Header Cards -->
    <div class="row g-4 mb-4">
      <div class="col-lg-6">
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white h-100">
          <div class="d-flex align-items-center">
            <div class="position-relative me-4">
              <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name}`" 
                   class="rounded-circle border border-3 border-white shadow-sm" width="80" height="80">
            </div>
            <div>
              <h4 class="fw-bold text-dark mb-1">{{ user.name }}</h4>
              <div class="text-muted small mb-2 fw-medium">
                <i class="fas fa-graduation-cap me-1 text-primary"></i> {{ user.department || 'General' }}
              </div>
              <span v-if="user.is_approved" class="badge bg-success-subtle text-success border rounded-pill px-3">Verified</span>
            </div>
          </div>
        </div>
      </div>
      <!-- Stats Cards -->
      <div class="col-lg-3 col-md-6">
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white h-100 text-center">
          <h2 class="fw-bold text-dark mb-0">{{ unappliedDrives.length }}</h2>
          <div class="text-muted fw-bold text-uppercase" style="font-size: 0.65rem;">Open Opportunities</div>
        </div>
      </div>
    </div>

    <!-- Search & Table -->
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden bg-white">
      <div class="p-4 border-bottom bg-white d-flex justify-content-between align-items-center">
        <h5 class="fw-bold text-dark mb-0">Eligible Placement Drives</h5>
        <input v-model="searchQuery" @input="fetchDashboard" class="form-control w-25" placeholder="Search...">
      </div>
      
      <table class="table table-hover align-middle mb-0">
        <thead class="table-light">
          <tr class="text-uppercase text-secondary small">
            <th class="py-3 px-4">Job Detail & Company</th>
            <th class="py-3">Deadline</th>
            <th class="text-end py-3 px-4">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in unappliedDrives" :key="drive.id">
            <td class="px-4 py-3">
              <div class="fw-bold text-dark">{{ drive.company_name }}</div>
              <div class="text-primary small">{{ drive.job_title }}</div>
            </td>
            <td>{{ drive.deadline }}</td>
            <td class="text-end px-4">
              <button @click="applyToDrive(drive.id)" class="btn btn-primary rounded-pill px-4 btn-sm shadow-sm">
                Apply Now
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>