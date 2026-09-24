import { z } from 'zod'

export const loginSchema = z.object({
  email: z
    .string()
    .trim()
    .min(1, 'O e-mail é obrigatório')
    .email('Digite um e-mail válido')
    .max(254, 'O e-mail informado é muito longo'),

  password: z
    .string()
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

export const registerSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(1, 'O nome é obrigatório')
      .min(3, 'Digite pelo menos 3 caracteres')
      .max(100, 'O nome deve possuir no máximo 100 caracteres'),

    email: z
      .string()
      .trim()
      .min(1, 'O e-mail é obrigatório')
      .email('Digite um e-mail válido')
      .max(254, 'O e-mail informado é muito longo'),

    password: z
      .string()
      .min(1, 'A senha é obrigatória')
      .min(8, 'A senha deve possuir pelo menos 8 caracteres')
      .max(72, 'A senha deve possuir no máximo 72 caracteres'),

    confirmPassword: z
      .string()
      .min(1, 'Confirme sua senha'),
  })
  .refine(
    (data) => data.password === data.confirmPassword,
    {
      message: 'As senhas não coincidem',
      path: ['confirmPassword'],
    },
  )

export type RegisterForm = z.input<typeof registerSchema>

export type RegisterPayload = z.output<typeof registerSchema>

export type RegisterField = keyof RegisterForm

export type RegisterFieldErrors = Partial<
  Record<RegisterField, string>
>

export interface AuthUser {
  id: string
  name: string
  email: string
}

export interface LoginResponse {
  accessToken: string
  user: AuthUser
}

export interface RegisterResponse {
  user: AuthUser
}

export type AuthErrorCode =
  | 'INVALID_CREDENTIALS'
  | 'EMAIL_ALREADY_EXISTS'
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

export type RegisterResult = Result<RegisterResponse>