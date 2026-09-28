import { computed, shallowRef } from 'vue'
import { z } from 'zod'
import type { AuthUser, LoginResponse } from './service'

const STORAGE_KEY = 'ristoapp.auth'

const sessionSchema = z.object({
  access_token: z.string(),
  token_type: z.literal('bearer'),
  user: z.object({
    id: z.string(),
    name: z.string(),
    email: z.string(),
  }),
})

function tokenIsCurrent(token: string): boolean {
  try {
    const encodedPayload = token.split('.')[1]

    if (!encodedPayload) return false

    const payload: unknown = JSON.parse(
      atob(
        encodedPayload
          .replace(/-/g, '+')
          .replace(/_/g, '/'),
      ),
    )

    return (
      !!payload &&
      typeof payload === 'object' &&
      'exp' in payload &&
      typeof payload.exp === 'number' &&
      payload.exp > Date.now() / 1000
    )
  } catch {
    return false
  }
}

function readSession(): LoginResponse | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return null

    const result = sessionSchema.safeParse(JSON.parse(raw))

    if (
      result.success &&
      tokenIsCurrent(result.data.access_token)
    ) {
      return result.data
    }

    sessionStorage.removeItem(STORAGE_KEY)
  } catch {
    // Sessão inválida ou armazenamento indisponível.
  }

  return null
}

const session = shallowRef<LoginResponse | null>(readSession())

export function useAuth() {
  function logout() {
    session.value = null

    try {
      sessionStorage.removeItem(STORAGE_KEY)
    } catch {
      // O estado em memória já foi removido.
    }
  }

  function currentSession(): LoginResponse | null {
    if (
      session.value &&
      !tokenIsCurrent(session.value.access_token)
    ) {
      logout()
    }

    return session.value
  }

  const user = computed<AuthUser | null>(
    () => currentSession()?.user ?? null,
  )

  const isAuthenticated = computed(
    () => !!currentSession(),
  )

  function saveSession(value: LoginResponse) {
    if (!tokenIsCurrent(value.access_token)) {
      throw new Error('Token recebido inválido ou expirado')
    }

    sessionStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(value),
    )

    session.value = value
  }

  return {
    user,
    isAuthenticated,
    saveSession,
    logout,
  }
}