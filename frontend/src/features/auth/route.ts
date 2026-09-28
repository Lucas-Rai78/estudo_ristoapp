import type { RouteRecordRaw } from 'vue-router'

export const authRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../../views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/cadastro',
    name: 'register',
    component: () => import('../../views/RegisterView.vue'),
    meta: { guest: true },
  },
  {
    path: '/bem-vindo',
    name: 'welcome',
    component: () => import('../../views/WelcomeView.vue'),
    meta: { requiresAuth: true },
  },
]