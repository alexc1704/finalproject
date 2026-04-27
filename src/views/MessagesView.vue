<template>
  <div class="messages-wrapper">

    <!-- Sidebar - Conversation List -->
    <div :class="['conversations-sidebar', mobileShowChat ? 'hide-mobile' : '']">

      <div class="sidebar-header">
        <h5 class="fw-bold mb-0">Messages 💬</h5>
        <span class="conversation-count">{{ conversations.length }}</span>
      </div>

      <!-- Search -->
      <div class="sidebar-search">
        <span>🔍</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search conversations..."
          class="sidebar-search-input"
        />
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-4">
        <div class="small-spinner"></div>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredConversations.length === 0"
        class="empty-conversations">
        <p class="display-6">💌</p>
        <p class="text-muted small">No conversations yet.</p>
        <router-link to="/matches" class="btn-find-matches">
          Find Matches →
        </router-link>
      </div>

      <!-- Conversation List -->
      <div v-else class="conversation-list">
        <div
          v-for="convo in filteredConversations"
          :key="convo.id"
          :class="['convo-item',
            selectedConvo?.id === convo.id ? 'active' : '',
            convo.unread ? 'unread' : '']"
          @click="selectConversation(convo)"
        >
          <!-- Avatar -->
          <div class="convo-avatar-wrap">
            <img
              :src="convo.photo || 'https://ui-avatars.com/api/?name=' +
                convo.name + '&background=random&size=128'"
              class="convo-avatar"
            />
            <span class="online-dot" v-if="convo.isOnline"></span>
          </div>

          <!-- Preview -->
          <div class="convo-preview">
            <div class="convo-top">
              <span class="convo-name">{{ convo.name }}</span>
              <span class="convo-time">{{ convo.lastMessageTime }}</span>
            </div>
            <p class="convo-last-msg">
              <span v-if="convo.lastSenderIsMe">You: </span>
              {{ convo.lastMessage }}
            </p>
          </div>

          <!-- Unread badge -->
          <span v-if="convo.unread" class="unread-badge">
            {{ convo.unreadCount }}
          </span>

        </div>
      </div>

    </div>

    <!-- Chat Area -->
    <div :class="['chat-area', mobileShowChat ? 'show-mobile' : '']">

      <!-- No Conversation Selected -->
      <div v-if="!selectedConvo" class="no-chat-selected">
        <p class="display-4">💬</p>
        <h5 class="fw-bold mt-2">Select a conversation</h5>
        <p class="text-muted small">
          Choose someone from the left to start chatting
        </p>
      </div>

      <!-- Active Chat -->
      <template v-else>

        <!-- Chat Header -->
        <div class="chat-header">
          <button class="btn-back-mobile" @click="mobileShowChat = false">
            ←
          </button>
          <img
            :src="selectedConvo.photo ||
              'https://ui-avatars.com/api/?name=' +
              selectedConvo.name + '&background=random&size=128'"
            class="chat-header-avatar"
          />
          <div class="chat-header-info">
            <h6 class="fw-bold mb-0">{{ selectedConvo.name }}</h6>
            <small :class="selectedConvo.isOnline ?
              'text-success' : 'text-muted'">
              {{ selectedConvo.isOnline ? '🟢 Online' : '⚫ Offline' }}
            </small>
          </div>
          <div class="chat-header-actions">
            <router-link
              :to="'/profile/' + selectedConvo.id"
              class="btn-view-profile"
            >
              👤 View Profile
            </router-link>
          </div>
        </div>

        <!-- Messages Area -->
        <div class="messages-area" ref="messagesContainer">

          <!-- Date Divider -->
          <div class="date-divider">
            <span>Today</span>
          </div>

          <!-- Message Bubbles -->
          <div
            v-for="msg in currentMessages"
            :key="msg.id"
            :class="['msg-row',
              msg.senderId === currentUserId ? 'mine' : 'theirs']"
          >
            <!-- Their avatar -->
            <img
              v-if="msg.senderId !== currentUserId"
              :src="selectedConvo.photo ||
                'https://ui-avatars.com/api/?name=' +
                selectedConvo.name + '&background=random&size=128'"
              class="msg-avatar"
            />

            <div class="msg-content">
              <div :class="['msg-bubble',
                msg.senderId === currentUserId ? 'mine' : 'theirs']">
                {{ msg.content }}
              </div>
              <small class="msg-time">{{ msg.timestamp }}</small>
            </div>

          </div>

          <!-- Typing Indicator -->
          <div class="msg-row theirs" v-if="isTyping">
            <img
              :src="'https://ui-avatars.com/api/?name=' +
                selectedConvo.name + '&background=random&size=128'"
              class="msg-avatar"
            />
            <div class="msg-content">
              <div class="msg-bubble theirs typing-bubble">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </div>
            </div>
          </div>

          <!-- Empty Chat -->
          <div v-if="currentMessages.length === 0 && !isTyping"
            class="empty-chat">
            <p class="display-6">👋</p>
            <p class="text-muted small">
              You matched with {{ selectedConvo.name }}!
              Say hello and break the ice.
            </p>
          </div>

        </div>

        <!-- Message Input -->
        <div class="message-input-area">
          <div class="input-wrap">

            <button class="btn-emoji" @click="toggleEmojiPanel">
              😊
            </button>

            <!-- Quick Emoji Panel -->
            <div v-if="showEmojiPanel" class="emoji-panel">
              <span
                v-for="emoji in quickEmojis"
                :key="emoji"
                class="emoji-option"
                @click="addEmoji(emoji)"
              >
                {{ emoji }}
              </span>
            </div>

            <input
              v-model="newMessage"
              type="text"
              :placeholder="'Message ' + selectedConvo.name + '...'"
              class="message-input"
              @keyup.enter="sendMessage"
              @input="handleTyping"
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

      </template>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const currentUserId = ref(1) // replace with authStore.user.id

