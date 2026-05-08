<template>
  <nav class="navbar navbar-expand-lg navbar-dark px-4" style="background: linear-gradient(135deg, #6f42c1, #e83e8c);">
    <router-link class="navbar-brand fw-bold" to="/">💘 DriftDater</router-link>
    <button class="navbar-toggler" type="button" @click="menuOpen = !menuOpen"><span class="navbar-toggler-icon"></span></button>
    <div :class="['collapse navbar-collapse', menuOpen ? 'show' : '']">
      <ul class="navbar-nav ms-auto align-items-lg-center">
        <li class="nav-item me-lg-2">
          <button class="btn btn-sm btn-light" @click="themeStore.toggle">{{ themeStore.mode === 'dark' ? '☀️ Light' : '🌙 Dark' }}</button>
        </li>
        <template v-if="!authStore.isLoggedIn">
          <li class="nav-item"><router-link class="nav-link" to="/login" @click="menuOpen=false">Login</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/register?fresh=1" @click="menuOpen=false">Register</router-link></li>
        </template>
        <template v-else>
          <li class="nav-item"><router-link class="nav-link" to="/dashboard" @click="menuOpen=false">Browse</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/matches" @click="menuOpen=false">Matches</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/messages" @click="menuOpen=false">Messages</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/profile" @click="menuOpen=false">Profile</router-link></li>
          <li class="nav-item"><a class="nav-link" href="#" @click.prevent="handleLogout">Logout</a></li>
        </template>
      </ul>
    </div>
  </nav>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'
const authStore = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()
const menuOpen = ref(false)
async function handleLogout() {
  await authStore.logout()
  menuOpen.value = false
  router.push('/login')
}
</script>
