<template>
  <div>
    <h2 class="fw-bold mb-4">Messages 💬</h2>
    <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
    <div class="row g-3">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
          <div class="card-header bg-white fw-bold">Conversations</div>
          <div v-if="loading" class="p-3 text-muted">Loading...</div>
          <button v-for="match in matches" :key="match.id" class="list-group-item list-group-item-action border-0 p-3 text-start" :class="selectedMatch?.id === match.id ? 'active' : ''" @click="selectMatch(match)">
            <div class="d-flex gap-2 align-items-center">
              <img :src="match.other_user.photo || avatarUrl(match.other_user.name)" width="45" height="45" class="rounded-circle" />
              <div class="overflow-hidden">
                <div class="fw-bold">{{ match.other_user.name }}</div>
                <small class="text-truncate d-block" :class="selectedMatch?.id === match.id ? 'text-white-50' : 'text-muted'">{{ match.last_message }}</small>
              </div>
            </div>
          </button>
          <div v-if="!loading && matches.length === 0" class="p-3 text-muted">No conversations yet.</div>
        </div>
      </div>
      <div class="col-md-8">
        <div class="card border-0 shadow-sm rounded-4 chat-card">
          <div v-if="selectedMatch" class="card-header bg-white d-flex align-items-center gap-2">
            <img
                :src="profile.photo ? `http://127.0.0.1:5050${profile.photo}` : avatarUrl(profile.name)"
                class="rounded-circle object-fit-cover"
                width="64"
                height="64"
              />
            <div><div class="fw-bold">{{ selectedMatch.other_user.name }}</div><small class="text-muted">Matched user • replies update automatically</small></div>
          </div>
          <div v-if="selectedMatch" ref="messagesBox" class="card-body messages-box">
            <div v-if="messages.length === 0" class="text-center text-muted my-5">Send the first message.</div>
            <div v-for="msg in messages" :key="msg.id" class="d-flex mb-3" :class="msg.sender_id === authStore.userId ? 'justify-content-end' : 'justify-content-start'">
              <div class="message-bubble" :class="msg.sender_id === authStore.userId ? 'mine' : 'theirs'">
                <div>{{ msg.body }}</div>
                <small>{{ formatTime(msg.created_at) }}</small>
              </div>
            </div>
          </div>
          <form v-if="selectedMatch" class="card-footer bg-white d-flex gap-2" @submit.prevent="sendMessage">
            <input v-model="newMessage" class="form-control" placeholder="Type a message..." />
            <button class="btn btn-primary" :disabled="sending">Send</button>
          </form>
          <div v-else class="card-body text-center text-muted py-5">Choose a conversation to start messaging.</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { apiFetch } from '../services/api'
const route = useRoute()
const authStore = useAuthStore()
const matches = ref([])
const selectedMatch = ref(null)
const messages = ref([])
const newMessage = ref('')
const loading = ref(false)
const sending = ref(false)
const errorMsg = ref('')
const messagesBox = ref(null)
let poller = null
function avatarUrl(name) { return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=6f42c1&color=fff` }
function formatTime(date) { return new Date(date).toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' }) }
async function loadMatches() {
  loading.value = true; errorMsg.value = ''
  try {
    matches.value = (await apiFetch('/api/matches')).matches
    const queryMatch = Number(route.query.match)
    selectedMatch.value = matches.value.find(m => m.id === queryMatch) || matches.value[0] || null
    if (selectedMatch.value) await loadMessages()
  } catch (e) { errorMsg.value = e.message } finally { loading.value = false }
}
async function selectMatch(match) { selectedMatch.value = match; await loadMessages() }
async function loadMessages() {
  if (!selectedMatch.value) return
  try {
    messages.value = (await apiFetch(`/api/messages/${selectedMatch.value.id}`)).messages
    await nextTick(); scrollDown()
  } catch (e) { errorMsg.value = e.message }
}
async function sendMessage() {
  const body = newMessage.value.trim()
  if (!body || !selectedMatch.value) return
  sending.value = true
  try {
    const data = await apiFetch('/api/messages', { method:'POST', body: JSON.stringify({ match_id: selectedMatch.value.id, body }) })
    messages.value.push(data.message)
    if (data.auto_reply) {
      messages.value.push(data.auto_reply)
      selectedMatch.value.last_message = data.auto_reply.body
    } else {
      selectedMatch.value.last_message = body
    }
    newMessage.value = ''
    await nextTick(); scrollDown()
  } catch (e) { errorMsg.value = e.message } finally { sending.value = false }
}
function scrollDown() { if (messagesBox.value) messagesBox.value.scrollTop = messagesBox.value.scrollHeight }
onMounted(() => { loadMatches(); poller = setInterval(loadMessages, 5000) })
onUnmounted(() => clearInterval(poller))
</script>
<style scoped>
.chat-card { min-height: 560px; }
.messages-box { height: 430px; overflow-y: auto; background: #faf7ff; }
.message-bubble { max-width: 70%; padding: .7rem .9rem; border-radius: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
.message-bubble.mine { background: linear-gradient(135deg,#6f42c1,#e83e8c); color: white; border-bottom-right-radius: .25rem; }
.message-bubble.theirs { background: white; color: #222; border-bottom-left-radius: .25rem; }
.message-bubble small { opacity: .75; display: block; margin-top: .25rem; }
</style>
