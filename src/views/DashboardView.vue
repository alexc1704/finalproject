<template>
  <div class="dashboard-wrapper">

    <!-- Profile Summary Banner -->
    <div class="profile-banner mb-4" v-if="currentUser">
      <div class="banner-left">
        <img
          :src="currentUser.photo || 'https://ui-avatars.com/api/?name=' + currentUser.name + '&background=6f42c1&color=fff'"
          class="banner-avatar"
        />
        <div>
          <h5 class="mb-0 fw-bold">Welcome back, {{ currentUser.name }}! 👋</h5>
          <p class="mb-0 small text-muted">
            📍 {{ currentUser.location }} &nbsp;|&nbsp;
            🎂 {{ currentUser.age }} years old
          </p>
          <p class="mb-0 small text-muted fst-italic">
            "{{ currentUser.bio }}"
          </p>
        </div>
      </div>
      <router-link to="/profile" class="btn-edit-profile">
        ✏️ Edit Profile
      </router-link>
    </div>

    <!-- Search & Filter Bar -->
    <div class="filter-bar mb-4">
      <div class="filter-input-wrap">
        <span>🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by name or bio..."
          class="filter-input"
        />
      </div>

      <select v-model="ageFilter" class="filter-select">
        <option value="">All Ages</option>
        <option value="18-24">18 - 24</option>
        <option value="25-30">25 - 30</option>
        <option value="31-40">31 - 40</option>
        <option value="40+">40+</option>
      </select>

      <div class="filter-input-wrap">
        <span>📍</span>
        <input
          v-model="locationFilter"
          type="text"
          placeholder="Filter by location..."
          class="filter-input"
        />
      </div>

      <button class="btn-reset" @click="resetFilters">
        ✖ Reset
      </button>
    </div>

    <!-- Stats Row -->
    <div class="stats-row mb-4">
      <div class="stat-card">
        <span class="stat-number">{{ profiles.length }}</span>
        <span class="stat-label">Potential Matches</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">{{ likedCount }}</span>
        <span class="stat-label">Profiles Liked</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">{{ matchCount }}</span>
        <span class="stat-label">Mutual Matches</span>
      </div>
    </div>

    <!-- Browse Section -->
    <h5 class="section-title mb-3">💫 Browse Potential Matches</h5>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="big-spinner"></div>
      <p class="text-muted mt-3">Finding your matches...</p>
    </div>

    <!-- No Results -->
    <div v-else-if="filteredProfiles.length === 0" class="empty-state">
      <p class="display-6">😔</p>
      <p class="text-muted">No profiles match your filters right now.</p>
      <button class="btn-reset mt-2" @click="resetFilters">Clear Filters</button>
    </div>

    <!-- Profile Cards Grid -->
    <div v-else class="profiles-grid">
      <div
        v-for="profile in filteredProfiles"
        :key="profile.id"
        class="profile-card"
        :class="{ 'swiped-like': swipedLike === profile.id,
                  'swiped-pass': swipedPass === profile.id }"
      >
        <!-- Photo -->
        <div class="card-photo-wrap">
          <img
            :src="profile.photo || 'https://ui-avatars.com/api/?name=' + profile.name + '&background=random'"
            class="card-photo"
          />
          <span class="match-badge">⚡ {{ profile.matchScore }}% Match</span>
        </div>

        <!-- Info -->
        <div class="card-body-custom">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h6 class="fw-bold mb-0">{{ profile.name }}, {{ profile.age }}</h6>
              <p class="small text-muted mb-1">📍 {{ profile.location }}</p>
            </div>
          </div>

          <p class="card-bio">{{ profile.bio }}</p>

          <!-- Interests -->
          <div class="interest-chips mb-3">
            <span
              v-for="interest in profile.interests.slice(0, 3)"
              :key="interest"
              class="chip"
            >
              {{ interest }}
            </span>
          </div>

          <!-- Action Buttons -->
          <div class="card-actions">
            <button
              class="btn-pass"
              @click="handlePass(profile.id)"
            >
              👎 Pass
            </button>
            <button
              class="btn-like"
              @click="handleLike(profile.id)"
            >
              💖 Like
            </button>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const loading = ref(false)
const searchQuery = ref('')
const ageFilter = ref('')
const locationFilter = ref('')
const swipedLike = ref(null)
const swipedPass = ref(null)
const likedCount = ref(0)
const matchCount = ref(0)

// Placeholder current user - replace with authStore.user when backend ready
const currentUser = ref({
  name: 'Alex',
  age: 22,
  location: 'Kingston, Jamaica',
  bio: 'Software developer by day, explorer by night.',
  photo: null
})

