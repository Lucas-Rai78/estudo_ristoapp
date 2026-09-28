import { z } from 'zod'
import { postJson } from '../../shared/api'
import {
  loginSchema,
  registerSchema,
  type LoginForm,
  type RegisterForm,
} from './schemas'

const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
})

const loginResponseSchema = z.object({
  access_token: z.string().min(1),
  token_type: z.literal('bearer'),
  user: userSchema,
})

const registerResponseSchema = z.object({
  message: z.string(),
  user: userSchema,
})

export type AuthUser = z.infer<typeof userSchema>
export type LoginResponse = z.infer<typeof loginResponseSchema>

export async function login(
  form: LoginForm,
): Promise<LoginResponse> {
  const body = loginSchema.parse(form)

  const response = await postJson<unknown>('/auth/login', body)
  return loginResponseSchema.parse(response)
}

export async function register(
  form: RegisterForm,
): Promise<AuthUser> {
  const validated = registerSchema.parse(form)

  // confirmPassword pertence apenas ao formulário.
  const body = {
    name: validated.name,
    email: validated.email,
    password: validated.password,
  }

  const response = await postJson<unknown>('/auth/register', body)
  return registerResponseSchema.parse(response).user
}