<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="home-container d-flex align-items-center justify-content-center min-vh-100 position-relative overflow-hidden ">
    <!-- Grid Overlay Background Styling Effect -->
    <div class="grid-background position-absolute top-0 start-0 w-100 h-100"></div>

    <div class="container position-relative z-index-10 py-5 text-center">
      <div class="row justify-content-center">
        <div class="col-12 col-md-10 col-lg-8">
          
          <h1 class="display-3 fw-bold mb-4 main-title">
            Empowering Careers, <br />
            <span class="text-primary">Connecting Futures.</span>
          </h1>
          
          <p class="lead text-muted mx-auto mb-5 description-text" style="max-width: 600px;">
            The unified platform for students, companies, and institutes to streamline recruitment and foster professional growth.
          </p>

          <div class="d-flex justify-content-center gap-3">
            <RouterLink to="/login" class="btn btn-primary btn-lg px-5 py-3 fw-bold shadow-sm">
              Login
            </RouterLink>
            <RouterLink to="/register" class="btn btn-outline-primary btn-lg px-5 py-3 fw-bold">
              Sign Up
            </RouterLink>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  background-color: #ffffff;
}

/* Restores your exact original clean grid background overlay layout */
.grid-background {
  background-size: 40px 40px;
  background-image: 
    linear-gradient(to right, rgba(0, 0, 0, 0.03) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0, 0, 0, 0.03) 1px, transparent 1px);
}

.z-index-10 {
  z-index: 10;
}

.main-title {
  color: #1e293b;
  letter-spacing: -1px;
}

.description-text {
  font-size: 1.15rem;
  line-height: 1.6;
}
</style>