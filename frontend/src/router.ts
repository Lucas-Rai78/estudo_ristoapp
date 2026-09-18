import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

// Importa todos os route.ts das features dinamicamente
const routeModules = import.meta.glob('../features/**/route.ts', { eager: true })

const routes: RouteRecordRaw[] = Object.values(routeModules).flatMap(
  (mod: any) => (Array.isArray(mod.default) ? mod.default : [mod.default]).filter(Boolean),
)

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})
