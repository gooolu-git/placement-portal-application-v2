<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const selectedStudents = ref([]);
const companyName = ref(''); // Simplified: just fetching name from auth or store

const fetchSelected = async () => {
  try {
    const token = localStorage.getItem('token');
    const res = await axios.get('http://localhost:5000/company/selected-candidates', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    // API returns { status: 'success', data: [...] }
    selectedStudents.value = res.data.data;
    
    // Optional: Get company name from a different call or store if not in this response
    // For now, we assume you might want to fetch it from the Dashboard API or 
    // simply use a placeholder if the API doesn't return it.
  } catch (err) {
    console.error("Error fetching selected:", err);
  }
};

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-GB', { month: 'short', day: '2-digit', year: 'numeric' });
};

onMounted(fetchSelected);
</script>

<template>
  <div class="container py-4 mt-5 bg-light">
    <!-- Header -->
    <div class="d-md-flex justify-content-between align-items-center mb-4">
      <div class="border-start border-primary border-4 ps-3">
        <h2 class="fw-bold text-dark mb-1">Selected <span class="text-primary">Candidates</span></h2>
      </div>
      <div class="mt-3 mt-md-0 d-flex gap-2">
        <button onclick="window.print()" class="btn btn-white border rounded-pill fw-bold px-4 shadow-sm btn-sm">
          <i class="fas fa-print me-2 text-primary"></i>Export Report
        </button>
        <router-link to="/company/dashboard" class="btn btn-primary rounded-pill fw-bold px-4 shadow-sm btn-sm">
          Dashboard
        </router-link>
      </div>
    </div>

    <!-- Table -->
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden bg-white">
      <table class="table align-middle mb-0">
        <thead class="table-light">
          <tr class="text-uppercase text-secondary" style="font-size: 0.7rem; letter-spacing: 0.05em;">
            <th class="ps-4 py-3 border-0">Candidate Name</th>
            <th class="py-3 border-0">Job Role</th>
            <th class="py-3 border-0">Academic Info</th>
            <th class="py-3 border-0">Status</th>
            <th class="text-end pe-4 py-3 border-0">Resume</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in selectedStudents" :key="app.id" class="border-bottom">
            <td class="ps-4 py-3">
              <div class="d-flex align-items-center">
                <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${app.student_name}`" 
                     class="rounded-circle border border-2 p-1 bg-light me-3" width="45" height="45">
                <div>
                  <div class="fw-bold text-dark" style="font-size: 0.9rem;">{{ app.student_name }}</div>
                  <div class="text-muted" style="font-size: 0.7rem;">ID: #{{ app.student_id }}</div>
                </div>
              </div>
            </td>
            <td>
              <div class="fw-bold text-dark" style="font-size: 0.85rem;">{{ app.drive_title }}</div>
              <div class="text-muted small" style="font-size: 0.7rem;">Hired: {{ formatDate(app.applied_on) }}</div>
            </td>
            <td>
              <div class="fw-bold text-dark small">{{ app.department }}</div>
              <div class="badge bg-info-subtle text-info border rounded-pill" style="font-size: 0.65rem;">
                CGPA: {{ app.cgpa }}
              </div>
            </td>
            <td>
              <span class="badge bg-success-subtle text-success border rounded-pill small">SELECTED</span>
            </td>
            <td class="text-end pe-4">
              <a v-if="app.resume" :href="`http://localhost:5000/static/uploads/${app.resume}`" 
                 target="_blank" class="btn btn-outline-primary btn-sm rounded-pill px-3">View</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>