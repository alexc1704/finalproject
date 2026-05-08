<template>
  <div>
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-1">Browse Potential Matches 💫</h2>
        <p class="text-muted mb-0">Database profiles scored by shared interests, age, location, goal, premium status, and boost visibility.</p>
      </div>
      <button class="btn btn-outline-primary mt-3 mt-md-0" @click="boostProfile" :disabled="boosting">
        🚀 {{ boosting ? 'Boosting...' : 'Boost My Profile' }}
      </button>
    </div>

    <div class="card border-0 shadow-sm rounded-4 p-3 mb-4">
      <div class="row g-2 align-items-end">
        <div class="col-md-3"><label class="form-label small">Search</label><input v-model="filters.q" class="form-control" placeholder="Name or bio" /></div>
        <div class="col-md-2"><label class="form-label small">Location</label><input v-model="filters.location" class="form-control" placeholder="Kingston" /></div>
        <div class="col-md-2"><label class="form-label small">Gender</label><select v-model="filters.gender" class="form-select"><option value="">Any</option><option value="Female">Female</option><option value="Male">Male</option><option value="Non-binary">Non-binary</option><option value="Other">Other</option></select></div>
        <div class="col-md-2"><label class="form-label small">Interest</label><input v-model="filters.interest" class="form-control" placeholder="gaming" /></div>
        <div class="col-md-1"><label class="form-label small">Min</label><input v-model.number="filters.min_age" type="number" class="form-control" /></div>
        <div class="col-md-1"><label class="form-label small">Max</label><input v-model.number="filters.max_age" type="number" class="form-control" /></div>
        <div class="col-md-2"><label class="form-label small">Goal</label><select v-model="filters.relationship_goal" class="form-select"><option value="">Any</option><option>Friendship</option><option>Dating</option><option>Long-term</option><option>Casual</option><option>Networking</option></select></div>
        <div class="col-md-1"><button class="btn btn-primary w-100" @click="loadProfiles">Go</button></div>
        <div class="col-md-3"><label class="form-label small">Sort</label><select v-model="filters.sort" class="form-select"><option value="score">Best match</option><option value="boosted">Boosted first</option><option value="verified">Verified first</option><option value="newest">Newest</option><option value="age">Age</option></select></div>
        <div class="col-md-9 d-flex flex-wrap gap-3 pt-2">
          <label class="form-check-label"><input v-model="filters.verified" class="form-check-input me-1" type="checkbox" /> Verified only</label>
          <label class="form-check-label"><input v-model="filters.premium" class="form-check-input me-1" type="checkbox" /> Premium only</label>
          <label class="form-check-label"><input v-model="filters.boosted" class="form-check-input me-1" type="checkbox" /> Boosted only</label>
          <button class="btn btn-sm btn-outline-secondary" @click="resetFilters">Reset filters</button>
        </div>
      </div>
    </div>

    <div v-if="notice" class="alert alert-success">{{ notice }}</div>
    <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
    <LoadingSpinner v-if="loading" message="Loading profiles..." />
    <div v-else-if="profiles.length === 0" class="alert alert-info">No profiles found. Try clearing filters.</div>

    <div class="row g-4">
      <div v-for="profile in profiles" :key="profile.id" class="col-md-6 col-xl-4">
        <div class="card h-100 border-0 shadow-sm rounded-4 overflow-hidden" :class="profile.is_boosted ? 'boosted-card' : ''">
          <div class="card-body">
            <div class="d-flex gap-3 align-items-center mb-3">
              <img
                  :src="profile.photo ? `http://127.0.0.1:5050${profile.photo}` : avatarUrl(profile.name)"
                  class="rounded-circle object-fit-cover"
                  width="64"
                  height="64"
                />
              <div>
                <h5 class="fw-bold mb-0">
                  {{ profile.name }}, {{ profile.age }}
                  <span v-if="profile.is_verified" class="text-primary" title="Verified profile">✔</span>
                </h5>
                <small class="text-muted">📍 {{ profile.location }}</small>
              </div>
            </div>
            <div class="d-flex flex-wrap gap-1 mb-2">
              <span class="badge bg-success">{{ profile.match_score }}% match</span>
              <span v-if="profile.is_premium" class="badge text-bg-warning">Premium</span>
              <span v-if="profile.is_boosted" class="badge text-bg-danger">Boosted</span>
              <span v-if="profile.is_verified" class="badge text-bg-primary">Verified</span>
            </div>
            <p class="small">{{ profile.bio }}</p>
            <p class="small text-muted mb-2">🎯 {{ profile.relationship_goal }} • 💼 {{ profile.occupation || 'N/A' }} • 🎓 {{ profile.education || 'N/A' }}</p>
            <div class="mb-3 d-flex flex-wrap gap-1">
              <span v-for="interest in profile.interests" :key="interest" class="badge text-bg-light">{{ interest }}</span>
            </div>
            <div class="d-flex gap-2 flex-wrap">
              <button class="btn btn-sm btn-outline-secondary" @click="act(profile, 'pass')">Pass</button>
              <button class="btn btn-sm btn-outline-danger" @click="act(profile, 'dislike')">Dislike</button>
              <button class="btn btn-sm btn-primary" @click="act(profile, 'like')">Like</button>
              <button class="btn btn-sm" :class="profile.is_favorite ? 'btn-warning' : 'btn-outline-warning'" @click="toggleFavorite(profile)">★</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, reactive, ref } from 'vue'
