<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const applicants = ref([]); // Now fetching this specifically
const driveId = route.params.drive_id; // Ensure your router uses this param name
const selectedApp = ref(null);
const showStatusModal = ref(false);

const fetchApplicants = async () => {
  try {
    const token = localStorage.getItem('token');
    // Using GetApplicantList API
    const res = await axios.get(`http://localhost:5000/company/drive/${driveId}/applicants`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    applicants.value = res.data.data;
  } catch (err) {
    console.error("Error fetching applicants:", err);
  }
};

const updateAppStatus = async (appId, newStatus) => {
  try {
    const token = localStorage.getItem('token');
    // Using UpdateApplicationStatus API
    await axios.patch(`http://localhost:5000/company/application/${appId}/status`, 
      { status: newStatus }, 
      { headers: { Authorization: `Bearer ${token}` } }
    );
    showStatusModal.value = false;
    fetchApplicants(); // Refresh the list
  } catch (err) { 
    alert("Error updating status"); 
  }
};

const selectedCount = computed(() => 
  applicants.value.filter(a => a.status === 'Selected').length
);

onMounted(fetchApplicants);
</script>

<template>
  <div class="container py-5 mt-5 bg-light">
    <div class="row g-4">
      <!-- Summary Column -->
      <div class="col-lg-4">
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4 bg-white text-center">
          <h5 class="fw-bold mb-4">Drive Summary</h5>
          <div class="row g-2">
            <div class="col-6">
              <div class="bg-light border rounded-4 p-3">
                <div class="h3 fw-bold text-primary">{{ applicants.length }}</div>
                <small class="text-muted fw-bold text-uppercase">Total Apps</small>
              </div>
            </div>
            <div class="col-6">
              <div class="bg-light border rounded-4 p-3">
                <div class="h3 fw-bold text-success">{{ selectedCount }}</div>
                <small class="text-muted fw-bold text-uppercase">Selected</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Applicants Table -->
      <div class="col-lg-8">
        <div class="card border-0 shadow-sm rounded-4 p-4 bg-white">
          <h5 class="fw-bold mb-4 border-start border-primary border-4 ps-3">Applicant List</h5>
          <table class="table table-hover align-middle">
            <thead>
              <tr class="small text-uppercase text-secondary">
                <th>Student</th>
                <th>Status</th>
                <th class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applicants" :key="app.id">
                <td>
                  <div class="fw-bold">{{ app.student_name }}</div>
                  <small class="text-muted">ID: {{ app.student_id }}</small>
                </td>
                <td>
                  <span :class="['badge rounded-pill', app.status === 'Selected' ? 'bg-success' : 'bg-warning']">
                    {{ app.status }}
                  </span>
                </td>
                <td class="text-end">
                  <button @click="selectedApp = app; showStatusModal = true" 
                          class="btn btn-sm btn-primary rounded-pill px-3">
                    Update Status
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Status Update Modal -->
  <div v-if="showStatusModal" class="modal d-block" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow rounded-4 p-4">
        <h5 class="fw-bold mb-3">Update Applicant Status</h5>
        <select v-model="selectedApp.status" class="form-select mb-3">
          <option value="Pending">Pending</option>
          <option value="Shortlisted">Shortlisted</option>
          <option value="Selected">Selected</option>
          <option value="Rejected">Rejected</option>
        </select>
        <div class="d-flex justify-content-end gap-2">
          <button @click="showStatusModal = false" class="btn btn-light rounded-pill">Cancel</button>
          <button @click="updateAppStatus(selectedApp.id, selectedApp.status)" class="btn btn-primary rounded-pill">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>