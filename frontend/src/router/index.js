// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth'
// import HomeView from '../views/HomeView.vue'

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     {
//       path: '/',
//       name: 'home',
//       component: HomeView,
//     },
//     {
//       path: '/login',
//       name: 'login',
//       component: () => import('../views/LoginView.vue')
//     },
//     {
//       path: '/register',
//       name: 'register',
//       component: () => import('../views/RegisterView.vue')
//     },

//     // ================= ROLE PROTECTED DASHBOARDS =================
//     { 
//       path: '/admin/dashboard', 
//       name: 'admin-dashboard', 
//       component: () => import('../views/admin/AdminDashboard.vue'),
//       meta: { requiresAuth: true, roles: ['admin'] }
//     },
//     { 
//       path: '/student/dashboard', 
//       name: 'student-dashboard', 
//       component: () => import('../views/student/StudentDashboard.vue'),
//       meta: { requiresAuth: true, roles: ['student'] }
//     },
//     { 
//       path: '/company/dashboard', 
//       name: 'company-dashboard', 
//       component: () => import('../views/company/CompanyDashboard.vue'),
//       meta: { requiresAuth: true, roles: ['company'] }
//     },

//     // ================= FALLBACK ERROR ACCESS ROUTE =================
//     { 
//       path: '/unauthorized', 
//       name: 'unauthorized', 
//       component: () => import('../views/UnauthorizedView.vue') 
//     }
//   ],
// })

// // Global Traffic Cop (Route Guard Layer)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()

//   // 1. Route requires authentication check
//   if (to.meta.requiresAuth) {
//     if (!authStore.isAuthenticated) {
//       return next({ name: 'login' })
//     }

//     // 2. User role verification check
//     if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
//       return next({ name: 'unauthorized' })
//     }
//   }

//   // 3. Prevent logged-in users from hitting login/register pages again
//   if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
//     if (authStore.userRole === 'admin') return next({ name: 'admin-dashboard' })
//     if (authStore.userRole === 'company') return next({ name: 'company-dashboard' })
//     return next({ name: 'student-dashboard' })
//   }

//   next()
// })

// export default router

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('../views/UnauthorizedView.vue')
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/companies',
      name: 'admin-dashboard-companies',
      component: () => import('../views/CompanyDirectory.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/students',
      name: 'admin-dashboard-students',
      component: () => import('../views/StudentDirectory.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/company/:id',
      name: 'CompanyProfile',
      component: () => import('../views/CompanyProfile.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/student/:id',
      name: 'StudentProfile',
      component: () => import('../views/StudentProfile.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/drives',
      name: 'DriveDirectory',
      component: () => import('../views/DriveDirectory.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/drives/:id',
      name: 'DriveProfile',
      component: () => import('../views/DriveProfile.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/company/dashboard',
      name: 'CompanyDashboard',
      component: () => import('../views/CompanyDashboard.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/company/past-drives',
      name: 'PastDrives',
      component: () => import('../views/PastDrives.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/company/drive/:drive_id/applicants',
      name: 'CompanyManageDrive',
      component: () => import('../views/ManageDrive.vue')
    },
    {
      path: '/company/selected-candidates',
      name: 'SelectedCandidates',
      component: () => import('../views/SelectedCandidates.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/student/dashboard',
      name: 'StudentDashboard',
      component: () => import('../views/StudentDashboard.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/applications',
      name: 'ApplicationTracking',
      component: () => import('../views/ApplicationTracking.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/history',
      name: 'ApplicationHistory',
      component: () => import('../views/ApplicationHistory.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/ProfileView.vue'), // Ensure this path matches your file structure
      meta: { requiresAuth: true } // Accessible by student, company, and admin
    }


  ],
})

// Global Traffic Cop Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Prevent logged-in users from hitting login or register pages again
  if (authStore.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
    // If you don't have dashboards yet, redirect them safely back to home page
    return next({ name: 'home' })
  }

  next()
})

export default router