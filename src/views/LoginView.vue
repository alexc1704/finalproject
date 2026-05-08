<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
      <div class="card shadow border-0 rounded-4 p-4">
        <h2 class="fw-bold mb-1">Welcome back 👋</h2>
        <p class="text-muted">Log in to browse matches and messages.</p>
        <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
        <form @submit.prevent="handleLogin">
          <label class="form-label">Email</label>
          <input v-model.trim="email" class="form-control mb-3" type="email" required />
          <label class="form-label">Password</label>
          <input v-model="password" class="form-control mb-3" type="password" required />
          <button class="btn btn-primary w-100" :disabled="loading">{{ loading ? 'Signing in...' : 'Sign In' }}</button>
        </form>
        <p class="text-center mt-3 mb-0">New here? <router-link to="/register">Create an account</router-link></p>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)
async function handleLogin() {
  errorMsg.value = ''
  loading.value = true
  try {
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch (error) {
    errorMsg.value = error.message
  } finally {
    loading.value = false
  }
}
</script>
