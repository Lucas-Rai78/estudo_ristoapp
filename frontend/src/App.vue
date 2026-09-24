<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

import BaseInput from '@/shared/components/BaseInput.vue'
import BaseButton from '@/shared/components/BaseButton.vue'

import {
  loginSchema,
  type LoginField,
  type LoginFieldErrors,
  type LoginForm,
  type LoginStatus,
} from '@/types/types'

const initialForm = {
  email: '',
  password: '',
} satisfies LoginForm

const form = reactive<LoginForm>({
  ...initialForm,
})

const errors = ref<LoginFieldErrors>({})

const loginState = ref<LoginStatus>({
  status: 'idle',
})

const isLoading = computed(
  () => loginState.value.status === 'submitting',
)

const hasErrors = computed(
  () => Object.keys(errors.value).length > 0,
)

function clearFieldError(field: LoginField): void {
  if (!errors.value[field]) {
    return
  }

  const nextErrors = {
    ...errors.value,
  }

  delete nextErrors[field]

  errors.value = nextErrors
}

function validateField(field: LoginField): void {
  if (field === 'email') {
    const result = loginSchema.shape.email.safeParse(form.email)

    if (!result.success) {
      errors.value = {
        ...errors.value,
        email: result.error.issues[0]?.message,
      }

      return
    }
  }

  if (field === 'password') {
    const result = loginSchema.shape.password.safeParse(
      form.password,
    )

    if (!result.success) {
      errors.value = {
        ...errors.value,
        password: result.error.issues[0]?.message,
      }

      return
    }
  }

  clearFieldError(field)
}

function mapZodErrors(
  result: ReturnType<typeof loginSchema.safeParse>,
): LoginFieldErrors {
  if (result.success) {
    return {}
  }

  const flattenedErrors = result.error.flatten().fieldErrors

  return {
    email: flattenedErrors.email?.[0],
    password: flattenedErrors.password?.[0],
  }
}

function handleSubmit(): void {
  loginState.value = {
    status: 'validating',
  }

  errors.value = {}

  const result = loginSchema.safeParse(form)

  if (!result.success) {
    errors.value = mapZodErrors(result)

    loginState.value = {
      status: 'invalid',
    }

    return
  }

  loginState.value = {
    status: 'ready',
    payload: result.data,
  }
}
</script>

<template>
  <main
    class="min-h-screen bg-bg-app flex items-center justify-center p-4 sm:p-6"
  >
    <section class="w-full max-w-md">
      <!-- Logo / Marca -->
      <header class="mb-8 text-center">
        <div
          class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-brand-primary shadow-brand-glow"
        >
          <svg
            class="h-6 w-6 text-white"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path
              d="M12 2L20 6V12C20 17 16.5 21 12 22C7.5 21 4 17 4 12V6L12 2Z"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M9 12L11 14L15 10"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </div>

        <h1 class="text-2xl font-bold text-text-primary">
          Bem-vindo
        </h1>

        <p class="mt-2 text-sm text-text-secondary">
          Entre com suas credenciais para acessar sua conta.
        </p>
      </header>

      <!-- Card -->
      <div
        class="rounded-xl border border-border-main bg-bg-surface p-6 shadow-card-md sm:p-8"
      >
        <form
          class="flex flex-col gap-5"
          novalidate
          @submit.prevent="handleSubmit"
        >
          <!-- E-mail -->
          <BaseInput
            v-model="form.email"
            id="email"
            label="E-mail"
            type="email"
            placeholder="nome@empresa.com"
            autocomplete="email"
            required
            :error="errors.email"
            @focus="clearFieldError('email')"
            @blur="validateField('email')"
          >
            <template #icon-left>
              <svg
                class="h-4 w-4"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  d="M4 4H20C21.1 4 22 4.9 22 6V18C22 19.1 21.1 20 20 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  d="M22 6L12 13L2 6"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </template>
          </BaseInput>

          <!-- Senha -->
          <BaseInput
            v-model="form.password"
            id="password"
            label="Senha"
            type="password"
            placeholder="Digite sua senha"
            autocomplete="current-password"
            required
            :error="errors.password"
            @focus="clearFieldError('password')"
            @blur="validateField('password')"
          >
            <template #icon-left>
              <svg
                class="h-4 w-4"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <rect
                  x="3"
                  y="11"
                  width="18"
                  height="10"
                  rx="2"
                  stroke="currentColor"
                  stroke-width="2"
                />

                <path
                  d="M7 11V7C7 4.23858 9.23858 2 12 2C14.7614 2 17 4.23858 17 7V11"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </template>
          </BaseInput>

          <!-- Erro geral -->
          <div
            v-if="
              loginState.status === 'invalid' &&
              hasErrors
            "
            class="rounded-lg bg-status-danger-bg px-3 py-2.5"
            role="alert"
          >
            <p class="text-xs font-medium text-status-danger">
              Verifique os campos destacados antes de continuar.
            </p>
          </div>

          <!-- Validação realizada -->
          <div
            v-if="loginState.status === 'ready'"
            class="rounded-lg bg-status-success-bg px-3 py-2.5"
            role="status"
          >
            <p class="text-xs font-medium text-status-success">
              Dados válidos. O formulário está pronto para ser
              conectado à API de autenticação.
            </p>
          </div>

          <!-- Submit -->
          <BaseButton
            type="submit"
            variant="primary"
            size="lg"
            full-width
            :loading="isLoading"
            :disabled="isLoading"
          >
            Entrar
          </BaseButton>
        </form>
      </div>

      <footer class="mt-6 text-center">
        <p class="text-xs text-text-muted">
          Acesso restrito a usuários autorizados.
        </p>
      </footer>
    </section>
  </main>
</template>