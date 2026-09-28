<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import BaseInput from '../shared/components/BaseInput.vue'
import BaseButton from '../shared/components/BaseButton.vue'
import AuthLayout from '../features/auth/Component.vue'

import {
  loginSchema,
  type LoginForm,
} from '../features/auth/schemas'

import { login } from '../features/auth/service'
import { useAuth } from '../features/auth/composable'
import {
  authErrorMessage,
  fieldErrors,
} from '../shared/utils'

const router = useRouter()
const route = useRoute()
const { saveSession } = useAuth()

const form = reactive<LoginForm>({
  email: '',
  password: '',
})

const errors = ref<
  Partial<Record<keyof LoginForm, string>>
>({})

const feedback = ref('')
const loading = ref(false)

async function submit() {
  if (loading.value) return

  feedback.value = ''

  const result = loginSchema.safeParse(form)

  if (!result.success) {
    errors.value = fieldErrors(result.error)
    return
  }

  errors.value = {}
  loading.value = true

  try {
    const response = await login(result.data)
    saveSession(response)

    const redirect = route.query.redirect

    await router.replace(
      typeof redirect === 'string' &&
      redirect.startsWith('/') &&
      !redirect.startsWith('//')
        ? redirect
        : { name: 'welcome' },
    )
  } catch (error) {
    feedback.value = authErrorMessage(error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <AuthLayout
    title="Bem-vindo de volta"
    subtitle="Entre na sua conta para continuar."
  >
    <form
      class="space-y-5"
      novalidate
      @submit.prevent="submit"
    >
      <p
        v-if="route.query.registered === '1'"
        role="status"
        class="rounded-lg bg-green-50 p-3 text-sm text-green-800"
      >
        Conta criada. Faça login para continuar.
      </p>

      <p
        v-if="feedback"
        role="alert"
        class="rounded-lg bg-red-50 p-3 text-sm text-status-danger"
      >
        {{ feedback }}
      </p>

      <BaseInput
        id="login-email"
        v-model="form.email"
        label="E-mail"
        type="email"
        autocomplete="email"
        :error="errors.email"
        :disabled="loading"
        @update:model-value="errors.email = undefined"
      />

      <BaseInput
        id="login-password"
        v-model="form.password"
        label="Senha"
        type="password"
        autocomplete="current-password"
        :error="errors.password"
        :disabled="loading"
        @update:model-value="errors.password = undefined"
      />

      <BaseButton
        type="submit"
        :loading="loading"
        full-width
      >
        Entrar
      </BaseButton>
    </form>

    <p class="mt-6 text-center text-sm text-text-secondary">
      Ainda não tem conta?

      <RouterLink
        to="/cadastro"
        class="font-semibold text-brand-primary hover:underline"
      >
        Criar conta
      </RouterLink>
    </p>
  </AuthLayout>
</template>