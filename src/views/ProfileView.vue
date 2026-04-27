<template>
  <div class="profile-wrapper">

    <!-- Profile Header Banner -->
    <div class="profile-banner">
      <div class="banner-bg"></div>
      <div class="banner-content">

        <!-- Avatar Upload -->
        <div class="avatar-section">
          <div class="avatar-wrap">
            <img
              :src="previewPhoto ||
                'https://ui-avatars.com/api/?name=' +
                form.firstName + '+' + form.lastName +
                '&background=6f42c1&color=fff&size=200'"
              class="profile-avatar"
            />
            <label class="avatar-upload-btn" for="photoInput">
              📷
            </label>
            <input
              id="photoInput"
              type="file"
              accept="image/*"
              class="d-none"
              @change="handlePhotoUpload"
            />
          </div>
          <div class="avatar-info">
            <h4 class="fw-bold text-white mb-0">
              {{ form.firstName }} {{ form.lastName }}
            </h4>
            <p class="text-white-50 small mb-0">
              📍 {{ form.location || 'No location set' }}
            </p>
            <span :class="['visibility-badge',
              form.isPublic ? 'public' : 'private']">
              {{ form.isPublic ? '🌍 Public Profile' : '🔒 Private Profile' }}
            </span>
          </div>
        </div>

        <!-- Edit Toggle -->
        <button
          class="btn-toggle-edit"
          @click="toggleEdit"
        >
          {{ isEditing ? '✕ Cancel' : '✏️ Edit Profile' }}
        </button>

      </div>
    </div>

    <!-- Success / Error -->
    <div v-if="successMsg" class="alert-custom alert-success mx-4 mt-3">
      ✅ {{ successMsg }}
    </div>
    <div v-if="errorMsg" class="alert-custom alert-error mx-4 mt-3">
      ⚠️ {{ errorMsg }}
    </div>

    <!-- Profile Body -->
    <div class="profile-body">

      <!-- Left Column -->
      <div class="profile-left">

        <!-- Basic Info Card -->
        <div class="info-card">
          <div class="card-title-row">
            <h6 class="card-section-title">👤 Basic Info</h6>
          </div>

          <div class="info-grid">

            <div class="info-field">
              <label>First Name</label>
              <input
                v-if="isEditing"
                v-model="form.firstName"
                class="profile-input"
                placeholder="First Name"
              />
              <p v-else class="info-value">{{ form.firstName }}</p>
            </div>

            <div class="info-field">
              <label>Last Name</label>
              <input
                v-if="isEditing"
                v-model="form.lastName"
                class="profile-input"
                placeholder="Last Name"
              />
              <p v-else class="info-value">{{ form.lastName }}</p>
            </div>

            <div class="info-field">
              <label>Age</label>
              <input
                v-if="isEditing"
                v-model="form.age"
                type="number"
                class="profile-input"
                placeholder="Age"
              />
              <p v-else class="info-value">{{ form.age }}</p>
            </div>

            <div class="info-field">
              <label>Gender</label>
              <select
                v-if="isEditing"
                v-model="form.gender"
                class="profile-input"
              >
                <option>Male</option>
                <option>Female</option>
                <option>Non-binary</option>
                <option>Prefer not to say</option>
              </select>
              <p v-else class="info-value">{{ form.gender }}</p>
            </div>

            <div class="info-field full-width">
              <label>Location</label>
              <input
                v-if="isEditing"
                v-model="form.location"
                class="profile-input"
                placeholder="e.g. Kingston, Jamaica"
              />
              <p v-else class="info-value">📍 {{ form.location }}</p>
            </div>

            <div class="info-field full-width">
              <label>Looking For</label>
              <select
                v-if="isEditing"
                v-model="form.lookingFor"
                class="profile-input"
              >
                <option>Men</option>
                <option>Women</option>
                <option>Everyone</option>
              </select>
              <p v-else class="info-value">💞 {{ form.lookingFor }}</p>
            </div>

          </div>
        </div>

        <!-- Visibility Card -->
        <div class="info-card">
          <h6 class="card-section-title">🔒 Profile Visibility</h6>
          <div class="visibility-toggle">
            <div>
              <p class="mb-0 fw-bold small">
                {{ form.isPublic ? 'Public' : 'Private' }}
              </p>
              <p class="mb-0 text-muted" style="font-size:12px">
                {{
                  form.isPublic
                    ? 'Anyone can find your profile'
                    : 'Only matches can see you'
                }}
              </p>
            </div>
            <div
              :class="['toggle-switch', form.isPublic ? 'on' : '']"
              @click="isEditing ? form.isPublic = !form.isPublic : null"
            >
              <div class="toggle-knob"></div>
            </div>
          </div>
        </div>

        <!-- Stats Card -->
        <div class="info-card">
          <h6 class="card-section-title">📊 Your Stats</h6>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-num">{{ stats.matches }}</span>
              <span class="stat-lbl">Matches</span>
            </div>
            <div class="stat-item">
              <span class="stat-num">{{ stats.liked }}</span>
              <span class="stat-lbl">Liked</span>
            </div>
            <div class="stat-item">
              <span class="stat-num">{{ stats.messages }}</span>
              <span class="stat-lbl">Messages</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column -->
      <div class="profile-right">

        <!-- Bio Card -->
        <div class="info-card">
          <h6 class="card-section-title">📝 About Me</h6>
          <textarea
            v-if="isEditing"
            v-model="form.bio"
            class="profile-input"
            rows="4"
            placeholder="Write something about yourself..."
            style="resize: none;"
          ></textarea>
          <p v-else class="info-value bio-text">
            {{ form.bio || 'No bio yet.' }}
          </p>
        </div>

        <!-- Interests Card -->
        <div class="info-card">
          <h6 class="card-section-title">🎯 Interests</h6>
          <p class="text-muted small mb-3" v-if="isEditing">
            Select at least 3 interests
          </p>

          <div class="interests-grid">
            <span
              v-for="interest in interestOptions"
              :key="interest"
              :class="['interest-tag',
                form.interests.includes(interest) ? 'selected' : '',
                !isEditing && !form.interests.includes(interest)
                  ? 'hidden-tag' : '']"
              @click="isEditing ? toggleInterest(interest) : null"
            >
              {{ interest }}
            </span>
          </div>
        </div>

        <!-- Preferences Card -->
        <div class="info-card">
          <h6 class="card-section-title">⚙️ Match Preferences</h6>

          <div class="info-field mb-3">
            <label>Age Range</label>
            <div class="d-flex gap-2 align-items-center">
              <input
                v-if="isEditing"
                v-model="form.ageMin"
                type="number"
                class="profile-input"
                placeholder="Min"
                style="width: 80px;"
              />
              <span v-if="isEditing" class="text-muted">to</span>
              <input
                v-if="isEditing"
                v-model="form.ageMax"
                type="number"
                class="profile-input"
                placeholder="Max"
                style="width: 80px;"
              />
              <p v-if="!isEditing" class="info-value mb-0">
                {{ form.ageMin }} – {{ form.ageMax }} years old
              </p>
            </div>
          </div>

          <div class="info-field">
            <label>Max Distance</label>
            <div v-if="isEditing">
              <input
                v-model="form.maxDistance"
                type="range"
                min="5"
                max="100"
                class="w-100"
              />
              <p class="small text-muted mt-1">
                {{ form.maxDistance }} km away
              </p>
            </div>
            <p v-else class="info-value mb-0">
              📍 Within {{ form.maxDistance }} km
            </p>
          </div>
        </div>

        <!-- Save Button -->
        <button
          v-if="isEditing"
          class="btn-save w-100"
          @click="saveProfile"
          :disabled="saving"
        >
          <span v-if="saving" class="spinner"></span>
          <span v-else>💾 Save Changes</span>
        </button>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const isEditing = ref(false)
