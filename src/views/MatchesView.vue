<template>
  <div class="matches-wrapper">

    <!-- Header -->
    <div class="matches-header mb-4">
      <div>
        <h4 class="fw-bold mb-0">Your Matches 💞</h4>
        <p class="text-muted small mb-0">
          People who liked you back — start a conversation!
        </p>
      </div>
      <div class="match-count-badge">
        {{ filteredMatches.length }} Matches
      </div>
    </div>

    <!-- Search Bar -->
    <div class="search-wrap mb-4">
      <span>🔍</span>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search your matches..."
        class="search-input"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="big-spinner"></div>
      <p class="text-muted mt-3">Loading your matches...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredMatches.length === 0" class="empty-state">
      <p class="display-5">💔</p>
      <h5 class="fw-bold mt-2">No matches yet</h5>
      <p class="text-muted small">
        Keep liking profiles on the dashboard to get matches!
      </p>
      <router-link to="/dashboard" class="btn-go-browse mt-2">
        Browse Profiles →
      </router-link>
    </div>

    <!-- Matches Grid -->
    <div v-else class="matches-grid">
      <div
        v-for="match in filteredMatches"
        :key="match.id"
        class="match-card"
        @click="openChat(match)"
        :class="{ active: selectedMatch?.id === match.id }"
      >
        <!-- Avatar -->
        <div class="avatar-wrap">
          <img
            :src="match.photo || 'https://ui-avatars.com/api/?name=' +
              match.name + '&background=random&size=128'"
            class="match-avatar"
          />
          <span class="online-dot" v-if="match.isOnline"></span>
        </div>

        <!-- Info -->
        <div class="match-info">
          <h6 class="fw-bold mb-0">{{ match.name }}, {{ match.age }}</h6>
          <p class="small text-muted mb-1">📍 {{ match.location }}</p>
          <p class="match-bio">{{ match.bio }}</p>

          <!-- Shared Interests -->
          <div class="shared-interests">
            <span
              v-for="interest in match.sharedInterests.slice(0, 2)"
              :key="interest"
              class="interest-chip"
            >
              {{ interest }}
            </span>
            <span
              v-if="match.sharedInterests.length > 2"
              class="interest-chip more"
            >
              +{{ match.sharedInterests.length - 2 }} more
            </span>
          </div>
        </div>

        <!-- Right Side -->
        <div class="match-right">
          <span class="match-score">⚡ {{ match.matchScore }}%</span>
          <button
            class="btn-message"
            @click.stop="openChat(match)"
          >
            💬 Message
          </button>
          <p class="match-date">
            Matched {{ match.matchedOn }}
          </p>
        </div>

      </div>
    </div>

    <!-- Chat Drawer -->
    <div :class="['chat-drawer', chatOpen ? 'open' : '']">

      <!-- Drawer Header -->
      <div class="drawer-header" v-if="selectedMatch">
        <div class="d-flex align-items-center gap-3">
          <img
            :src="selectedMatch.photo ||
              'https://ui-avatars.com/api/?name=' +
              selectedMatch.name + '&background=random&size=128'"
            class="drawer-avatar"
          />
          <div>
            <h6 class="fw-bold mb-0 text-white">
              {{ selectedMatch.name }}
            </h6>
            <small class="text-white-50">
              {{ selectedMatch.isOnline ? '🟢 Online' : '⚫ Offline' }}
            </small>
          </div>
        </div>
        <button class="btn-close-drawer" @click="closeChat">✕</button>
      </div>

      <!-- Messages -->
      <div class="drawer-messages" ref="messagesContainer">
        <div
          v-for="msg in currentMessages"
          :key="msg.id"
          :class="['msg-bubble',
            msg.senderId === currentUserId ? 'mine' : 'theirs']"
        >
          <p class="mb-0">{{ msg.content }}</p>
          <small class="msg-time">{{ msg.timestamp }}</small>
        </div>

        <div v-if="currentMessages.length === 0" class="text-center py-4">
          <p class="text-muted small">
            No messages yet — say hello! 👋
          </p>
        </div>
      </div>

      <!-- Message Input -->
      <div class="drawer-input">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type a message..."
          class="msg-input"
          @keyup.enter="sendMessage"
        />
        <button
          class="btn-send"
          @click="sendMessage"
          :disabled="!newMessage.trim()"
        >
          ➤
        </button>
      </div>

    </div>

    <!-- Overlay -->
    <div
      class="drawer-overlay"
      v-if="chatOpen"
      @click="closeChat"
    ></div>

  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const currentUserId = ref(1) // replace with authStore.user.id

const loading = ref(false)
const searchQuery = ref('')
const chatOpen = ref(false)
const selectedMatch = ref(null)
const newMessage = ref('')
const messagesContainer = ref(null)

// Placeholder matches - replace with API call
const matches = ref([
  {
    id: 1,
    name: 'Alice Wonder',
    age: 23,
    location: 'Kingston, Jamaica',
    bio: 'Love hiking and adventure! Let\'s explore the world together.',
    matchScore: 92,
    sharedInterests: ['✈️ Travel', '🏋️ Fitness', '📸 Photography'],
    isOnline: true,
    matchedOn: '2 days ago',
    photo: null
  },
  {
    id: 2,
    name: 'Emma Artist',
    age: 24,
    location: 'Kingston, Jamaica',
    bio: 'Artist and creative soul. Let\'s create art together!',
    matchScore: 88,
    sharedInterests: ['🎨 Art', '🎬 Movies'],
    isOnline: false,
    matchedOn: '5 days ago',
    photo: null
  },
  {
    id: 3,
    name: 'Grace Gamer',
    age: 21,
    location: 'Portmore, Jamaica',
    bio: 'Gamer and coffee enthusiast. Let\'s play!',
    matchScore: 75,
    sharedInterests: ['🎮 Gaming', '🎵 Music', '💻 Tech'],
    isOnline: true,
    matchedOn: '1 week ago',
    photo: null
  },
])

