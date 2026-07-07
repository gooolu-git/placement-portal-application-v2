<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const drive = ref(null)

const fetchDrive = async () => {
  const res = await fetch(`http://localhost:5000/admin/drive/${route.params.id}`, { headers: { 'Authorization': `Bearer ${authStore.token}` } })
  const json = await res.json()
  drive.value = json.data
}

const updateDrive = async (statusOverride = null) => {
  const payload = { ...drive.value }
  if (statusOverride) payload.status = statusOverride
  await fetch(`http://localhost:5000/admin/drive/${drive.value.id}`, {
    method: 'PATCH',
    headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  fetchDrive()
}

onMounted(fetchDrive)
</script>

<template>
  <div v-if="drive" class="container py-4 mt-4">
    <div class="row g-4">
      <div class="col-lg-4 order-lg-2">
        <div class="card shadow-sm border-0 rounded-4 p-4">
          <div class="d-flex justify-content-between mb-3">
             <h6 class="text-uppercase fw-bold text-muted small">Status</h6>
             <span :class="['badge rounded-pill px-3', drive.status === 'Approved' ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning']">{{ drive.status }}</span>
          </div>
          <form @submit.prevent="updateDrive()">
            <input v-model="drive.job_title" class="form-control form-control-sm mb-3">
            <input v-model="drive.job_description" class="form-control form-control-sm mb-3">
            <button class="btn btn-primary btn-sm w-100 rounded-pill fw-bold">Save Changes</button>
          </form>
          <hr>
          <button @click="updateDrive(drive.status === 'Closed' ? 'Approved' : 'Closed')" class="btn btn-sm w-100 rounded-pill" :class="drive.status === 'Closed' ? 'btn-outline-success' : 'btn-outline-danger'">
            {{ drive.status === 'Closed' ? 'Re-open Drive' : 'Close Applications' }}
          </button>
        </div>
      </div>

      <div class="col-lg-8 order-lg-1">
        <div class="card shadow-sm border-0 rounded-4">
          <div class="card-header bg-white py-3 border-0 border-bottom"><h5>Candidate List</h5></div>
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light"><tr><th>Name</th><th>Dept</th><th>Status</th></tr></thead>
            <tbody>
              <tr v-for="app in drive.applications" :key="app.id">
                <td><div class="fw-bold">{{ app.student_name }}</div></td>
                <td>{{ app.department || 'N/A' }}</td>
                <td><span class="badge bg-primary-subtle text-primary">{{ app.status }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>