import { apiFetch } from '../services/api'
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
const loading = ref(false)
const boosting = ref(false)
const profiles = ref([])
const errorMsg = ref('')
const notice = ref('')
const filters = reactive({ q:'', location:'', gender:'', interest:'', min_age:'', max_age:'', relationship_goal:'', verified:false, premium:false, boosted:false, sort:'score' })
function avatarUrl(name) { return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=6f42c1&color=fff` }
function resetFilters() { Object.assign(filters, { q:'', location:'', gender:'', interest:'', min_age:'', max_age:'', relationship_goal:'', verified:false, premium:false, boosted:false, sort:'score' }); loadProfiles() }
async function loadProfiles() {
  errorMsg.value = ''; notice.value = ''; loading.value = true
  try {
    const params = new URLSearchParams()
    Object.entries(filters).forEach(([k,v]) => { if (v !== '' && v !== null && v !== false) params.append(k, v === true ? '1' : v) })
    const data = await apiFetch(`/api/profiles?${params}`)
    profiles.value = data.profiles
  } catch (error) { errorMsg.value = error.message } finally { loading.value = false }
}
async function act(profile, action) {
  try {
    const data = await apiFetch(`/api/profiles/${profile.id}/action`, { method:'POST', body: JSON.stringify({ action }) })
    profile.my_action = action
    notice.value = data.matched ? `It's a mutual match with ${profile.name}! Check Matches or Messages.` : data.message
  } catch (error) { errorMsg.value = error.message }
}
async function toggleFavorite(profile) {
  try {
    await apiFetch(`/api/profiles/${profile.id}/favorite`, { method: profile.is_favorite ? 'DELETE' : 'POST' })
    profile.is_favorite = !profile.is_favorite
  } catch (error) { errorMsg.value = error.message }
}
async function boostProfile() {
  errorMsg.value = ''; notice.value = ''; boosting.value = true
  try {
    const data = await apiFetch('/api/profile/boost', { method:'POST' })
    authStore.setUser(data.user)
    notice.value = data.message
    await loadProfiles()
  } catch (error) { errorMsg.value = error.message } finally { boosting.value = false }
}
onMounted(loadProfiles)
</script>
<style scoped>
.boosted-card { border: 2px solid rgba(220,53,69,.35) !important; }
</style>