const loading = ref(false)
const searchQuery = ref('')
const selectedConvo = ref(null)
const newMessage = ref('')
const messagesContainer = ref(null)
const mobileShowChat = ref(false)
const isTyping = ref(false)
const showEmojiPanel = ref(false)
let typingTimeout = null

const quickEmojis = [
  '😊','😂','❤️','🔥','👏','😍',
  '🥺','😎','🙏','💯','✨','🎉'
]

// Placeholder conversations
const conversations = ref([
  {
    id: 1,
    name: 'Alice Wonder',
    photo: null,
    isOnline: true,
    lastMessage: 'We should go hiking sometime!',
    lastMessageTime: '10:33 AM',
    lastSenderIsMe: false,
    unread: true,
    unreadCount: 2
  },
  {
    id: 2,
    name: 'Emma Artist',
    photo: null,
    isOnline: false,
    lastMessage: 'That sounds amazing 🎨',
    lastMessageTime: 'Yesterday',
    lastSenderIsMe: true,
    unread: false,
    unreadCount: 0
  },
  {
    id: 3,
    name: 'Grace Gamer',
    photo: null,
    isOnline: true,
    lastMessage: 'Heyyy what games do you play?',
    lastMessageTime: 'Monday',
    lastSenderIsMe: false,
    unread: true,
    unreadCount: 1
  }
])

// Message history per conversation
const messageHistory = ref({
  1: [
    {
      id: 1, senderId: 2,
      content: 'Hey! Looks like we matched 😊',
      timestamp: '10:30 AM'
    },
    {
      id: 2, senderId: 1,
      content: 'Hi Alice! Yeah I loved your profile!',
      timestamp: '10:32 AM'
    },
    {
      id: 3, senderId: 2,
      content: 'We should go hiking sometime!',
      timestamp: '10:33 AM'
    },
  ],
  2: [
    {
      id: 1, senderId: 1,
      content: 'Hey Emma! Love your artwork 🎨',
      timestamp: 'Yesterday'
    },
    {
      id: 2, senderId: 2,
      content: 'That sounds amazing 🎨',
      timestamp: 'Yesterday'
    },
  ],
  3: [
    {
      id: 1, senderId: 3,
      content: 'Heyyy what games do you play?',
      timestamp: 'Monday'
    },
  ]
})

