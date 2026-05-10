<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-1">Your Matches 💞</h2>
        <p class="text-muted mb-0">Only mutual likes become matches.</p>
      </div>
      <span class="badge bg-primary fs-6">{{ matches.length }} Matches</span>
    </div>

    <div v-if="errorMsg" class="alert alert-danger">
      {{ errorMsg }}
    </div>

    <LoadingSpinner v-if="loading" message="Loading matches..." />

    <div v-else-if="matches.length === 0" class="alert alert-info">
      No mutual matches yet. Go to Browse and like profiles. Some seeded users already liked you, so liking them back will create matches.
    </div>

    <div v-else class="row g-4">
      <div v-for="item in matches" :key="item.id" class="col-md-6">
        <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
          <div class="d-flex gap-3">
            <img
              :src="imageUrl(item.other_user)"
              class="rounded-circle object-fit-cover flex-shrink-0"
              width="64"
              height="64"
              alt="Profile photo"
            />

            <div class="flex-grow-1">
              <h5 class="fw-bold mb-0">
                {{ item.other_user?.name || 'Unknown User' }}, {{ item.other_user?.age || 'N/A' }}
                <span v-if="item.other_user?.is_verified" class="text-primary" title="Verified profile">✔</span>
              </h5>

              <p class="text-muted small mb-1">
                📍 {{ item.other_user?.location || 'Unknown location' }}
                <span v-if="item.other_user?.match_score !== undefined">
                  • {{ item.other_user.match_score }}% match
                </span>
              </p>

              <p class="small mb-2">
                {{ item.other_user?.bio || 'No bio available.' }}
              </p>

              <p class="small text-muted mb-2">
                Last message: {{ item.last_message || 'Start a conversation' }}
              </p>

              <div class="d-flex gap-2 flex-wrap">
                <router-link class="btn btn-sm btn-primary" :to="`/messages?match=${item.id}`">
                  Message
                </router-link>
                <span v-if="item.other_user?.is_premium" class="badge text-bg-warning align-self-center">Premium</span>
                <span v-if="item.other_user?.is_boosted" class="badge text-bg-danger align-self-center">Boosted</span>
              </div>
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
import LoadingSpinner from '../components/LoadingSpinner.vue'

const matches = ref([])
const loading = ref(false)
const errorMsg = ref('')

function avatarUrl(name) {
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'User')}&background=e83e8c&color=fff`
}

function imageUrl(profile) {
  const photo = profile?.photo || profile?.profile_picture

  if (!photo) {
    return avatarUrl(profile?.name)
  }

  if (photo.startsWith('http')) {
    return photo
  }

  return `http://127.0.0.1:5050${photo}`
}

async function loadMatches() {
  loading.value = true
  errorMsg.value = ''

  try {
    const data = await apiFetch('/api/matches')
    console.log('MATCHES RESPONSE:', data)

    matches.value = Array.isArray(data.matches) ? data.matches : []
  } catch (e) {
    console.error('MATCHES ERROR:', e)
    errorMsg.value = e.message || 'Could not load matches'
    matches.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadMatches)
</script>
