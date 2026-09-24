<script setup lang="ts">
import { ref } from 'vue'

import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

type AuthView =
  | 'login'
  | 'register'

const currentView = ref<AuthView>('login')

function showLogin(): void {
  currentView.value = 'login'
}

function showRegister(): void {
  currentView.value = 'register'
}
</script>

<template>
  <LoginView
    v-if="currentView === 'login'"
    @register="showRegister"
  />

  <RegisterView
    v-else
    @login="showLogin"
  />
</template>