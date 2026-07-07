<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// --- State ---
const drives = ref([]);
const loading = ref(true);

// --- Fetch Data ---
const fetchDrives = async () => {
  try {
    const token = localStorage.getItem('token');
    // Using the same endpoint as dashboard to get all drives
    const res = await axios.get('http://localhost:5000/company/dashboard', {
      headers: { Authorization: `Bearer ${token}` }
    });
    drives.value = res.data.drives;
  } catch (err) {
    console.error("Error fetching drives:", err);
  } finally {
    loading.value = false;
  }
};

// --- Computed: Logic to mimic your Jinja filter ---
const pastDrivesList = computed(() => {
  const now = new Date();
  return drives.value.filter(d => new Date(d.deadline) < now);
});

onMounted(fetchDrives);
</script>

<template>
  <div class="container py-5 mt-4 bg-light min-vh-100">
    
    <!-- Header -->
    <div class="d-md-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold text-dark mb-1">Drive <span class="text-secondary">Archive</span></h2>
        <p class="text-secondary mb-0">Reviewing <strong>{{ pastDrivesList.length }}</strong> completed recruitment cycles</p>
      </div>
      <router-link to="/company/dashboard" class="btn btn-white border rounded-pill px-4 fw-bold shadow-sm mt-3 mt-md-0">
        <i class="fa-solid fa-arrow-left me-2"></i>Active Console
      </router-link>
    </div>

    <!-- Stats Card -->
    <div class="row g-4 mb-4">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
          <div class="d-flex align-items-center">
            <div class="bg-secondary bg-opacity-10 text-secondary rounded-3 d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
              <i class="fa-solid fa-clock-rotate-left fs-4"></i>
            </div>
            <div>
              <h6 class="text-muted small text-uppercase mb-0 fw-bold" style="font-size: 0.7rem; letter-spacing: 0.5px;">Completed Drives</h6>
              <h3 class="fw-bold mb-0 text-dark">{{ pastDrivesList.length }}</h3>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden bg-white">
      <div class="px-4 py-3 border-bottom bg-light">
        <h6 class="fw-bold mb-0 text-dark">Expired Job Postings</h6>
      </div>
      <div class="table-responsive">
        <table class="table align-middle mb-0">
          <thead class="table-light">
            <tr class="text-uppercase text-secondary" style="font-size: 0.75rem; letter-spacing: 0.05em;">
              <th class="ps-4 py-3 border-0">Job Details</th>
              <th class="py-3 border-0">Applications</th>
              <th class="py-3 border-0">Closed On</th>
              <th class="text-end pe-4 py-3 border-0">Final Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in pastDrivesList" :key="drive.id" class="border-bottom">
              <td class="ps-4 py-3">
                <div class="fw-bold text-dark">{{ drive.job_title }}</div>
                <div class="small text-muted">
                  <i class="fa-solid fa-circle-info me-1"></i> Final Status: {{ drive.status }}
                </div>
              </td>
              <td>
                <div class="d-flex align-items-center">
                  <span class="fw-bold me-2 text-dark">{{ drive.applications?.length || 0 }}</span>
                  <i class="fa-solid fa-user-check text-success small"></i>
                </div>
              </td>
              <td>
                <div class="small fw-bold text-danger">
                  <i class="fa-solid fa-calendar-xmark me-1"></i>
                  {{ new Date(drive.deadline).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) }}
                </div>
              </td>
              <td class="text-end pe-4">
                <router-link :to="`/company/drive/${drive.id}/applicants`" class="btn btn-outline-secondary btn-sm rounded-pill px-4 shadow-sm fw-bold">
                  View Results <i class="fa-solid fa-chart-line ms-1"></i>
                </router-link>
              </td>
            </tr>
            <tr v-if="pastDrivesList.length === 0">
              <td colspan="4" class="text-center py-5">
                <div class="text-secondary opacity-25 mb-3">
                  <i class="fa-solid fa-folder-open fa-4x"></i>
                </div>
                <h5 class="text-muted fw-bold">No past drives found</h5>
                <p class="text-muted small mb-0">Drives will appear here once their deadline passes.</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>