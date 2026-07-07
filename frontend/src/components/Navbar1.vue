<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/') // Redirect back to the landing page on logout
}
</script>

<template>
  <nav class="navbar navbar-expand-lg fixed-top navbar-custom px-2" style="z-index: 1050;">
    <div class="container">
      <!-- App Brand Title Logo -->
      <RouterLink class="navbar-brand fw-bold text-primary d-flex align-items-center fs-4" to="/">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="me-2">
          <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
          <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
        </svg>
        <span style="letter-spacing: -0.5px;">PlaceMeFirst</span>
      </RouterLink>

      <button class="navbar-toggler border-0 shadow-none" type="button" data-bs-toggle="collapse"
        data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">

          <!-- ================= AUTHORIZED ROUTING LINKS ================= -->
          <template v-if="authStore.isAuthenticated">

            <!-- Admin Specific Nav Links -->
            <template v-if="authStore.userRole === 'admin'">
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/admin/dashboard">Dashboard
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/admin/companies">Companies
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/admin/students">Students
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/admin/drives">Drives
                </RouterLink>
              </li>
            </template>

            <!-- Company Specific Nav Links -->
            <template v-slot:default v-else-if="authStore.userRole === 'company'">
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/admin/dashboard">Dashboard
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/company/dashboard">Active
                  Drives</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/company/past-drives">Past
                  Drives</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/company/selected">Selected
                </RouterLink>
              </li>
            </template>

            <!-- Student Specific Nav Links (Default fallback auth role) -->
            <template v-else>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/student/dashboard">Browse
                  Jobs</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/student/applications">My
                  Applications</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/student/history">
                  Applications History</RouterLink>
              </li>
            </template>

            <!-- Profile Avatar Layout -->
            <li class="nav-item ms-lg-4">
              <RouterLink to="/profile" class="d-flex align-items-center text-decoration-none" title="View Profile">
                <div class="avatar-ring rounded-circle shadow-sm">
                  <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${authStore.user?.name || 'Guest'}`"
                    alt="Profile Avatar" class="rounded-circle"
                    style="width: 32px; height: 32px; object-fit: cover; background-color: #f1f5f9;">
                </div>
              </RouterLink>
            </li>

            <!-- Interactive Logout Action -->
            <li class="nav-item ms-lg-3">
              <button @click="handleLogout"
                class="btn btn-outline-danger logout-btn fw-bold px-4 rounded-pill btn-sm shadow-sm">
                Logout
              </button>
            </li>
          </template>

          <!-- ================= UNAUTHORIZED ROUTING LINKS ================= -->
          <template v-else>
            <li class="nav-item">
              <RouterLink class="nav-link nav-link-custom text-dark px-3 fw-semibold" to="/">About</RouterLink>
            </li>
            <li class="nav-item ms-lg-3">
              <RouterLink to="/login" class="btn btn-link text-dark text-decoration-none fw-bold px-3">Log In
              </RouterLink>
            </li>
            <li class="nav-item ms-lg-2">
              <RouterLink to="/register" class="btn btn-primary fw-bold px-4 rounded-pill shadow-sm">Get Started
              </RouterLink>
            </li>
          </template>

        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* Scoped styles guarantee your styles won't bleed out into other templates */
.navbar-custom {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.nav-link-custom {
  position: relative;
  transition: color 0.3s ease;
  font-size: 0.95rem;
}

.nav-link-custom::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0px;
  left: 50%;
  background: #0d6efd;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-link-custom:hover::after {
  width: 60%;
}

.avatar-ring {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(13, 110, 253, 0.15);
  background: white;
  padding: 2px;
}

.avatar-ring:hover {
  transform: scale(1.1);
  border-color: #0d6efd;
  box-shadow: 0 8px 15px rgba(13, 110, 253, 0.1);
}

.logout-btn {
  transition: all 0.3s ease;
  border: 1.5px solid #fee2e2;
  color: #dc3545;
  background: transparent;
}

.logout-btn:hover {
  background-color: #dc3545 !important;
  color: white !important;
  transform: translateY(-1px);
}
</style>