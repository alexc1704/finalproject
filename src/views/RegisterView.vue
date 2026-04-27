<template>
  <div class="register-wrapper">

    <!-- Left Panel -->
    <div class="register-left d-none d-md-flex">
      <div class="left-content">
        <h1 class="display-4 fw-bold text-white">✨</h1>
        <h2 class="text-white fw-bold mt-3">Start Your Story</h2>
        <p class="text-white-50 mt-2">
          Join thousands of people finding meaningful connections every day.
        </p>

        <div class="features mt-4">
          <div class="feature-item">✅ Smart matching algorithm</div>
          <div class="feature-item">✅ Real-time messaging</div>
          <div class="feature-item">✅ Find people near you</div>
        </div>
      </div>
    </div>

    <!-- Right Panel - Form -->
    <div class="register-right">
      <div class="form-box">

        <div class="mb-4">
          <h3 class="fw-bold">Create Account 🚀</h3>
          <p class="text-muted small">Fill in your details to get started</p>
        </div>

        <!-- Error/Success -->
        <div v-if="errorMsg" class="alert-custom alert-error">
          ⚠️ {{ errorMsg }}
        </div>
        <div v-if="successMsg" class="alert-custom alert-success">
          🎉 {{ successMsg }}
        </div>

        <!-- Step Indicator -->
        <div class="steps mb-4">
          <div :class="['step', step >= 1 ? 'active' : '']">1</div>
          <div class="step-line"></div>
          <div :class="['step', step >= 2 ? 'active' : '']">2</div>
          <div class="step-line"></div>
          <div :class="['step', step >= 3 ? 'active' : '']">3</div>
        </div>

        <!-- Step 1: Account Info -->
        <div v-if="step === 1">
          <p class="step-label">Account Info</p>

          <div class="input-group-custom mb-3">
            <span class="input-icon">✉️</span>
            <input v-model="form.email" type="email"
              placeholder="Email address" class="custom-input" />
          </div>

          <div class="input-group-custom mb-3">
            <span class="input-icon">👤</span>
            <input v-model="form.username" type="text"
              placeholder="Username" class="custom-input" />
          </div>

          <div class="input-group-custom mb-3">
            <span class="input-icon">🔒</span>
            <input v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Password" class="custom-input" />
            <span class="input-toggle"
              @click="showPassword = !showPassword">
              {{ showPassword ? '🙈' : '👁️' }}
            </span>
          </div>

          <button class="btn-next w-100" @click="nextStep">
            Next →
          </button>
        </div>

        <!-- Step 2: Personal Info -->
        <div v-if="step === 2">
          <p class="step-label">Personal Info</p>

          <div class="row g-2 mb-3">
            <div class="col-6">
              <div class="input-group-custom">
                <input v-model="form.firstName" type="text"
                  placeholder="First Name" class="custom-input" />
              </div>
            </div>
            <div class="col-6">
              <div class="input-group-custom">
                <input v-model="form.lastName" type="text"
                  placeholder="Last Name" class="custom-input" />
              </div>
            </div>
          </div>

          <div class="input-group-custom mb-3">
            <span class="input-icon">🎂</span>
            <input v-model="form.dob" type="date"
              class="custom-input" />
          </div>

          <div class="input-group-custom mb-3">
            <span class="input-icon">⚧️</span>
            <select v-model="form.gender" class="custom-input">
              <option value="" disabled>Select gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Non-binary</option>
              <option>Prefer not to say</option>
            </select>
          </div>

          <div class="input-group-custom mb-3">
            <span class="input-icon">💞</span>
            <select v-model="form.lookingFor" class="custom-input">
              <option value="" disabled>Looking for...</option>
              <option>Men</option>
              <option>Women</option>
              <option>Everyone</option>
            </select>
          </div>

          <div class="d-flex gap-2">
            <button class="btn-back w-50" @click="step = 1">← Back</button>
            <button class="btn-next w-50" @click="nextStep">Next →</button>
          </div>
        </div>

        <!-- Step 3: Profile Details -->
        <div v-if="step === 3">
          <p class="step-label">Your Profile</p>

          <div class="input-group-custom mb-3">
            <span class="input-icon">📍</span>
            <input v-model="form.location" type="text"
              placeholder="Your location (e.g. Kingston, JA)"
              class="custom-input" />
          </div>

          <div class="input-group-custom mb-3">
            <span class="input-icon">📝</span>
            <textarea v-model="form.bio"
              placeholder="Write a short bio..."
              class="custom-input" rows="3"
              style="resize:none;"></textarea>
          </div>

          <div class="mb-3">
            <p class="small text-muted mb-2">
              🎯 Pick your interests (min 3)
            </p>
            <div class="interests-grid">
              <span
                v-for="interest in interestOptions"
                :key="interest"
                :class="['interest-tag',
                  form.interests.includes(interest) ? 'selected' : '']"
                @click="toggleInterest(interest)"
              >
                {{ interest }}
              </span>
            </div>
          </div>

          <div class="d-flex gap-2">
            <button class="btn-back w-50" @click="step = 2">← Back</button>
            <button class="btn-register w-50"
              @click="handleRegister" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              <span v-else>Join Now 🎉</span>
            </button>
          </div>
        </div>

        <p class="text-center mt-4 small text-muted">
          Already have an account?
          <router-link to="/login"
            class="fw-bold text-decoration-none link-purple">
            Login here
          </router-link>
        </p>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const step = ref(1)
