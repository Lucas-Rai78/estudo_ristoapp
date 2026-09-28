const API_URL = (
  import.meta.env.VITE_API_URL || 'http://localhost:8000'
).replace(/\/$/, '')

export class ApiError extends Error {
  readonly status: number
  readonly detail: string

  constructor(status: number, detail: string) {
    super(detail)

    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

export async function postJson<T>(
  path: string,
  body: unknown,
): Promise<T> {
  let response: Response

  try {
    response = await fetch(`${API_URL}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
  } catch {
    throw new ApiError(0, 'NETWORK_ERROR')
  }

  if (!response.ok) {
    const payload: unknown = await response.json().catch(() => null)

    const detail =
      payload &&
      typeof payload === 'object' &&
      'detail' in payload
        ? (payload as { detail: unknown }).detail
        : null

    throw new ApiError(
      response.status,
      typeof detail === 'string'
        ? detail
        : 'UNKNOWN_ERROR',
    )
  }

  return response.json() as Promise<T>
}