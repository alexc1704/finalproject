<template>
  <div class="app-shell">
    <AppHeader />
    <main class="container mt-4">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import { useThemeStore } from './stores/theme'
const themeStore = useThemeStore()
onMounted(() => themeStore.apply())
</script>

<style>
:root {
  --dd-bg: #ffffff;
  --dd-card: #ffffff;
  --dd-text: #212529;
  --dd-muted: #6c757d;
  --dd-border: rgba(0,0,0,.08);
}
:root[data-theme='dark'] {
  --dd-bg: #12101a;
  --dd-card: #1f1b2e;
  --dd-text: #f5f3ff;
  --dd-muted: #c5bfd6;
  --dd-border: rgba(255,255,255,.12);
}
body { background: var(--dd-bg); color: var(--dd-text); }
.card, .modal-content, .list-group-item, .form-control, .form-select {
  background-color: var(--dd-card) !important;
  color: var(--dd-text) !important;
  border-color: var(--dd-border) !important;
}
.text-muted { color: var(--dd-muted) !important; }
:root[data-theme='dark'] .text-bg-light { background-color: #332b49 !important; color: #f5f3ff !important; }
:root[data-theme='dark'] .bg-white { background-color: var(--dd-card) !important; }
:root[data-theme='dark'] .messages-box { background: #181322 !important; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