const saving = ref(false)
const successMsg = ref('')
const errorMsg = ref('')
const previewPhoto = ref(null)

// Placeholder data - replace with authStore.user when backend ready
const form = reactive({
  firstName: 'Alex',
  lastName: 'Johnson',
  age: 22,
  gender: 'Male',
  location: 'Kingston, Jamaica',
  lookingFor: 'Everyone',
  bio: 'Software developer by day, explorer by night. Looking for someone to share adventures with! 🌍',
  interests: ['💻 Tech', '✈️ Travel', '🎵 Music', '🏋️ Fitness'],
  isPublic: true,
  ageMin: 18,
  ageMax: 30,
  maxDistance: 25,
  photo: null
})

const stats = reactive({
  matches: 3,
  liked: 12,
  messages: 8
})

const interestOptions = [
  '🎮 Gaming', '🎵 Music', '🏋️ Fitness', '📚 Reading',
  '🍕 Foodie', '✈️ Travel', '🎨 Art', '🎬 Movies',
  '🏄 Sports', '💻 Tech', '🌿 Nature', '🐾 Pets',
  '📸 Photography', '🍳 Cooking', '🎭 Theatre', '🧘 Wellness'
]

function toggleEdit() {
  isEditing.value = !isEditing.value
  successMsg.value = ''
  errorMsg.value = ''
}

