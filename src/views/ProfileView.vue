<template>
  <div class="row justify-content-center">
    <div class="col-lg-9">
      <div class="card border-0 shadow rounded-4 p-4">
        <h2 class="fw-bold">Edit Profile ⚙️</h2>
        <p class="text-muted">Update your database profile, interests, preferences, photo and visibility.</p>
        <div v-if="notice" class="alert alert-success">{{ notice }}</div>
        <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
        <LoadingSpinner v-if="loading" message="Loading profile..." />
        <form v-else @submit.prevent="saveProfile">
          <div class="d-flex gap-3 align-items-center mb-4">
            <img :src="preview || form.profile_picture || avatarUrl(form.name || 'User')" class="rounded-circle" width="90" height="90" />
            <input type="file" class="form-control" accept="image/*" @change="onFileChange" />
          </div>
          <div class="row g-3">
            <div class="col-md-6"><label class="form-label">First Name</label><input v-model="form.first_name" class="form-control" required /></div>
            <div class="col-md-6"><label class="form-label">Last Name</label><input v-model="form.last_name" class="form-control" required /></div>
            <div class="col-md-3"><label class="form-label">Age</label><input v-model.number="form.age" type="number" min="18" class="form-control" required /></div>
            <div class="col-md-3"><label class="form-label">Gender</label><input v-model="form.gender" class="form-control" /></div>
            <div class="col-md-3"><label class="form-label">Looking For</label><input v-model="form.looking_for" class="form-control" /></div>
            <div class="col-md-3"><label class="form-label">Goal</label><input v-model="form.relationship_goal" class="form-control" /></div>
            <div class="col-md-6"><label class="form-label">Location</label><input v-model="form.location" class="form-control" /></div>
            <div class="col-md-6"><label class="form-label">Preferred Location</label><input v-model="form.preferred_location" class="form-control" /></div>
            <div class="col-md-3"><label class="form-label">Min Age</label><input v-model.number="form.min_age" type="number" class="form-control" /></div>
            <div class="col-md-3"><label class="form-label">Max Age</label><input v-model.number="form.max_age" type="number" class="form-control" /></div>
            <div class="col-md-3"><label class="form-label">Occupation</label><input v-model="form.occupation" class="form-control" /></div>
            <div class="col-md-3"><label class="form-label">Education</label><input v-model="form.education" class="form-control" /></div>
            <div class="col-12"><label class="form-label">Bio</label><textarea v-model="form.bio" rows="3" class="form-control"></textarea></div>
            <div class="col-12"><label class="form-label">Interests (comma separated, min 3)</label><input v-model="interestText" class="form-control" /></div>
            <div class="col-md-4 form-check ms-2"><input id="is_private" v-model="form.is_private" class="form-check-input" type="checkbox" /><label class="form-check-label" for="is_private">Profile is private</label></div>
            <div class="col-md-4 form-check ms-2"><input id="is_premium" v-model="form.is_premium" class="form-check-input" type="checkbox" /><label class="form-check-label" for="is_premium">Premium user features</label></div>
            <div class="col-md-4 form-check ms-2"><input id="is_verified" v-model="form.is_verified" class="form-check-input" type="checkbox" /><label class="form-check-label" for="is_verified">Verified badge</label></div>
            <div class="col-12">
              <div class="alert alert-info mb-0">
                Premium users can use the Boost Profile button on Browse. Boosted and verified profiles receive badges and advanced filter visibility.
              </div>
            </div>
          </div>
          <button class="btn btn-primary mt-4" :disabled="saving">{{ saving ? 'Saving...' : 'Save Profile' }}</button>
        </form>
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
const saving = ref(false)
const errorMsg = ref('')
const notice = ref('')
const uploadFile = ref(null)
const preview = ref('')
const interestText = ref('')
const form = reactive({})
function avatarUrl(name) { return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=6f42c1&color=fff` }
async function loadProfile() {
  loading.value = true
  try {
    const data = await apiFetch('/api/profile')
    Object.assign(form, data.profile)
    interestText.value = data.profile.interests.join(', ')
  } catch(e) { errorMsg.value = e.message } finally { loading.value = false }
}
function onFileChange(event) {
  uploadFile.value = event.target.files[0]
  preview.value = uploadFile.value ? URL.createObjectURL(uploadFile.value) : ''
}
async function saveProfile() {
  errorMsg.value = ''; notice.value = ''
  const interests = interestText.value.split(',').map(x => x.trim()).filter(Boolean)
  if (interests.length < 3) { errorMsg.value = 'Please enter at least 3 interests.'; return }
  saving.value = true
  try {
    const fd = new FormData()
    ;['first_name','last_name','age','gender','looking_for','bio','location','preferred_location','min_age','max_age','relationship_goal','occupation','education','is_private','is_premium','is_verified'].forEach(k => fd.append(k, form[k] ?? ''))
    fd.append('interests', interests.join(','))
    if (uploadFile.value) fd.append('profile_picture', uploadFile.value)
    const data = await apiFetch('/api/profile', { method:'PUT', body: fd })
    Object.assign(form, data.profile)
    authStore.refreshProfile(data.profile)
    notice.value = 'Profile saved.'
  } catch(e) { errorMsg.value = e.message } finally { saving.value = false }
}
onMounted(loadProfile)
</script>
