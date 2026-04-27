<!-- Replace your current AppHeader.vue with this -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark px-4"
    style="background: linear-gradient(135deg, #6f42c1, #e83e8c);">

    <router-link class="navbar-brand fw-bold" to="/">
      💘 DriftDater
    </router-link>

    <!-- Hamburger -->
    <button
      class="navbar-toggler"
      type="button"
      @click="menuOpen = !menuOpen"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div :class="['collapse navbar-collapse', menuOpen ? 'show' : '']">
      <ul class="navbar-nav ms-auto">

        <template v-if="!authStore.isLoggedIn">
          <li class="nav-item">
            <router-link class="nav-link" to="/login"
              @click="menuOpen = false">
              Login
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/register"
              @click="menuOpen = false">
              Register
            </router-link>
          </li>
        </template>

        <template v-else>
          <li class="nav-item">
            <router-link class="nav-link" to="/dashboard"
              @click="menuOpen = false">
              Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/matches"
              @click="menuOpen = false">
              Matches
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/messages"
              @click="menuOpen = false">
              Messages
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profile"
              @click="menuOpen = false">
              Profile
            </router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="handleLogout">
              Logout
            </a>
          </li>
        </template>

      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const menuOpen = ref(false)

function handleLogout() {
  authStore.logout()
  menuOpen.value = false
  router.push('/login')
}
</script>