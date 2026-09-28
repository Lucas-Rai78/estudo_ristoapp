import { createRouter, createWebHistory } from 'vue-router'
import { authRoutes } from './features/auth/route'
import { useAuth } from './features/auth/composable'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/bem-vindo' },

    // Mantenha aqui as demais rotas do seu projeto.
    ...authRoutes,
  ],
})

router.beforeEach(to => {
  const { isAuthenticated } = useAuth()

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return {
      name: 'login',
      query: { redirect: to.fullPath },
    }
  }

  if (to.meta.guest && isAuthenticated.value) {
    return { name: 'welcome' }
  }
})

export default router