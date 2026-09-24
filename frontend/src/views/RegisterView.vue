<script setup lang="ts">
import { reactive, ref } from 'vue'

import BaseInput from '@/shared/components/BaseInput.vue'
import BaseButton from '@/shared/components/BaseButton.vue'

import {
  registerSchema,
  type RegisterField,
  type RegisterFieldErrors,
  type RegisterForm,
} from '@/types/types'

const emit = defineEmits<{
  (event: 'login'): void
}>()

const form = reactive<RegisterForm>({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const errors = ref<RegisterFieldErrors>({})

const success = ref(false)

function clearFieldError(field: RegisterField): void {
  if (!errors.value[field]) {
    return
  }

  const nextErrors = {
    ...errors.value,
  }

  delete nextErrors[field]

  errors.value = nextErrors
}

function handleSubmit(): void {
  errors.value = {}
  success.value = false

  const result = registerSchema.safeParse(form)

  if (!result.success) {
    const fieldErrors = result.error.flatten().fieldErrors

    errors.value = {
      name: fieldErrors.name?.[0],
      email: fieldErrors.email?.[0],
      password: fieldErrors.password?.[0],
      confirmPassword: fieldErrors.confirmPassword?.[0],
    }

    return
  }

  success.value = true

  /**
   * Futuramente:
   *
   * await authService.register(result.data)
   */

  console.log('Cadastro válido:', result.data)
}
</script>

<template>
  <main
    class="min-h-screen bg-bg-app flex items-center justify-center p-4 sm:p-6"
  >
    <section class="w-full max-w-md">
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
          Criar conta
        </h1>

        <p class="mt-2 text-sm text-text-secondary">
          Preencha seus dados para criar sua conta.
        </p>
      </header>

      <div
        class="rounded-xl border border-border-main bg-bg-surface p-6 shadow-card-md sm:p-8"
      >
        <form
          class="flex flex-col gap-5"
          novalidate
          @submit.prevent="handleSubmit"
        >
          <BaseInput
            v-model="form.name"
            id="register-name"
            label="Nome"
            type="text"
            placeholder="Digite seu nome"
            required
            :error="errors.name"
            @focus="clearFieldError('name')"
          />

          <BaseInput
            v-model="form.email"
            id="register-email"
            label="E-mail"
            type="email"
            placeholder="nome@empresa.com"
            required
            :error="errors.email"
            @focus="clearFieldError('email')"
          />

          <BaseInput
            v-model="form.password"
            id="register-password"
            label="Senha"
            type="password"
            placeholder="Crie uma senha"
            required
            :error="errors.password"
            hint="Utilize pelo menos 8 caracteres."
            @focus="clearFieldError('password')"
          />

          <BaseInput
            v-model="form.confirmPassword"
            id="register-confirm-password"
            label="Confirmar senha"
            type="password"
            placeholder="Digite novamente sua senha"
            required
            :error="errors.confirmPassword"
            @focus="clearFieldError('confirmPassword')"
          />

          <div
            v-if="success"
            class="rounded-lg bg-status-success-bg px-3 py-2.5"
          >
            <p
              class="text-xs font-medium text-status-success"
            >
              Dados validados com sucesso.
            </p>
          </div>

          <BaseButton
            type="submit"
            variant="primary"
            size="lg"
            full-width
          >
            Criar conta
          </BaseButton>

          <div
            class="border-t border-border-main pt-5 text-center"
          >
            <p class="text-sm text-text-secondary">
              Já possui uma conta?

              <button
                type="button"
                class="font-semibold text-brand-primary hover:text-brand-hover"
                @click="emit('login')"
              >
                Entrar
              </button>
            </p>
          </div>
        </form>
      </div>
    </section>
  </main>
</template>