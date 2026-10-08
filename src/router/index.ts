import { createRouter, createWebHistory } from 'vue-router'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'login', component: () => import('../features/auth/views/LoginView.vue') },
    { path: '/register', name: 'register', component: () => import('../features/auth/views/RegisterView.vue') },
  ],
})