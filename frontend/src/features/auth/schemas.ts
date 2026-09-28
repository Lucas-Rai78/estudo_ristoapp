import { z } from 'zod'

const email = z
  .string()
  .trim()
  .min(1, 'Informe o e-mail')
  .email('Digite um e-mail válido')
  .max(254, 'O e-mail é muito longo')

const password = z
  .string()
  .min(1, 'Informe a senha')
  .min(8, 'Use pelo menos 8 caracteres')
  .max(72, 'Use no máximo 72 caracteres')

export const loginSchema = z.object({
  email,
  password,
})

export const registerSchema = z
  .object({
    name: z.string().trim()
      .min(3, 'Digite pelo menos 3 caracteres')
      .max(100, 'Use no máximo 100 caracteres'),
    email,
    password,
    confirmPassword: z.string().min(1, 'Confirme a senha'),
  })
  .refine(data => data.password === data.confirmPassword, {
    path: ['confirmPassword'],
    message: 'As senhas não coincidem',
  })

export type LoginForm = z.input<typeof loginSchema>
export type RegisterForm = z.input<typeof registerSchema>