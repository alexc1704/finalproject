<template>
  <div class="login-wrapper">

    <!-- Left Panel - Decorative -->
    <div class="login-left d-none d-md-flex">
      <div class="left-content">
        <h1 class="display-4 fw-bold text-white">💘</h1>
        <h2 class="text-white fw-bold mt-3">Find Your Drift</h2>
        <p class="text-white-50 mt-2">
          Life is better when you share it with someone who gets you.
        </p>
        <div class="dots mt-4">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>

    <!-- Right Panel - Form -->
    <div class="login-right">
      <div class="form-box">

        <div class="mb-4">
          <h3 class="fw-bold">Welcome back 👋</h3>
          <p class="text-muted small">Sign in to continue your journey</p>
        </div>

        <!-- Error Alert -->
        <div v-if="errorMsg" class="alert alert-danger py-2 small">
          ⚠️ {{ errorMsg }}
        </div>

        <!-- Email -->
        <div class="input-group-custom mb-3">
          <span class="input-icon">✉️</span>
          <input
            v-model="email"
            type="email"
            placeholder="Email address"
            class="custom-input"
          />
        </div>

        <!-- Password -->
        <div class="input-group-custom mb-4">
          <span class="input-icon">🔒</span>
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Password"
            class="custom-input"
          />
          <span class="input-toggle" @click="showPassword = !showPassword">
            {{ showPassword ? '🙈' : '👁️' }}
          </span>
        </div>

        <!-- Login Button -->
        <button
          class="btn-login w-100"
          @click="handleLogin"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner"></span>
          <span v-else>Sign In →</span>
        </button>

        <p class="text-center mt-4 small text-muted">
          New here?
          <router-link to="/register" class="fw-bold text-decoration-none link-purple">
            Create an account
          </router-link>
        </p>

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
const showPassword = ref(false)

async function handleLogin() {
  errorMsg.value = ''

  if (!email.value || !password.value) {
    errorMsg.value = 'Please fill in all fields.'
    return
  }

  loading.value = true

  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      authStore.login(data.user, data.token)
      router.push('/dashboard')
    } else {
      errorMsg.value = data.message || 'Invalid email or password.'
    }

  } catch (err) {
    errorMsg.value = 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  min-height: 90vh;
  border-radius: 20px;
  overflow: hidden;
  max-width: 900px;
  margin: 40px auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}

/* Left decorative panel */
.login-left {
  flex: 1;
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.left-content {
  text-align: center;
}

.dots span {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  margin: 0 4px;
}

.dots span:first-child {
  background: white;
}

/* Right form panel */
.login-right {
  flex: 1;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.form-box {
  width: 100%;
  max-width: 340px;
}

/* Custom input */
.input-group-custom {
  display: flex;
  align-items: center;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  padding: 10px 14px;
  transition: border 0.2s;
}

.input-group-custom:focus-within {
  border-color: #6f42c1;
}

.input-icon {
  margin-right: 10px;
  font-size: 16px;
}

.input-toggle {
  cursor: pointer;
  margin-left: auto;
  font-size: 16px;
}

.custom-input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 14px;
  background: transparent;
}

/* Login button */
.btn-login {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}

.btn-login:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Spinner */
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.link-purple {
  color: #6f42c1;
}
</style>