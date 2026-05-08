<template>
  <div class="container py-4">
    <div class="mb-4">
      <h1 class="fw-bold mb-1">Your Favorites ⭐</h1>
      <p class="text-muted mb-0">
        Profiles you bookmarked to revisit later.
      </p>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else-if="favorites.length === 0" class="text-center py-5">
      <h4>No favorites yet</h4>
      <p class="text-muted">
        Go to Browse and click the star button on profiles you want to save.
      </p>
      <router-link to="/dashboard" class="btn btn-primary">
        Browse Profiles
      </router-link>
    </div>

    <div v-else class="row g-4">
      <div
        v-for="profile in favorites"
        :key="profile.id"
        class="col-md-6 col-xl-4"
      >
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-body">
            <div class="d-flex gap-3 align-items-center mb-3">
              <img
                :src="imageUrl(profile)"
                class="rounded-circle object-fit-cover"
                width="72"
                height="72"
                alt="Profile picture"
              />

              <div>
                <h5 class="fw-bold mb-0">
                  {{ profile.name }}, {{ profile.age }}
                  <span
                    v-if="profile.is_verified"
                    class="text-primary"
                    title="Verified profile"
                  >
                    ✔
                  </span>
                </h5>

                <small class="text-muted">
                  📍 {{ profile.location }}
                </small>
              </div>
            </div>

            <div class="mb-2 d-flex flex-wrap gap-1">
              <span
                v-if="profile.match_score !== undefined"
                class="badge bg-success"
              >
                {{ profile.match_score }}% match
              </span>

              <span
                v-if="profile.is_premium"
                class="badge text-bg-warning"
              >
                Premium
              </span>

              <span
                v-if="profile.is_boosted"
                class="badge text-bg-danger"
              >
                Boosted
              </span>

              <span
                v-if="profile.is_verified"
                class="badge text-bg-primary"
              >
                Verified
              </span>
            </div>

            <p class="small mb-2">
              {{ profile.bio }}
            </p>

            <p class="small text-muted mb-2">
              🎯 {{ profile.relationship_goal || 'N/A' }}
              • 💼 {{ profile.occupation || 'N/A' }}
              • 🎓 {{ profile.education || 'N/A' }}
            </p>

            <div class="mb-3 d-flex flex-wrap gap-1">
              <span
                v-for="interest in profile.interests"
                :key="interest"
                class="badge text-bg-light"
              >
                {{ interest }}
              </span>
            </div>

            <div class="d-flex gap-2">
              <button
                class="btn btn-outline-danger btn-sm"
                @click="removeFavorite(profile.id)"
              >
                Remove
              </button>

              <router-link
                to="/messages"
                class="btn btn-primary btn-sm"
              >
                Message
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <p v-if="error" class="text-danger mt-3">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const favorites = ref([])
const loading = ref(true)
const error = ref('')

function avatarUrl(name) {
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'User')}&background=7c3aed&color=fff`
}

function imageUrl(profile) {
  const photo = profile.photo || profile.profile_picture

  if (!photo) {
    return avatarUrl(profile.name)
  }

  if (photo.startsWith('http')) {
    return photo
  }

  return `http://127.0.0.1:5050${photo}`
}

async function loadFavorites() {
  loading.value = true
  error.value = ''

  try {
    const res = await fetch('/api/favorites', {
      credentials: 'include'
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.error || 'Could not load favorites')
    }

    favorites.value = data.favorites || []
  } catch (err) {
    console.error(err)
    error.value = err.message || 'Something went wrong'
  } finally {
    loading.value = false
  }
}

async function removeFavorite(profileId) {
  try {
    const res = await fetch(`/api/profiles/${profileId}/favorite`, {
      method: 'DELETE',
      credentials: 'include'
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.error || 'Could not remove favorite')
    }

    favorites.value = favorites.value.filter(profile => profile.id !== profileId)
  } catch (err) {
    console.error(err)
    error.value = err.message || 'Something went wrong'
  }
}

onMounted(loadFavorites)
</script>
