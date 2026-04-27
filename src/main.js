import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import LoadingSpinner from './components/LoadingSpinner.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Register globally - now usable in ANY view without importing
app.component('LoadingSpinner', LoadingSpinner)

app.mount('#app')