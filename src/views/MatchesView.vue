<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div><h2 class="fw-bold mb-1">Your Matches 💞</h2><p class="text-muted mb-0">Only mutual likes become matches.</p></div>
      <span class="badge bg-primary fs-6">{{ matches.length }} Matches</span>
    </div>
    <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
    <LoadingSpinner v-if="loading" message="Loading matches..." />
    <div v-else-if="matches.length === 0" class="alert alert-info">No mutual matches yet. Like profiles from Browse, then have another user like you back.</div>
    <div class="row g-4">
      <div v-for="item in matches" :key="item.id" class="col-md-6">
        <div class="card border-0 shadow-sm rounded-4 p-3">
          <div class="d-flex gap-3">
            <img :src="item.other_user.photo || avatarUrl(item.other_user.name)" class="rounded-circle" width="70" height="70" />
            <div class="flex-grow-1">
              <h5 class="fw-bold mb-0">{{ item.other_user.name }}, {{ item.other_user.age }}</h5>
              <p class="text-muted small mb-1">📍 {{ item.other_user.location }} • {{ item.other_user.match_score }}% match</p>
              <p class="small mb-2">{{ item.other_user.bio }}</p>
              <router-link class="btn btn-sm btn-primary" :to="`/messages?match=${item.id}`">Message</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { apiFetch } from '../services/api'
const matches = ref([])
const loading = ref(false)
const errorMsg = ref('')
function avatarUrl(name) { return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=e83e8c&color=fff` }
async function loadMatches() {
  loading.value = true; errorMsg.value = ''
  try { matches.value = (await apiFetch('/api/matches')).matches } catch (e) { errorMsg.value = e.message } finally { loading.value = false }
}
onMounted(loadMatches)
</script>
