<template>
  <div class="card mb-3 shadow-sm">
    <div class="row g-0">
      <div class="col-md-3">
        <img :src="profile.photo || '/default-avatar.png'" class="img-fluid rounded-start" />
      </div>
      <div class="col-md-9">
        <div class="card-body">
          <h5 class="card-title">{{ profile.name }}, {{ profile.age }}</h5>
          <p class="card-text text-muted">{{ profile.location }}</p>
          <p class="card-text">{{ profile.bio }}</p>
          <span class="badge bg-success me-2">Match Score: {{ profile.matchScore }}%</span>
          <button class="btn btn-primary btn-sm me-2" @click="$emit('like', profile.id)">
            👍 Like
          </button>
          <button class="btn btn-secondary btn-sm" @click="$emit('pass', profile.id)">
            Pass
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  profile: Object
})
defineEmits(['like', 'pass'])
</script>