function toggleInterest(interest) {
  const idx = form.interests.indexOf(interest)
  if (idx === -1) {
    form.interests.push(interest)
  } else {
    form.interests.splice(idx, 1)
  }
}

function handlePhotoUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (e) => {
    previewPhoto.value = e.target.result
  }
  reader.readAsDataURL(file)
}

async function saveProfile() {
  errorMsg.value = ''
  successMsg.value = ''

  if (!form.firstName || !form.lastName || !form.location) {
    errorMsg.value = 'Please fill in all required fields.'
    return
  }

  if (form.interests.length < 3) {
    errorMsg.value = 'Please select at least 3 interests.'
    return
  }

  saving.value = true

  try {
    // TODO: replace with real API call
    // const response = await fetch('/api/profile', {
    //   method: 'PUT',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     Authorization: `Bearer ${authStore.token}`
    //   },
    //   body: JSON.stringify(form)
    // })
    // const data = await response.json()
    // if (!response.ok) throw new Error(data.message)

    // Simulate save delay
    await new Promise(resolve => setTimeout(resolve, 800))

    successMsg.value = 'Profile updated successfully!'
    isEditing.value = false

  } catch (err) {
    errorMsg.value = 'Failed to save profile. Please try again.'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.profile-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding-bottom: 40px;
}

/* Banner */
.profile-banner {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 24px;
}

.banner-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
}

.banner-content {
  position: relative;
  padding: 30px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-wrap {
  position: relative;
  flex-shrink: 0;
}

.profile-avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid white;
}

.avatar-upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.visibility-badge {
  display: inline-block;
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 20px;
  margin-top: 6px;
}

.visibility-badge.public {
  background: rgba(255,255,255,0.2);
  color: white;
}

.visibility-badge.private {
  background: rgba(0,0,0,0.2);
  color: white;
}

.btn-toggle-edit {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1.5px solid white;
  border-radius: 12px;
  padding: 9px 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-toggle-edit:hover {
  background: rgba(255,255,255,0.35);
}

/* Alerts */
.alert-custom {
  padding: 10px 16px;
  border-radius: 12px;
  font-size: 13px;
  margin-bottom: 4px;
}

.alert-success {
  background: #f0fff4;
  color: #27ae60;
  border: 1px solid #c3e6cb;
}

.alert-error {
  background: #fff0f3;
  color: #c0392b;
  border: 1px solid #f5c6cb;
}

/* Body Layout */
.profile-body {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 20px;
  padding: 0 4px;
}

/* Cards */
.info-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  border: 1.5px solid #f0e8ff;
}

.card-section-title {
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

/* Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.info-field { display: flex; flex-direction: column; gap: 4px; }
.info-field.full-width { grid-column: span 2; }

.info-field label {
  font-size: 11px;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 14px;
  color: #333;
  margin: 0;
  font-weight: 500;
}

.bio-text {
  line-height: 1.6;
  color: #555;
}

/* Inputs */
.profile-input {
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 13px;
  outline: none;
  width: 100%;
  transition: border 0.2s;
  background: #fdfbff;
}

.profile-input:focus { border-color: #6f42c1; }

/* Visibility Toggle */
.visibility-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.toggle-switch {
  width: 46px;
  height: 26px;
  background: #ddd;
  border-radius: 20px;
  position: relative;
  cursor: pointer;
  transition: background 0.3s;
}

.toggle-switch.on { background: linear-gradient(135deg, #6f42c1, #e83e8c); }

.toggle-knob {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: left 0.3s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}

.toggle-switch.on .toggle-knob { left: 23px; }

/* Stats */
.stats-grid {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-size: 26px;
  font-weight: 800;
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-lbl {
  font-size: 11px;
  color: #999;
}

/* Interests */
.interests-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.interest-tag {
  padding: 6px 12px;
  border-radius: 20px;
  border: 1.5px solid #e0e0e0;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.interest-tag.selected {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border-color: transparent;
}

.interest-tag:hover { border-color: #6f42c1; }
.interest-tag.hidden-tag { display: none; }

/* Save Button */
.btn-save {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border: none;
  border-radius: 14px;
  padding: 14px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}

.btn-save:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }

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

@keyframes spin { to { transform: rotate(360deg); } }

/* Responsive */
@media (max-width: 680px) {
  .profile-body { grid-template-columns: 1fr; }
  .info-grid { grid-template-columns: 1fr; }
  .info-field.full-width { grid-column: span 1; }
}
</style>