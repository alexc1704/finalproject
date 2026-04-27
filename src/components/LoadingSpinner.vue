<!-- src/components/LoadingSpinner.vue -->
<template>
  <div class="text-center py-5">
    <div class="spinner-wrap">
      <div class="spin"></div>
    </div>
    <p class="text-muted mt-3 small">{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: 'Loading...'
  }
})
</script>

<style scoped>
.spin {
  width: 48px;
  height: 48px;
  border: 4px solid #f0e8ff;
  border-top-color: #6f42c1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

@keyframes spin { 
  to { transform: rotate(360deg); } 
}
</style>