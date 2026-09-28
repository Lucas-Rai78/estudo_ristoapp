<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

import BaseButton from '../shared/components/BaseButton.vue'
import { useAuth } from '../features/auth/composable'

const router = useRouter()

const {
  user,
  isAuthenticated,
  logout,
} = useAuth()

async function leave() {
  logout()
  await router.replace({ name: 'login' })
}

let expiryCheck: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  expiryCheck = setInterval(() => {
    if (!isAuthenticated.value) {
      void router.replace({ name: 'login' })
    }
  }, 15_000)
})

onUnmounted(() => {
  if (expiryCheck) clearInterval(expiryCheck)
})
</script>

<template>
  <main class="flex min-h-dvh items-center justify-center bg-bg-app px-4">
    <section
      class="w-full max-w-lg rounded-2xl border border-border-main bg-bg-surface p-8 text-center shadow-sm"
    >
      <div
        class="mx-auto mb-5 flex size-12 items-center justify-center rounded-xl bg-brand-primary text-xl font-bold text-white"
      >
        R
      </div>

      <p class="text-sm font-semibold text-brand-primary">
        RistoApp
      </p>

      <h1 class="mt-3 text-3xl font-bold text-text-primary">
        Bem-vindo, {{ user?.name }}!
      </h1>

      <p class="mt-3 text-sm text-text-secondary">
        Você entrou com a conta {{ user?.email }}.
      </p>

      <div class="mx-auto mt-8 max-w-40">
        <BaseButton variant="outline" full-width @click="leave">
          Sair
        </BaseButton>
      </div>
    </section>
  </main>
</template>