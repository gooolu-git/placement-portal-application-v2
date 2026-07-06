<template>
  <!-- Hero Section -->
  <section 
    class="vh-100 d-flex align-items-center justify-content-center text-center bg-white position-relative hero-section"
  >
    <!-- Decorative Blobs using inline styles -->
    <div class="blob blob-top-right"></div>
    <div class="blob blob-bottom-left"></div>
    
    <div class="container position-relative z-1">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <h1 class="display-2 fw-bolder text-dark mb-4">
            Empowering Careers, <br>
            <span class="text-primary">Connecting Futures.</span>
          </h1>
          <p class="lead text-secondary mb-5 mx-auto max-w-700">
            The unified platform for students, companies, and institutes to streamline recruitment and foster professional growth.
          </p>
          <div class="d-flex justify-content-center gap-3">
            <router-link to="/login" class="btn btn-primary btn-lg px-5 py-3 fw-bold shadow">
              Login
            </router-link>
            <!-- <router-link to="/s" class="btn btn-outline-primary btn-lg px-5 py-3 fw-bold shadow-sm">
              Sign Up
            </router-link> -->
          </div>
        </div>
      </div>
    </div>
  </section>
</template>



<style scoped>
/* Scoped styles to keep your template clean and readable */
.hero-section {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cpath d='M0 40 L40 40 L40 0 M0 0 L0 40' fill='none' stroke='%230d6efd' stroke-width='0.5' stroke-opacity='0.1'/%3E%3C/svg%3E");
}

.blob {
  position: absolute;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(13, 110, 253, 0.08) 0%, rgba(255, 255, 255, 0) 70%);
  border-radius: 50%;
  z-index: 0;
}

.blob-top-right {
  top: -10%;
  right: -10%;
}

.blob-bottom-left {
  bottom: -10%;
  left: -10%;
}

.max-w-700 {
  max-width: 700px;
}

.z-1 {
  z-index: 1;
}
</style>