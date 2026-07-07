<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user = ref(JSON.parse(localStorage.getItem('user')) || {});
const history = ref([]);

const fetchHistory = async () => {
  try {
    const token = localStorage.getItem('token');
    // Calling the API endpoint created in the previous step
    const res = await axios.get('http://localhost:5000/student/history', {
      headers: { Authorization: `Bearer ${token}` }
    });
    history.value = res.data.data;
  } catch (err) {
    console.error("Error loading history:", err);
  }
};

onMounted(fetchHistory);
</script>

<template>
  <div class="container py-5 mt-5 bg-light">
    <!-- User Profile Header -->
    <div class="row g-3 mb-4">
      <div class="col-lg-12">
        <div class="card border-0 shadow-sm rounded-4 p-3 bg-white">
          <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center">
              <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${user.name}`" 
                   class="rounded-circle border border-2 p-1 me-3 bg-white" width="70" height="70">
              <div>
                <h5 class="fw-bold mb-0 text-dark">{{ user.name }}</h5>
                <p class="text-muted small mb-1">{{ user.department }}</p>
                <span class="small fw-bold text-success"><i class="fas fa-check-circle me-1"></i>Verified Student</span>
              </div>
            </div>
            <router-link to="/student/applications" class="btn btn-sm btn-outline-secondary rounded-pill px-4 fw-bold">
              Back
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- History Table -->
    <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
      <div class="d-flex justify-content-between align-items-center mb-4 border-start border-secondary border-4 ps-3">
        <h5 class="fw-bold text-dark mb-0">Closed Application Records</h5>
      </div>

      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light text-uppercase small">
            <tr>
              <th class="py-3 px-4">Company & Role</th>
              <th class="py-3">Drive Deadline</th>
              <th class="text-end py-3 px-4">Final Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in history" :key="app.id" class="border-bottom">
              <td class="py-3 px-4">
                <div class="fw-bold text-dark" style="font-size: 0.85rem;">{{ app.company_name }}</div>
                <div class="text-primary fw-semibold" style="font-size: 0.75rem;">{{ app.job_title }}</div>
              </td>
              <td>
                <div class="text-muted small">
                  <i class="far fa-calendar-times me-1 text-danger"></i> {{ app.applied_on }}
                </div>
              </td>
              <td class="text-end px-4">
                <span :class="['badge rounded-pill px-3 py-1 border small', 
                      app.status === 'Selected' ? 'bg-success-subtle text-success border-success-subtle' : 
                      app.status === 'Rejected' ? 'bg-danger-subtle text-danger border-danger-subtle' : 'bg-light text-secondary']">
                  {{ app.status }}
                </span>
              </td>
            </tr>
            <tr v-if="history.length === 0">
              <td colspan="3" class="text-center py-5 text-muted">
                <i class="fas fa-history fa-3x opacity-50 mb-3"></i>
                <p>No past recruitment records found.</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>