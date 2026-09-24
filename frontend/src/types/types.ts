import { z } from 'zod'

export const loginSchema = z.object({
  email: z
    .string({
      message: 'O e-mail é obrigatório',
    })
    .trim()
    .min(1, 'O e-mail é obrigatório')
    .email('Digite um e-mail válido')
    .max(254, 'O e-mail informado é muito longo'),

  password: z
    .string({
      message: 'A senha é obrigatória',
    })
    .min(1, 'A senha é obrigatória')
    .min(8, 'A senha deve possuir pelo menos 8 caracteres')
    .max(72, 'A senha deve possuir no máximo 72 caracteres'),
})

export type LoginForm = z.input<typeof loginSchema>

export type LoginPayload = z.output<typeof loginSchema>

export type LoginField = keyof LoginForm

export type LoginFieldErrors = Partial<
  Record<LoginField, string>
>

export type LoginStatus =
  | {
      status: 'idle'
    }
  | {
      status: 'validating'
    }
  | {
      status: 'invalid'
    }
  | {
      status: 'ready'
      payload: LoginPayload
    }
  | {
      status: 'submitting'
    }
  | {
      status: 'error'
      message: string
    }

export interface AuthUser {
  id: string
  name: string
  email: string
}

export interface LoginResponse {
  accessToken: string
  user: AuthUser
}

export type AuthErrorCode =
  | 'INVALID_CREDENTIALS'
  | 'USER_DISABLED'
  | 'RATE_LIMITED'
  | 'NETWORK_ERROR'
  | 'UNKNOWN_ERROR'

export interface AuthError {
  code: AuthErrorCode
  message: string
}

export type Result<TData, TError = AuthError> =
  | {
      success: true
      data: TData
    }
  | {
      success: false
      error: TError
    }

export type LoginResult = Result<LoginResponse>