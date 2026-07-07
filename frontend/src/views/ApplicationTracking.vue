<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user = ref(JSON.parse(localStorage.getItem('user')) || {});
const applications = ref([]);
const availableCount = ref(0); // Fetched from API or calculated

const fetchTracking = async () => {
  try {
    const token = localStorage.getItem('token');
    // Fetch tracking data
    const res = await axios.get('http://localhost:5000/student/tracking', {
      headers: { Authorization: `Bearer ${token}` }
    });
    applications.value = res.data.data;
    
    // Also fetch dashboard data to get the count of available jobs
    const dashRes = await axios.get('http://localhost:5000/student/dashboard', {
      headers: { Authorization: `Bearer ${token}` }
    });
    availableCount.value = dashRes.data.drives.length - dashRes.data.applied_drive_ids.length;
  } catch (err) {
    console.error("Error loading tracking:", err);
  }
};

onMounted(fetchTracking);
</script>

<template>
  <div class="container py-4 mt-5 bg-light">
    <!-- Header Summary -->
    <div class="row g-3 mb-4">
      <div class="col-lg-6">
        <div class="card border-0 shadow-sm rounded-4 p-3 bg-white h-100">
          <div class="d-flex align-items-center">
            <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name}`" 
                 class="rounded-circle border border-2 p-1 me-3 bg-white" width="70" height="70">
            <div>
              <h5 class="fw-bold mb-0 text-dark">{{ user.name }}</h5>
              <p class="text-muted small mb-1">{{ user.department || 'General' }}</p>
              <span class="small fw-bold text-success"><i class="fas fa-check-circle me-1"></i>Verified</span>
            </div>
          </div>
        </div>
      </div>
      <!-- Stats Cards -->
      <div class="col-lg-3 col-md-6">
        <router-link to="/student/dashboard" class="text-decoration-none h-100 d-block">
          <div class="card border-0 shadow-sm rounded-4 p-3 bg-white h-100 text-center">
            <div class="text-primary mb-1"><i class="fas fa-briefcase fa-lg"></i></div>
            <h4 class="fw-bold mb-0 text-primary">{{ availableCount }}</h4>
            <span class="text-muted fw-bold text-uppercase" style="font-size: 0.65rem;">Available Jobs</span>
          </div>
        </router-link>
      </div>
      <div class="col-lg-3 col-md-6">
        <div class="card border-success shadow-sm rounded-4 p-3 bg-white h-100 text-center" style="border: 1px solid rgba(25, 135, 84, 0.2);">
          <div class="text-success mb-1"><i class="fas fa-clipboard-check fa-lg"></i></div>
          <h4 class="fw-bold mb-0 text-success">{{ applications.length }}</h4>
          <span class="text-muted fw-bold text-uppercase" style="font-size: 0.65rem;">Applied Jobs</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
      <div class="d-flex justify-content-between align-items-center mb-4 border-start border-success border-4 ps-3">
        <h5 class="fw-bold text-dark mb-0">Application Tracking</h5>
        <router-link to="/student/dashboard" class="btn btn-sm btn-light border rounded-pill px-3 shadow-sm fw-bold">
          <i class="fas fa-plus me-1 text-success"></i> Apply More
        </router-link>
      </div>

      <table class="table table-hover align-middle mb-0">
        <thead class="table-light text-uppercase small">
          <tr>
            <th class="py-3 px-4">Company & Role</th>
            <th class="py-3">Applied Date</th>
            <th class="text-end py-3 px-4">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td class="py-3 px-4">
              <div class="fw-bold text-dark" style="font-size: 0.85rem;">{{ app.company_name }}</div>
              <div class="text-primary fw-semibold" style="font-size: 0.75rem;">{{ app.job_title }}</div>
            </td>
            <td class="text-muted small">{{ app.applied_on }}</td>
            <td class="text-end px-4">
              <span :class="['badge rounded-pill px-3 py-1 border small', 
                    app.status === 'Selected' ? 'bg-success-subtle text-success border-success-subtle' : 
                    app.status === 'Rejected' ? 'bg-danger-subtle text-danger border-danger-subtle' : 
                    app.status === 'Pending' ? 'bg-warning-subtle text-warning border-warning-subtle' : 'bg-primary-subtle text-primary']">
                {{ app.status }}
              </span>
            </td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="3" class="text-center py-5 text-muted">
              <i class="fas fa-inbox fa-3x opacity-25 mb-3"></i>
              <p>No applications found yet.</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>