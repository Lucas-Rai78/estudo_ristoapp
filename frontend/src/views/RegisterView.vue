<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import BaseInput from '../shared/components/BaseInput.vue'
import BaseButton from '../shared/components/BaseButton.vue'
import AuthLayout from '../features/auth/Component.vue'

import {
  registerSchema,
  type RegisterForm,
} from '../features/auth/schemas'

import { register } from '../features/auth/service'

import {
  authErrorMessage,
  fieldErrors,
} from '../shared/utils'

const router = useRouter()

const form = reactive<RegisterForm>({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const errors = ref<
  Partial<Record<keyof RegisterForm, string>>
>({})

const feedback = ref('')
const loading = ref(false)

async function submit() {
  if (loading.value) return

  feedback.value = ''

  const result = registerSchema.safeParse(form)

  if (!result.success) {
    errors.value = fieldErrors(result.error)
    return
  }

  errors.value = {}
  loading.value = true

  try {
    await register(result.data)

    await router.replace({
      name: 'login',
      query: { registered: '1' },
    })
  } catch (error) {
    feedback.value = authErrorMessage(error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <AuthLayout
    title="Criar conta"
    subtitle="Preencha os dados para começar."
  >
    <form
      class="space-y-4"
      novalidate
      @submit.prevent="submit"
    >
      <p
        v-if="feedback"
        role="alert"
        class="rounded-lg bg-red-50 p-3 text-sm text-status-danger"
      >
        {{ feedback }}
      </p>

      <BaseInput
        id="register-name"
        v-model="form.name"
        label="Nome"
        :error="errors.name"
        :disabled="loading"
        @update:model-value="errors.name = undefined"
      />

      <BaseInput
        id="register-email"
        v-model="form.email"
        label="E-mail"
        type="email"
        autocomplete="email"
        :error="errors.email"
        :disabled="loading"
        @update:model-value="errors.email = undefined"
      />

      <BaseInput
        id="register-password"
        v-model="form.password"
        label="Senha"
        type="password"
        autocomplete="new-password"
        :error="errors.password"
        :disabled="loading"
        @update:model-value="errors.password = undefined"
      />

      <BaseInput
        id="register-confirm-password"
        v-model="form.confirmPassword"
        label="Confirmar senha"
        type="password"
        autocomplete="new-password"
        :error="errors.confirmPassword"
        :disabled="loading"
        @update:model-value="errors.confirmPassword = undefined"
      />

      <BaseButton
        type="submit"
        :loading="loading"
        full-width
      >
        Criar conta
      </BaseButton>
    </form>

    <p class="mt-6 text-center text-sm text-text-secondary">
      Já tem conta?

      <RouterLink
        to="/login"
        class="font-semibold text-brand-primary hover:underline"
      >
        Entrar
      </RouterLink>
    </p>
  </AuthLayout>
</template>