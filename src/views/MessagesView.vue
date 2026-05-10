<template>
  <div>
    <h2 class="fw-bold mb-4">Messages 💬</h2>

    <div v-if="errorMsg" class="alert alert-danger">
      {{ errorMsg }}
    </div>

    <div class="row g-3">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
          <div class="card-header bg-white fw-bold">Conversations</div>

          <div v-if="loading" class="p-3 text-muted">
            Loading conversations...
          </div>

          <div v-else-if="matches.length === 0" class="p-3 text-muted">
            No conversations yet. Go to Browse, like profiles, and create a mutual match first.
          </div>

          <div v-else class="list-group list-group-flush">
            <button
              v-for="match in matches"
              :key="match.id"
              class="list-group-item list-group-item-action border-0 p-3 text-start"
              :class="selectedMatch?.id === match.id ? 'active' : ''"
              @click="selectMatch(match)"
            >
              <div class="d-flex gap-2 align-items-center">
                <img
                  :src="imageUrl(match.other_user)"
                  width="45"
                  height="45"
                  class="rounded-circle object-fit-cover flex-shrink-0"
                  alt="Profile photo"
                />

                <div class="overflow-hidden flex-grow-1">
                  <div class="fw-bold">
                    {{ match.other_user?.name || 'Unknown User' }}
                  </div>
                  <small
                    class="text-truncate d-block"
                    :class="selectedMatch?.id === match.id ? 'text-white-50' : 'text-muted'"
                  >
                    {{ match.last_message || 'Start a conversation' }}
                  </small>
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <div class="card border-0 shadow-sm rounded-4 chat-card">
          <div v-if="selectedMatch" class="card-header bg-white d-flex align-items-center gap-2">
            <img
              :src="imageUrl(selectedMatch.other_user)"
              class="rounded-circle object-fit-cover"
              width="54"
              height="54"
              alt="Profile photo"
            />

            <div>
              <div class="fw-bold">
                {{ selectedMatch.other_user?.name || 'Unknown User' }}
              </div>
              <small class="text-muted">Matched user • messages saved to database</small>
            </div>
          </div>

          <div v-if="selectedMatch" ref="messagesBox" class="card-body messages-box">
            <div v-if="messagesLoading" class="text-center text-muted my-5">
              Loading messages...
            </div>

            <div v-else-if="messages.length === 0" class="text-center text-muted my-5">
              Send the first message.
            </div>

            <template v-else>
              <div
                v-for="msg in messages"
                :key="msg.id"
                class="d-flex mb-3"
                :class="Number(msg.sender_id) === Number(authStore.userId) ? 'justify-content-end' : 'justify-content-start'"
              >
                <div
                  class="message-bubble"
                  :class="Number(msg.sender_id) === Number(authStore.userId) ? 'mine' : 'theirs'"
                >
                  <div>{{ msg.body }}</div>
                  <small>{{ formatTime(msg.created_at) }}</small>
                </div>
              </div>
            </template>
          </div>

          <form v-if="selectedMatch" class="card-footer bg-white d-flex gap-2" @submit.prevent="sendMessage">
            <input v-model="newMessage" class="form-control" placeholder="Type a message..." />
            <button class="btn btn-primary" :disabled="sending || !newMessage.trim()">
              {{ sending ? 'Sending...' : 'Send' }}
            </button>
          </form>

          <div v-else class="card-body text-center text-muted py-5">
            Choose a conversation to start messaging.
          </div>
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
const messagesLoading = ref(false)
const sending = ref(false)
const errorMsg = ref('')
const messagesBox = ref(null)
let poller = null

function avatarUrl(name) {
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'User')}&background=6f42c1&color=fff`
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

function formatTime(date) {
  if (!date) return ''
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

async function loadMatches() {
  loading.value = true
  errorMsg.value = ''

  try {
    const data = await apiFetch('/api/matches')
    console.log('MESSAGES MATCHES RESPONSE:', data)

    matches.value = Array.isArray(data.matches) ? data.matches : []

    const queryMatch = Number(route.query.match)
    selectedMatch.value = matches.value.find(m => Number(m.id) === queryMatch) || matches.value[0] || null

    if (selectedMatch.value) {
      await loadMessages()
    } else {
      messages.value = []
    }
  } catch (e) {
    console.error('MESSAGES MATCHES ERROR:', e)
    errorMsg.value = e.message || 'Could not load conversations'
    matches.value = []
    selectedMatch.value = null
  } finally {
    loading.value = false
  }
}

async function selectMatch(match) {
  selectedMatch.value = match
  await loadMessages()
}

async function loadMessages() {
  if (!selectedMatch.value) return

  messagesLoading.value = true
  errorMsg.value = ''

  try {
    const data = await apiFetch(`/api/messages/${selectedMatch.value.id}`)
    console.log('MESSAGES RESPONSE:', data)

    messages.value = Array.isArray(data.messages) ? data.messages : []
    await nextTick()
    scrollDown()
  } catch (e) {
    console.error('MESSAGES ERROR:', e)
    errorMsg.value = e.message || 'Could not load messages'
    messages.value = []
  } finally {
    messagesLoading.value = false
  }
}

async function sendMessage() {
  const body = newMessage.value.trim()
  if (!body || !selectedMatch.value) return

  sending.value = true
  errorMsg.value = ''

  try {
    const data = await apiFetch('/api/messages', {
      method: 'POST',
      body: JSON.stringify({
        match_id: selectedMatch.value.id,
        body
      })
    })

    if (data.message) {
      messages.value.push(data.message)
    }

    if (data.auto_reply) {
      messages.value.push(data.auto_reply)
      selectedMatch.value.last_message = data.auto_reply.body
    } else {
      selectedMatch.value.last_message = body
    }

    newMessage.value = ''
    await nextTick()
    scrollDown()
  } catch (e) {
    console.error('SEND MESSAGE ERROR:', e)
    errorMsg.value = e.message || 'Could not send message'
  } finally {
    sending.value = false
  }
}

function scrollDown() {
  if (messagesBox.value) {
    messagesBox.value.scrollTop = messagesBox.value.scrollHeight
  }
}

onMounted(() => {
  loadMatches()
  poller = setInterval(() => {
    if (selectedMatch.value) loadMessages()
  }, 5000)
})

onUnmounted(() => {
  if (poller) clearInterval(poller)
})
</script>

<style scoped>
.chat-card {
  min-height: 560px;
}

.messages-box {
  height: 430px;
  overflow-y: auto;
  background: #faf7ff;
}

.message-bubble {
  max-width: 70%;
  padding: .7rem .9rem;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,.08);
}

.message-bubble.mine {
  background: linear-gradient(135deg,#6f42c1,#e83e8c);
  color: white;
  border-bottom-right-radius: .25rem;
}

.message-bubble.theirs {
  background: white;
  color: #222;
  border-bottom-left-radius: .25rem;
}

.message-bubble small {
  opacity: .75;
  display: block;
  margin-top: .25rem;
}
</style>