// Messages per match
const messageHistory = ref({
  1: [
    { id: 1, senderId: 2, content: 'Hey! Looks like we matched 😊', timestamp: '10:30 AM' },
    { id: 2, senderId: 1, content: 'Hi Alice! Yeah I loved your profile!', timestamp: '10:32 AM' },
    { id: 3, senderId: 2, content: 'We should go hiking sometime!', timestamp: '10:33 AM' },
  ],
  2: [],
  3: [
    { id: 1, senderId: 3, content: 'Heyyy what games do you play?', timestamp: 'Yesterday' },
  ]
})

const filteredMatches = computed(() => {
  if (!searchQuery.value) return matches.value
  return matches.value.filter(m =>
    m.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    m.bio.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const currentMessages = computed(() => {
  if (!selectedMatch.value) return []
  return messageHistory.value[selectedMatch.value.id] || []
})

function openChat(match) {
  selectedMatch.value = match
  chatOpen.value = true
  nextTick(() => scrollToBottom())
}

function closeChat() {
  chatOpen.value = false
  selectedMatch.value = null
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop =
      messagesContainer.value.scrollHeight
  }
}

function sendMessage() {
  if (!newMessage.value.trim() || !selectedMatch.value) return

  const msg = {
    id: Date.now(),
    senderId: currentUserId.value,
    content: newMessage.value.trim(),
    timestamp: new Date().toLocaleTimeString([], {
      hour: '2-digit', minute: '2-digit'
    })
  }

  if (!messageHistory.value[selectedMatch.value.id]) {
    messageHistory.value[selectedMatch.value.id] = []
  }

  messageHistory.value[selectedMatch.value.id].push(msg)
  newMessage.value = ''

  nextTick(() => scrollToBottom())

  // TODO: POST /api/messages when backend ready
}
</script>

<style scoped>
.matches-wrapper {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  position: relative;
}

/* Header */
.matches-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.match-count-badge {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

/* Search */
.search-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  padding: 10px 16px;
  background: white;
}

.search-wrap:focus-within {
  border-color: #6f42c1;
}

.search-input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 14px;
}

/* Matches Grid */
.matches-grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.match-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  border: 1.5px solid #f0e8ff;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.match-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(111,66,193,0.12);
}

.match-card.active {
  border-color: #6f42c1;
  background: #fdf8ff;
}

/* Avatar */
.avatar-wrap {
  position: relative;
  flex-shrink: 0;
}

.match-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f0e8ff;
}

.online-dot {
  position: absolute;
  bottom: 3px;
  right: 3px;
  width: 13px;
  height: 13px;
  background: #2ecc71;
  border-radius: 50%;
  border: 2px solid white;
}

/* Match Info */
.match-info {
  flex: 1;
}

.match-bio {
  font-size: 12px;
  color: #777;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.shared-interests {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.interest-chip {
  font-size: 11px;
  background: #f3eeff;
  color: #6f42c1;
  padding: 3px 9px;
  border-radius: 20px;
}

.interest-chip.more {
  background: #f5f5f5;
  color: #888;
}

/* Right Side */
.match-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  flex-shrink: 0;
}

.match-score {
  font-size: 12px;
  font-weight: 700;
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.btn-message {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 7px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  white-space: nowrap;
}

.btn-message:hover { opacity: 0.85; }

.match-date {
  font-size: 11px;
  color: #aaa;
  margin: 0;
}

/* Chat Drawer */
.chat-drawer {
  position: fixed;
  bottom: 0;
  right: -420px;
  width: 400px;
  height: 70vh;
  background: white;
  border-radius: 20px 20px 0 0;
  box-shadow: -4px 0 30px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  transition: right 0.3s ease;
  z-index: 1000;
}

.chat-drawer.open {
  right: 0;
}

.drawer-header {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  padding: 16px 20px;
  border-radius: 20px 20px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.drawer-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 2px solid white;
  object-fit: cover;
}

.btn-close-drawer {
  background: rgba(255,255,255,0.2);
  border: none;
  color: white;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  font-size: 14px;
}

.drawer-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.msg-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 13px;
  line-height: 1.4;
}

.msg-bubble.mine {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.msg-bubble.theirs {
  background: #f3eeff;
  color: #333;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.msg-time {
  font-size: 10px;
  opacity: 0.7;
  display: block;
  margin-top: 4px;
}

.drawer-input {
  padding: 14px 16px;
  border-top: 1px solid #f0e0ff;
  display: flex;
  gap: 10px;
  align-items: center;
}

.msg-input {
  flex: 1;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 13px;
  outline: none;
}

.msg-input:focus { border-color: #6f42c1; }

.btn-send {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border: none;
  border-radius: 12px;
  width: 42px;
  height: 42px;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-send:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-send:hover:not(:disabled) { opacity: 0.85; }

/* Overlay */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  z-index: 999;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.btn-go-browse {
  display: inline-block;
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  padding: 10px 24px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: opacity 0.2s;
}

.btn-go-browse:hover { opacity: 0.85; color: white; }

/* Spinner */
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