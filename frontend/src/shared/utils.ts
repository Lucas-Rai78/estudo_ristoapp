import { z } from 'zod'
import { ApiError } from './api'

export function fieldErrors<T extends string>(
  error: z.ZodError,
): Partial<Record<T, string>> {
  const errors: Partial<Record<T, string>> = {}

  for (const issue of error.issues) {
    const field = issue.path[0] as T

    if (!errors[field]) {
      errors[field] = issue.message
    }
  }

  return errors
}

export function authErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    if (
      error.detail === 'INVALID_CREDENTIALS' ||
      error.status === 401
    ) {
      return 'E-mail ou senha incorretos.'
    }

    if (error.detail === 'EMAIL_ALREADY_EXISTS') {
      return 'Este e-mail já está cadastrado.'
    }

    if (error.detail === 'NETWORK_ERROR') {
      return 'Não foi possível conectar à API. Confira se o backend está ativo.'
    }

    if (error.status === 422) {
      return 'Confira os dados informados e tente novamente.'
    }
  }

  return 'Ocorreu um erro. Tente novamente em instantes.'
}