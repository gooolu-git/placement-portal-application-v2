<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Store user info and history
const user = ref(JSON.parse(localStorage.getItem('user')) || {});
const history = ref([]);
const isExporting = ref(false);

const fetchData = async () => {
  try {
    const token = localStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };

    // Fetch both History and Profile info to ensure data consistency
    const [historyRes, profileRes] = await Promise.all([
      axios.get('http://localhost:5000/student/history', { headers }),
      axios.get('http://localhost:5000/profile', { headers })
    ]);

    history.value = historyRes.data.data;
    // Update local user ref with latest profile data (department/cgpa)
    user.value = { ...user.value, ...profileRes.data };
  } catch (err) {
    console.error("Error loading data:", err);
  }
};

const exportHistory = async () => {
  isExporting.value = true;
  try {
    const token = localStorage.getItem('token');
    await axios.post('http://localhost:5000/student/export-applications', {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert("Export request sent! The report will be emailed to you shortly.");
  } catch (err) {
    console.error("Export error:", err);
    alert("Export request failed. Please try again.");
  } finally {
    isExporting.value = false;
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="container py-5 mt-5">
    <!-- Header -->
    <div class="row g-3 mb-4">
      <div class="col-12">
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
          <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center">
              <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name}`" 
                   class="rounded-circle border p-1 me-3" width="70" height="70">
              <div>
                <h4 class="fw-bold mb-0 text-dark">{{ user.name }}</h4>
                <p class="text-muted small mb-1">{{ user.department || 'Department' }} | CGPA: {{ user.cgpa || 'N/A' }}</p>
                <span class="badge bg-success-subtle text-success rounded-pill px-3">
                  <i class="fas fa-check-circle me-1"></i>Verified Student
                </span>
              </div>
            </div>
            
            <button @click="exportHistory" 
                    :disabled="isExporting || !history.length" 
                    class="btn btn-primary rounded-pill px-4 py-2 shadow-sm">
              <i :class="isExporting ? 'fas fa-spinner fa-spin' : 'fas fa-file-csv'"></i>
              {{ isExporting ? 'Generating...' : 'Download Report' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
      <h5 class="fw-bold mb-4 border-start border-primary border-4 ps-3">Application History</h5>
      
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th class="py-3 px-4">Company</th>
              <th class="py-3">Job Role</th>
              <th class="py-3">Date Applied</th>
              <th class="py-3 text-center">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in history" :key="app.id">
              <td class="px-4">
                <div class="fw-bold">{{ app.company_name }}</div>
                <a :href="app.company_website" target="_blank" class="text-decoration-none small text-muted">
                  <i class="fas fa-external-link-alt me-1"></i>Visit Website
                </a>
              </td>
              <td><span class="text-primary fw-semibold">{{ app.job_title }}</span></td>
              <td class="text-muted small">{{ app.applied_on }}</td>
              <td class="text-center">
                <span :class="['badge rounded-pill px-3', 
                      app.status === 'Selected' ? 'bg-success' : 
                      app.status === 'Rejected' ? 'bg-danger' : 'bg-warning text-dark']">
                  {{ app.status }}
                </span>
              </td>
            </tr>
            <tr v-if="!history.length">
              <td colspan="4" class="text-center py-5 text-muted">No past applications found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>