const showPassword = ref(false)
const errorMsg = ref('')
const successMsg = ref('')
const loading = ref(false)

const form = reactive({
  email: '',
  username: '',
  password: '',
  firstName: '',
  lastName: '',
  dob: '',
  gender: '',
  lookingFor: '',
  location: '',
  bio: '',
  interests: []
})

const interestOptions = [
  '🎮 Gaming', '🎵 Music', '🏋️ Fitness', '📚 Reading',
  '🍕 Foodie', '✈️ Travel', '🎨 Art', '🎬 Movies',
  '🏄 Sports', '💻 Tech', '🌿 Nature', '🐾 Pets',
  '📸 Photography', '🍳 Cooking', '🎭 Theatre', '🧘 Wellness'
]

function toggleInterest(interest) {
  const idx = form.interests.indexOf(interest)
  if (idx === -1) {
    form.interests.push(interest)
  } else {
    form.interests.splice(idx, 1)
  }
}

function nextStep() {
  errorMsg.value = ''

  if (step.value === 1) {
    if (!form.email || !form.username || !form.password) {
      errorMsg.value = 'Please fill in all fields.'
      return
    }
    if (form.password.length < 6) {
      errorMsg.value = 'Password must be at least 6 characters.'
      return
    }
  }

  if (step.value === 2) {
    if (!form.firstName || !form.lastName || !form.dob || !form.gender) {
      errorMsg.value = 'Please fill in all fields.'
      return
    }
  }

  step.value++
}

async function handleRegister() {
  errorMsg.value = ''

  if (!form.location || !form.bio) {
    errorMsg.value = 'Please fill in your location and bio.'
    return
  }

  if (form.interests.length < 3) {
    errorMsg.value = 'Please select at least 3 interests.'
    return
  }

  loading.value = true

  try {
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })

    const data = await response.json()

    if (response.ok) {
      successMsg.value = 'Account created! Redirecting to login...'
      setTimeout(() => router.push('/login'), 2000)
    } else {
      errorMsg.value = data.message || 'Registration failed.'
    }

  } catch (err) {
    errorMsg.value = 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-wrapper {
  display: flex;
  min-height: 90vh;
  border-radius: 20px;
  overflow: hidden;
  max-width: 900px;
  margin: 40px auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}

.register-left {
  flex: 1;
  background: linear-gradient(135deg, #e83e8c, #6f42c1);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.left-content { text-align: center; }

.feature-item {
  color: rgba(255,255,255,0.85);
  margin: 8px 0;
  font-size: 14px;
}

.register-right {
  flex: 1;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  overflow-y: auto;
}

.form-box {
  width: 100%;
  max-width: 360px;
}

/* Step indicator */
.steps {
  display: flex;
  align-items: center;
  justify-content: center;
}

.step {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e0e0e0;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: bold;
  transition: all 0.3s;
}

.step.active {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
}

.step-line {
  flex: 1;
  height: 2px;
  background: #e0e0e0;
  margin: 0 6px;
}

.step-label {
  font-weight: 600;
  color: #6f42c1;
  margin-bottom: 16px;
  font-size: 14px;
}

/* Inputs */
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
  font-size: 15px;
}

.input-toggle {
  cursor: pointer;
  margin-left: auto;
}

.custom-input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 14px;
  background: transparent;
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

.interest-tag:hover {
  border-color: #6f42c1;
}

/* Alerts */
.alert-custom {
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13px;
  margin-bottom: 16px;
}

.alert-error {
  background: #fff0f3;
  color: #c0392b;
  border: 1px solid #f5c6cb;
}

.alert-success {
  background: #f0fff4;
  color: #27ae60;
  border: 1px solid #c3e6cb;
}

/* Buttons */
.btn-next, .btn-register {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 11px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}

.btn-next:hover, .btn-register:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-back {
  background: #f5f5f5;
  color: #555;
  border: none;
  border-radius: 12px;
  padding: 11px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-back:hover { background: #ececec; }

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 15px;
  height: 15px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.link-purple { color: #6f42c1; }
</style>