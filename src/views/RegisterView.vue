<template>
  <div class="row justify-content-center">
    <div class="col-lg-8">
      <div class="card shadow border-0 rounded-4 p-4">
        <h2 class="fw-bold">Create Account 🚀</h2>
        <p class="text-muted">All profile information is saved in the database.</p>
        <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
        <form autocomplete="off" @submit.prevent="handleRegister">
          <div class="row g-3">
            <div class="col-md-6"><label class="form-label">Email</label><input v-model.trim="form.email" name="new-driftdater-email" autocomplete="new-email" type="email" class="form-control" required /></div>
            <div class="col-md-6"><label class="form-label">Username</label><input v-model.trim="form.username" name="new-driftdater-username" autocomplete="off" class="form-control" required /></div>
            <div class="col-md-6"><label class="form-label">Password</label><input v-model="form.password" name="new-driftdater-password" autocomplete="new-password" type="password" minlength="6" class="form-control" required /></div>
            <div class="col-md-6"><label class="form-label">Date of Birth</label><input v-model="form.dob" type="date" class="form-control" required /></div>
            <div class="col-md-6"><label class="form-label">First Name</label><input v-model.trim="form.firstName" class="form-control" required /></div>
            <div class="col-md-6"><label class="form-label">Last Name</label><input v-model.trim="form.lastName" class="form-control" required /></div>
            <div class="col-md-6"><label class="form-label">Gender</label><select v-model="form.gender" class="form-select" required><option disabled value="">Choose...</option><option>Male</option><option>Female</option><option>Non-binary</option><option>Prefer not to say</option></select></div>
            <div class="col-md-6"><label class="form-label">Looking For</label><select v-model="form.lookingFor" class="form-select" required><option disabled value="">Choose...</option><option>Men</option><option>Women</option><option>Everyone</option></select></div>
            <div class="col-md-6"><label class="form-label">Location</label><input v-model.trim="form.location" class="form-control" placeholder="Kingston, Jamaica" required /></div>
            <div class="col-md-6"><label class="form-label">Preferred Location</label><input v-model.trim="form.preferredLocation" class="form-control" placeholder="Optional" /></div>
            <div class="col-md-3"><label class="form-label">Min Age</label><input v-model.number="form.minAge" type="number" min="18" class="form-control" /></div>
            <div class="col-md-3"><label class="form-label">Max Age</label><input v-model.number="form.maxAge" type="number" min="18" class="form-control" /></div>
            <div class="col-md-6"><label class="form-label">Relationship Goal</label><select v-model="form.relationshipGoal" class="form-select"><option>Friendship</option><option>Dating</option><option>Long-term</option><option>Networking</option></select></div>
            <div class="col-md-6"><label class="form-label">Occupation</label><input v-model.trim="form.occupation" class="form-control" placeholder="Custom field 1" /></div>
            <div class="col-md-6"><label class="form-label">Education</label><input v-model.trim="form.education" class="form-control" placeholder="Custom field 2" /></div>
            <div class="col-12"><label class="form-label">Bio</label><textarea v-model.trim="form.bio" rows="3" class="form-control" required></textarea></div>
            <div class="col-12">
              <label class="form-label">Interests / Hobbies (minimum 3)</label>
              <div class="d-flex flex-wrap gap-2">
                <button v-for="interest in interestOptions" :key="interest" type="button" class="btn btn-sm" :class="form.interests.includes(interest) ? 'btn-primary' : 'btn-outline-primary'" @click="toggleInterest(interest)">{{ interest }}</button>
              </div>
            </div>
            <div class="col-md-4 form-check ms-2"><input id="private" v-model="form.isPrivate" class="form-check-input" type="checkbox" /><label for="private" class="form-check-label">Make my profile private</label></div>
            <div class="col-md-4 form-check ms-2"><input id="premium" v-model="form.isPremium" class="form-check-input" type="checkbox" /><label for="premium" class="form-check-label">Premium account</label></div>
            <div class="col-md-4 form-check ms-2"><input id="verified" v-model="form.isVerified" class="form-check-input" type="checkbox" /><label for="verified" class="form-check-label">Verified badge</label></div>
          </div>
          <button class="btn btn-primary w-100 mt-4" :disabled="loading">{{ loading ? 'Creating...' : 'Join DriftDater' }}</button>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const loading = ref(false)
const errorMsg = ref('')
const interestOptions = ['gaming','music','fitness','reading','foodie','travel','art','movies','sports','tech','nature','pets','photography','cooking','theatre','wellness']
const defaults = { email:'', username:'', password:'', firstName:'', lastName:'', dob:'', gender:'', lookingFor:'', location:'', preferredLocation:'', minAge:18, maxAge:35, relationshipGoal:'Friendship', occupation:'', education:'', bio:'', interests:[], isPrivate:false, isPremium:false, isVerified:false }
const form = reactive({ ...defaults })
function toggleInterest(interest) {
  form.interests.includes(interest) ? form.interests.splice(form.interests.indexOf(interest), 1) : form.interests.push(interest)
}
async function handleRegister() {
  errorMsg.value = ''
  if (form.interests.length < 3) { errorMsg.value = 'Select at least 3 interests.'; return }
  loading.value = true
  try {
    await authStore.register({ ...form })
    router.push('/dashboard')
  } catch (error) { errorMsg.value = error.message } finally { loading.value = false }
}

onMounted(async () => {
  Object.assign(form, { ...defaults, interests: [] })
  if (route.query.fresh === '1') await authStore.logout()
})
</script>
