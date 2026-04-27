import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import MatchesView from '../views/MatchesView.vue'
import MessagesView from '../views/MessagesView.vue'
import ProfileView from '../views/ProfileView.vue'




const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',           component: HomeView },
    { path: '/login',      component: LoginView },
    { path: '/register',   component: RegisterView },
    { path: '/dashboard',  component: DashboardView, meta: { requiresAuth: true } },
    { path: '/matches',    component: MatchesView,   meta: { requiresAuth: true } },
    { path: '/messages',   component: MessagesView,  meta: { requiresAuth: true } },
    { path: '/profile',    component: ProfileView,   meta: { requiresAuth: true } },
    { path: '/:pathMatch(.*)*', component: () => import('../views/NotFoundView.vue') }
  ]
})


// Protect pages that require login
// router.beforeEach((to, from, next) => {
//   const token = localStorage.getItem('token')
//   if (to.meta.requiresAuth && !token) {
//     next('/login')
//   } else {
//     next()
//   }
// })

export default router