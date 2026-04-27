<template>
  <div :class="['d-flex mb-2', isMine ? 'justify-content-end' : 'justify-content-start']">
    <div :class="['p-2 rounded', isMine ? 'bg-primary text-white' : 'bg-light text-dark']"
         style="max-width: 60%">
      <p class="mb-0">{{ message.content }}</p>
      <small class="opacity-75">{{ message.timestamp }}</small>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: Object,
  isMine: Boolean
})
</script>