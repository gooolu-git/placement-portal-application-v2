import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State: Initialized from localStorage if it exists
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || null)

  // Actions
  function login(userData, userToken) {
    token.value = userToken
    user.value = userData
    
    localStorage.setItem('token', userToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isAuthenticated, userRole, login, logout }
})