export interface LoginPayload {
  email: string
  password: string
  remember: boolean
}

export interface RegisterPayload {
  username: string
  email: string
  password: string
}

export interface RegisterForm extends RegisterPayload {
  confirm: string
  terms: boolean
}