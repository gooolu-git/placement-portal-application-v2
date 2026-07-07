<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { toast } from '@/utils/toast'

const authStore = useAuthStore()
const companies = ref([])
const searchQuery = ref('')
const isLoading = ref(true)

// Fetch all companies from your Flask API
const fetchCompanies = async () => {
  isLoading.value = true
  try {
    const res = await fetch('http://localhost:5000/admin/users', {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const response = await res.json()
    if (response.status === 'success') {
      // Filter only roles that are 'company'
      companies.value = response.data.filter(u => u.role === 'company')
    }
  } catch (err) {
    toast.error('Error', 'Could not load companies.')
  } finally {
    isLoading.value = false
  }
}

// Logic to approve/verify a company
const verifyCompany = async (user_id) => {
  try {
    const res = await fetch(`http://localhost:5000/admin/approve/${user_id}`, {
      method: 'PATCH',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}` 
      },
      body: JSON.stringify({ is_approved: true })
    })
    if (res.ok) {
      toast.success('Success', 'Company verified successfully.')
      fetchCompanies() // Refresh list
    }
  } catch (err) {
    toast.error('Error', 'Verification failed.')
  }
}

const filteredCompanies = computed(() => {
  return companies.value.filter(u => 
    u.company_profile?.company_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    u.username.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

onMounted(fetchCompanies)
</script>

<template>
  <div class="container py-5 mt-5 bg-light m">
    <!-- Header -->
    <div class="row mb-4 align-items-end">
      <div class="col-lg-7">
        <h2 class="fw-bold text-dark mb-1">Company <span class="text-primary">Directory</span></h2>
        <p class="text-secondary mb-0">Manage and verify company accounts.</p>
      </div>
      <div class="col-lg-5 mt-3 mt-lg-0">
        <div class="input-group shadow-sm rounded-pill overflow-hidden">
          <span class="input-group-text bg-white border-end-0 ps-3">
            <i class="fas fa-search text-muted"></i>
          </span>
          <input v-model="searchQuery" type="text" class="form-control border-start-0 py-2 shadow-none" placeholder="Search company...">
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
      <table class="table align-middle mb-0">
        <thead class="table-light">
          <tr class="text-uppercase text-secondary" style="font-size: 0.75rem;">
            <th class="py-3 px-4">Company Details</th>
            <th class="py-3">HR Contact</th>
            <th class="py-3">Website</th>
            <th class="py-3">Status</th>
            <th class="text-end py-3 px-4">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr v-for="user in filteredCompanies" :key="user.id" class="border-bottom">
            <td class="px-4 py-3">
              <div class="d-flex align-items-center">
                <img :src="`https://api.dicebear.com/7.x/identicon/svg?seed=${user.company_profile?.company_name || user.username}`" class="rounded-circle border border-2 p-1 me-3" width="45" height="45">
                <div>
                  <div class="fw-bold text-dark">{{ user.company_profile?.company_name || 'N/A' }}</div>
                  <div class="text-muted" style="font-size: 0.7rem;">ID: {{ user.id }} | @{{ user.username }}</div>
                </div>
              </div>
            </td>
            <td>{{ user.company_profile?.hr_contact || 'N/A' }}</td>
            <td>
              <a v-if="user.company_profile?.website" :href="user.company_profile.website" target="_blank" class="btn btn-sm btn-light border rounded-pill px-3 fw-bold text-primary" style="font-size: 0.7rem;">
                Visit <i class="fas fa-external-link-alt ms-1"></i>
              </a>
            </td>
            <td>
              <span class="fw-bold px-3 py-1 rounded-pill border small" :class="user.is_approved ? 'bg-success-subtle text-success' : 'bg-warning-subtle text-warning'">
                {{ user.is_approved ? 'Verified' : 'Pending' }}
              </span>
            </td>
            <td class="text-end px-4">
              <button v-if="!user.is_approved" @click="verifyCompany(user.id)" class="btn btn-sm btn-primary rounded-pill px-3 fw-bold shadow-sm me-2">Verify</button>
              <router-link :to="`/admin/company/${user.id}`" class="btn btn-sm btn-outline-primary rounded-pill px-3 fw-bold shadow-sm">
                View <i class="fas fa-eye ms-1"></i>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>