export const MIN_PASSWORD_LENGTH = 8

export const isEmail = (value: string): boolean => /^\S+@\S+\.\S+$/.test(value)