const filteredConversations = computed(() => {
  if (!searchQuery.value) return conversations.value
  return conversations.value.filter(c =>
    c.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const currentMessages = computed(() => {
  if (!selectedConvo.value) return []
  return messageHistory.value[selectedConvo.value.id] || []
})

function selectConversation(convo) {
  selectedConvo.value = convo
  mobileShowChat.value = true
  // Mark as read
  convo.unread = false
  convo.unreadCount = 0
  nextTick(() => scrollToBottom())

  // TODO: fetch messages from API
  // const res = await fetch(`/api/messages/${convo.id}`, {
  //   headers: { Authorization: `Bearer ${authStore.token}` }
  // })
  // const data = await res.json()
  // messageHistory.value[convo.id] = data.messages
}

function sendMessage() {
  if (!newMessage.value.trim() || !selectedConvo.value) return

  const msg = {
    id: Date.now(),
    senderId: currentUserId.value,
    content: newMessage.value.trim(),
    timestamp: new Date().toLocaleTimeString([], {
      hour: '2-digit', minute: '2-digit'
    })
  }

  if (!messageHistory.value[selectedConvo.value.id]) {
    messageHistory.value[selectedConvo.value.id] = []
  }

  messageHistory.value[selectedConvo.value.id].push(msg)

  // Update conversation preview
  const convo = conversations.value.find(
    c => c.id === selectedConvo.value.id
  )
  if (convo) {
    convo.lastMessage = msg.content
    convo.lastMessageTime = msg.timestamp
    convo.lastSenderIsMe = true
  }

  newMessage.value = ''
  showEmojiPanel.value = false
  nextTick(() => scrollToBottom())

  // TODO: POST /api/messages when backend ready
}

function handleTyping() {
  // Simulate typing indicator coming back
  clearTimeout(typingTimeout)
  isTyping.value = true
  typingTimeout = setTimeout(() => {
    isTyping.value = false
  }, 2000)
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop =
      messagesContainer.value.scrollHeight
  }
}

function toggleEmojiPanel() {
  showEmojiPanel.value = !showEmojiPanel.value
}

function addEmoji(emoji) {
  newMessage.value += emoji
  showEmojiPanel.value = false
}
</script>

<style scoped>
.messages-wrapper {
  display: flex;
  height: calc(100vh - 80px);
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 30px rgba(0,0,0,0.08);
  border: 1.5px solid #f0e8ff;
}

/* Sidebar */
.conversations-sidebar {
  width: 320px;
  flex-shrink: 0;
  border-right: 1.5px solid #f0e8ff;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 20px 16px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f5f0ff;
}

.conversation-count {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border-radius: 20px;
  padding: 2px 10px;
  font-size: 12px;
  font-weight: 600;
}

.sidebar-search {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 10px 12px;
  background: #f9f5ff;
  border-radius: 12px;
  padding: 9px 14px;
  border: 1.5px solid transparent;
}

.sidebar-search:focus-within {
  border-color: #6f42c1;
}

.sidebar-search-input {
  border: none;
  outline: none;
  background: transparent;
  font-size: 13px;
  width: 100%;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
}

/* Conversation Item */
.convo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.15s;
  position: relative;
  border-bottom: 1px solid #faf5ff;
}

.convo-item:hover { background: #fdf8ff; }

.convo-item.active {
  background: #f3eeff;
  border-left: 3px solid #6f42c1;
}

.convo-item.unread .convo-name {
  font-weight: 700;
  color: #333;
}

.convo-item.unread .convo-last-msg {
  color: #444;
  font-weight: 500;
}

.convo-avatar-wrap {
  position: relative;
  flex-shrink: 0;
}

.convo-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #f0e8ff;
}

.online-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 11px;
  height: 11px;
  background: #2ecc71;
  border-radius: 50%;
  border: 2px solid white;
}

