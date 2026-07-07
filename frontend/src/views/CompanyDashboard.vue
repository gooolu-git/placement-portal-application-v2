<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// State
const user = ref({ company_profile: { company_name: '' }, is_approved: false });
const drives = ref([]);
const showModal = ref(false);

const newDrive = ref({
  job_title: '',
  deadline: '',
  eligibility_criteria: '',
  job_description: ''
});

// API Methods
const fetchDashboard = async () => {
  try {
    const token = localStorage.getItem('token');
    const res = await axios.get('http://localhost:5000/company/dashboard', {
      headers: { Authorization: `Bearer ${token}` }
    });
    user.value = res.data.company;
    drives.value = res.data.drives;
  } catch (err) {
    console.error("Error fetching dashboard:", err);
  }
};

const createDrive = async () => {
  try {
    const token = localStorage.getItem('token');
    await axios.post('http://localhost:5000/company/drive/create', {
      job_title: newDrive.value.job_title,
      deadline: newDrive.value.deadline,
      eligibility_criteria: newDrive.value.eligibility_criteria,
      job_description: newDrive.value.job_description
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    showModal.value = false;
    newDrive.value = { job_title: '', deadline: '', eligibility_criteria: '', job_description: '' };
    fetchDashboard();
  } catch (error) {
    alert("Error creating drive: " + (error.response?.data?.message || error.message));
  }
};

// Computed
const activeDrives = computed(() => {
  const now = new Date();
  return drives.value.filter(d => new Date(d.deadline) > now);
});

onMounted(fetchDashboard);
</script>

<template>
  <div class="container py-5 mt-5 bg-light ">
    
    <!-- Header -->
    <div class="d-md-flex justify-content-between align-items-center mb-5">
      <div>
        <h2 class="fw-bold text-dark mb-1"> <span class="text-danger">{{ user.company_name }} <span> </span></span>Recruitment <span class="text-primary">Console</span></h2>
        <p class="text-secondary mb-0">Welcome back, <strong>{{ user.hr_name}}</strong></p>
      </div>
      <div class="d-flex gap-2 mt-3 mt-md-0">
        <router-link to="/company/past-drives" class="btn btn-white border rounded-pill px-4 py-2 fw-bold shadow-sm">
          <i class="fa-solid fa-clock-rotate-left me-2"></i>Past Drives
        </router-link>
        <button @click="showModal = true" class="btn btn-primary px-4 py-2 fw-bold rounded-pill shadow-sm">
          <i class="fa-solid fa-plus me-2"></i>Create New Opening
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row g-4 mb-5">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 p-4 h-100 bg-white">
          <div class="d-flex align-items-center">
            <div class="bg-primary bg-opacity-10 text-primary rounded-3 d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
              <i class="fa-solid fa-briefcase fs-4"></i>
            </div>
            <div>
              <h6 class="text-muted small text-uppercase mb-0 fw-bold">Active Drives</h6>
              <h3 class="fw-bold mb-0 text-dark">{{ activeDrives.length }}</h3>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 p-4 h-100 bg-white">
          <div class="d-flex align-items-center">
            <div class="bg-warning bg-opacity-10 text-warning rounded-3 d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
              <i class="fa-solid fa-bullhorn fs-4"></i>
            </div>
            <div>
              <h6 class="text-muted small text-uppercase mb-0 fw-bold">Verification Status</h6>
              <span :class="['badge rounded-pill px-3 py-2 fw-bold', user.is_approved ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning']">
                {{ user.is_approved ? 'Verified' : 'Pending Approval' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Job Postings Table -->
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden bg-white">
      <div class="px-4 py-3 border-bottom bg-light d-flex justify-content-between align-items-center">
        <h6 class="fw-bold mb-0 text-dark">Active Job Postings</h6>
        <span class="badge bg-primary rounded-pill px-3">{{ activeDrives.length }} Open</span>
      </div>
      <div class="table-responsive">
        <table class="table align-middle mb-0">
          <thead class="table-light text-uppercase text-secondary" style="font-size: 0.75rem;">
            <tr>
              <th class="ps-4 py-3">Job Details</th>
              <th class="py-3">Status</th>
              <th class="py-3">Applied</th>
              <th class="py-3">Deadline</th>
              <th class="text-end pe-4 py-3">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in activeDrives" :key="drive.id" class="border-bottom">
              <td class="ps-4 py-3">
                <div class="fw-bold text-dark">{{ drive.job_title }}</div>
                <div class="small text-muted">{{ drive.eligibility_criteria }}</div>
              </td>
              <td>
                <span class="badge rounded-pill" :class="drive.status === 'Approved' ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'">
                  {{ drive.status }}
                </span>
              </td>
              <td>{{ drive.applications?.length || 0 }}</td>
              <td>{{ drive.deadline }}</td>
              <td class="text-end pe-4">
                <router-link :to="`/company/drive/${drive.id}/applicants`" class="btn btn-primary btn-sm rounded-pill px-4 fw-bold">
                  Manage
                </router-link>
              </td>
            </tr>
            <tr v-if="activeDrives.length === 0">
              <td colspan="5" class="text-center py-5 text-muted">No active job openings found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Create Drive Modal -->
  <div v-if="showModal" class="modal d-block" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content border-0 shadow rounded-4 p-4">
        <div class="modal-header border-0 pb-3">
          <h5 class="fw-bold"><i class="fa-solid fa-pen-nib text-primary me-2"></i>Post Placement Drive</h5>
          <button type="button" class="btn-close" @click="showModal = false"></button>
        </div>
        <form @submit.prevent="createDrive">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label small fw-bold">Job Title</label>
              <input v-model="newDrive.job_title" class="form-control" required>
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-bold">Deadline</label>
              <input v-model="newDrive.deadline" type="datetime-local" class="form-control" required>
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-bold">Eligibility Criteria</label>
              <input v-model="newDrive.eligibility_criteria" class="form-control">
            </div>
            <div class="col-12">
              <label class="form-label small fw-bold">Job Description</label>
              <textarea v-model="newDrive.job_description" rows="4" class="form-control" required></textarea>
            </div>
          </div>
          <div class="mt-4 d-flex justify-content-end gap-2">
            <button type="button" @click="showModal = false" class="btn btn-light rounded-pill px-4">Cancel</button>
            <button type="submit" class="btn btn-primary rounded-pill px-5">Publish Drive</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>