// Placeholder profiles - replace with API call when backend ready
const profiles = ref([
  {
    id: 1,
    name: 'Alice Wonder',
    age: 23,
    location: 'Kingston, Jamaica',
    bio: 'Love hiking and adventure! Let\'s explore the world together.',
    matchScore: 92,
    interests: ['✈️ Travel', '🏋️ Fitness', '📸 Photography'],
    photo: null
  },
  {
    id: 2,
    name: 'Grace Gamer',
    age: 21,
    location: 'Portmore, Jamaica',
    bio: 'Gamer and coffee enthusiast. Let\'s play!',
    matchScore: 85,
    interests: ['🎮 Gaming', '☕ Coffee', '🎵 Music'],
    photo: null
  },
  {
    id: 3,
    name: 'Carol Cook',
    age: 25,
    location: 'Montego Bay, Jamaica',
    bio: 'Chef and coffee lover. Looking for someone to cook for.',
    matchScore: 78,
    interests: ['🍳 Cooking', '🌿 Nature', '📚 Reading'],
    photo: null
  },
  {
    id: 4,
    name: 'Emma Artist',
    age: 24,
    location: 'Kingston, Jamaica',
    bio: 'Artist and creative soul. Let\'s create art together!',
    matchScore: 74,
    interests: ['🎨 Art', '🎬 Movies', '🎭 Theatre'],
    photo: null
  },
])

// Filter logic
const filteredProfiles = computed(() => {
  return profiles.value.filter(p => {
    const matchesSearch =
      p.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      p.bio.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesLocation =
      !locationFilter.value ||
      p.location.toLowerCase().includes(locationFilter.value.toLowerCase())

    const matchesAge = (() => {
      if (!ageFilter.value) return true
      const age = p.age
      if (ageFilter.value === '18-24') return age >= 18 && age <= 24
      if (ageFilter.value === '25-30') return age >= 25 && age <= 30
      if (ageFilter.value === '31-40') return age >= 31 && age <= 40
      if (ageFilter.value === '40+')   return age > 40
      return true
    })()

    return matchesSearch && matchesLocation && matchesAge
  })
})

function resetFilters() {
  searchQuery.value = ''
  ageFilter.value = ''
  locationFilter.value = ''
}

function handleLike(id) {
  swipedLike.value = id
  likedCount.value++
  setTimeout(() => {
    profiles.value = profiles.value.filter(p => p.id !== id)
    swipedLike.value = null
  }, 500)

  // TODO: call POST /api/matches/like/:id when backend ready
}

function handlePass(id) {
  swipedPass.value = id
  setTimeout(() => {
    profiles.value = profiles.value.filter(p => p.id !== id)
    swipedPass.value = null
  }, 500)

  // TODO: call POST /api/matches/pass/:id when backend ready
}

onMounted(async () => {
  // TODO: replace placeholder data with real API calls
  // loading.value = true
  // const res = await fetch('/api/matches/potential', {
  //   headers: { Authorization: `Bearer ${authStore.token}` }
  // })
  // const data = await res.json()
  // profiles.value = data.profiles
  // currentUser.value = data.currentUser
  // loading.value = false
})
</script>

<style scoped>
.dashboard-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

/* Banner */
.profile-banner {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  border-radius: 16px;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.banner-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
}

.banner-left h5, .banner-left p {
  color: white;
}

.btn-edit-profile {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1.5px solid white;
  border-radius: 10px;
  padding: 8px 16px;
  font-size: 13px;
  text-decoration: none;
  transition: background 0.2s;
}

.btn-edit-profile:hover {
  background: rgba(255,255,255,0.35);
  color: white;
}

/* Filter Bar */
.filter-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-input-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  padding: 8px 12px;
  flex: 1;
  min-width: 160px;
  background: white;
}

.filter-input-wrap:focus-within {
  border-color: #6f42c1;
}

.filter-input {
  border: none;
  outline: none;
  font-size: 13px;
  width: 100%;
  background: transparent;
}

.filter-select {
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 13px;
  outline: none;
  background: white;
  cursor: pointer;
}

.filter-select:focus {
  border-color: #6f42c1;
}

.btn-reset {
  background: #f5f5f5;
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-reset:hover { background: #ececec; }

/* Stats */
.stats-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.stat-card {
  flex: 1;
  min-width: 120px;
  background: white;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  border: 1.5px solid #f0e8ff;
}

.stat-number {
  display: block;
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  font-size: 12px;
  color: #888;
}

/* Section title */
.section-title {
  font-weight: 700;
  color: #333;
}

/* Profiles Grid */
.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.profile-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.07);
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1.5px solid #f0e8ff;
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(111,66,193,0.15);
}

.profile-card.swiped-like {
  transform: translateX(60px) rotate(5deg);
  opacity: 0;
  transition: all 0.4s ease;
}

.profile-card.swiped-pass {
  transform: translateX(-60px) rotate(-5deg);
  opacity: 0;
  transition: all 0.4s ease;
}

/* Card Photo */
.card-photo-wrap {
  position: relative;
}

.card-photo {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.match-badge {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}

/* Card Body */
.card-body-custom {
  padding: 14px;
}

.card-bio {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.interest-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.chip {
  font-size: 11px;
  background: #f3eeff;
  color: #6f42c1;
  padding: 3px 9px;
  border-radius: 20px;
}

/* Action Buttons */
.card-actions {
  display: flex;
  gap: 8px;
}

.btn-like, .btn-pass {
  flex: 1;
  border: none;
  border-radius: 10px;
  padding: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}

.btn-like {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
}

.btn-pass {
  background: #f5f5f5;
  color: #555;
}

.btn-like:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-pass:hover { background: #ececec; }

/* Empty state */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

/* Loading spinner */
.big-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f0e8ff;
  border-top-color: #6f42c1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>