.convo-preview { flex: 1; overflow: hidden; }

.convo-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3px;
}

.convo-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.convo-time {
  font-size: 11px;
  color: #aaa;
}

.convo-last-msg {
  font-size: 12px;
  color: #999;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.unread-badge {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-weight: 700;
}

/* Chat Area */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.no-chat-selected {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #aaa;
  padding: 40px;
}

/* Chat Header */
.chat-header {
  padding: 14px 20px;
  border-bottom: 1.5px solid #f0e8ff;
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
}

.btn-back-mobile {
  display: none;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #6f42c1;
}

.chat-header-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #f0e8ff;
}

.chat-header-info { flex: 1; }

.btn-view-profile {
  font-size: 12px;
  background: #f3eeff;
  color: #6f42c1;
  border-radius: 10px;
  padding: 6px 12px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-view-profile:hover {
  background: #e8d5ff;
  color: #6f42c1;
}

/* Messages Area */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #fdfbff;
}

.date-divider {
  text-align: center;
  margin: 8px 0;
}

.date-divider span {
  background: #f0e8ff;
  color: #9b7fd4;
  font-size: 11px;
  padding: 4px 12px;
  border-radius: 20px;
}

.msg-row {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.msg-row.mine { flex-direction: row-reverse; }

.msg-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.msg-content {
  display: flex;
  flex-direction: column;
  max-width: 65%;
}

.msg-row.mine .msg-content { align-items: flex-end; }
.msg-row.theirs .msg-content { align-items: flex-start; }

.msg-bubble {
  padding: 10px 14px;
  border-radius: 18px;
  font-size: 13px;
  line-height: 1.5;
  word-break: break-word;
}

.msg-bubble.mine {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border-bottom-right-radius: 4px;
}

.msg-bubble.theirs {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.msg-time {
  font-size: 10px;
  color: #bbb;
  margin-top: 4px;
  padding: 0 4px;
}

/* Typing indicator */
.typing-bubble {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 16px;
}

.dot {
  width: 7px;
  height: 7px;
  background: #aaa;
  border-radius: 50%;
  animation: bounce 1.2s infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

/* Empty Chat */
.empty-chat {
  flex: 1;
  text-align: center;
  padding: 60px 20px;
  margin: auto;
}

/* Message Input */
.message-input-area {
  padding: 14px 16px;
  border-top: 1.5px solid #f0e8ff;
  background: white;
  position: relative;
}

.input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f9f5ff;
  border-radius: 14px;
  padding: 8px 12px;
  border: 1.5px solid transparent;
  position: relative;
}

.input-wrap:focus-within { border-color: #6f42c1; }

.btn-emoji {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.emoji-panel {
  position: absolute;
  bottom: 56px;
  left: 10px;
  background: white;
  border-radius: 14px;
  padding: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.12);
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  width: 220px;
  z-index: 10;
  border: 1.5px solid #f0e8ff;
}

.emoji-option {
  font-size: 20px;
  cursor: pointer;
  transition: transform 0.1s;
}

.emoji-option:hover { transform: scale(1.3); }

.message-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 13px;
}

.btn-send {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  border: none;
  border-radius: 10px;
  width: 36px;
  height: 36px;
  font-size: 15px;
  cursor: pointer;
  transition: opacity 0.2s;
  flex-shrink: 0;
}

.btn-send:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-send:hover:not(:disabled) { opacity: 0.85; }

/* Empty conversations */
.empty-conversations {
  text-align: center;
  padding: 40px 20px;
}

.btn-find-matches {
  display: inline-block;
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
  color: white;
  padding: 8px 20px;
  border-radius: 10px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  margin-top: 8px;
}

/* Spinner */
.small-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #f0e8ff;
  border-top-color: #6f42c1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Mobile */
@media (max-width: 640px) {
  .conversations-sidebar { width: 100%; }
  .hide-mobile { display: none; }
  .chat-area { display: none; }
  .chat-area.show-mobile { display: flex; width: 100%; }
  .btn-back-mobile { display: block; }
}
</style>