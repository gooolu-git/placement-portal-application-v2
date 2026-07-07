<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const drives = ref([])
const searchQuery = ref('')

const fetchDrives = async () => {
  const url = searchQuery.value ? `http://localhost:5000/admin/drives?search=${searchQuery.value}` : 'http://localhost:5000/admin/drives'
  const res = await fetch(url, { headers: { 'Authorization': `Bearer ${authStore.token}` } })
  const json = await res.json()
  drives.value = json.data
}

const isExpired = (deadline) => new Date(deadline) < new Date()

onMounted(fetchDrives)
</script>

<template>
  <div class="container py-5 mt-4 bg-light ">
    <div class="row mb-5 align-items-center">
      <div class="col-lg-7">
        <h2 class="fw-bold text-dark mb-2">Available <span class="text-primary">Drives</span></h2>
        <p class="text-secondary mb-0">View current job opportunities that are open for application.</p>
      </div>
      <div class="col-lg-5 mt-3 mt-lg-0">
        <div class="input-group shadow-sm rounded-pill overflow-hidden">
          <span class="input-group-text bg-white border-end-0 ps-3"><i class="fas fa-search text-muted"></i></span>
          <input type="text" v-model="searchQuery" @keyup.enter="fetchDrives" class="form-control border-start-0 py-2 shadow-none" placeholder="Search Job Title or ID...">
          <button v-if="searchQuery" @click="searchQuery=''; fetchDrives()" class="input-group-text bg-white border-start-0 pe-3 text-danger border-0">
            <i class="fas fa-times-circle"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm rounded-4 overflow-hidden bg-white">
      <table class="table align-middle mb-0">
        <thead class="table-light">
          <tr class="text-uppercase text-secondary" style="font-size: 0.7rem; letter-spacing: 0.05em;">
            <th class="py-3 px-4">Job Title</th><th>Company-ID</th><th>Deadline</th><th>Status</th><th class="text-end px-4">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in drives" :key="drive.id" class="border-bottom">
            <td class="px-4 py-3">
              <div class="fw-bold text-dark">{{ drive.job_title }}</div>
              <small class="text-muted" style="font-size: 0.7rem;">Post ID: #{{ drive.id }}</small>
            </td>
            <td><div class="fw-semibold small"><i class="fas fa-building me-2 text-primary opacity-75"></i> ID: #{{ drive.company_id }}</div></td>
            <td><div class="text-muted small"><i class="far fa-calendar-alt me-2"></i> {{ drive.deadline }}</div></td>
            <td>
              <span class="fw-bold px-3 py-1 rounded-pill border small" :class="isExpired(drive.deadline) ? 'bg-danger-subtle text-danger border-danger-subtle' : 'bg-success-subtle text-success border-success-subtle'">
                {{ isExpired(drive.deadline) ? 'Closed' : 'Active' }}
              </span>
            </td>
            <td class="text-end px-4">
              <router-link :to="`/admin/drive/${drive.id}`" class="btn btn-primary btn-sm rounded-pill px-3 fw-bold"><i class="fas fa-eye me-1"></i> View</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>