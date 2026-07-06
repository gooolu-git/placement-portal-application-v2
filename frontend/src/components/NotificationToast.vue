<template>
  <!-- Fixed container in top-right corner -->
  <div class="position-fixed top-0 end-0 p-3" style="z-index: 1050; max-width: 400px;">
    <!-- Smooth group animations for stacking toasts -->
    <transition-group name="notification" tag="div">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        class="toast show d-flex align-items-start gap-3 p-3 mb-2 shadow-sm rounded border"
        :class="getToastClass(notification.type)"
      >
        <!-- Dynamic Emoji/Icon -->
        <div class="flex-shrink-0 fs-5">
          {{ getIcon(notification.type) }}
        </div>
        
        <!-- Header & Message Body text content -->
        <div class="flex-grow-1">
          <div class="fw-semibold text-dark mb-1">{{ notification.title }}</div>
          <div v-if="notification.message" class="small text-muted">
            {{ notification.message }}
          </div>
        </div>
        
        <!-- Local removal button -->
        <button class="btn-close flex-shrink-0" @click="removeNotification(notification.id)"></button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const notifications = ref([])

// Notification generation engine execution
function addNotification(notification) {
  const id = Date.now() + Math.random()
  const newNotification = {
    id,
    type: notification.type || 'info',
    title: notification.title,
    message: notification.message,
    duration: notification.duration || 5000
  }
  
  notifications.value.push(newNotification)
  
  // Auto-destruct event timer rule
  if (newNotification.duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
  }
}

function removeNotification(id) {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

function getIcon(type) {
  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: 'ℹ️'
  }
  return icons[type] || icons.info
}

function getToastClass(type) {
  const classes = {
    success: 'border-success bg-success bg-opacity-10',
    error: 'border-danger bg-danger bg-opacity-10',
    warning: 'border-warning bg-warning bg-opacity-10',
    info: 'border-primary bg-primary bg-opacity-10'
  }
  return classes[type] || classes.info
}

// Global Custom Event hook listener handler
function handleGlobalNotification(event) {
  addNotification(event.detail)
}

onMounted(() => {
  window.addEventListener('show-notification', handleGlobalNotification)
})

onUnmounted(() => {
  window.removeEventListener('show-notification', handleGlobalNotification)
})

// Expose methods natively to templates explicitly accessing via refs
defineExpose({
  addNotification,
  removeNotification
})
</script>

<style scoped>
/* Stacking layout transitions rules */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.35s cubic-bezier(0.25, 1, 0.5, 1);
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(120%) scale(0.9);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(120%) scale(0.9);
}

/* Ensure absolute positioning handles layout shift calculations on item removal */
.notification-leave-active {
  position: absolute;
  width: 100%;
}

/* Mobile Responsiveness View Overrides */
@media (max-width: 768px) {
  .position-fixed {
    left: 1rem !important;
    right: 1rem !important;
    max-width: none !important;
  }
}
</style>