import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  full_name: string
  is_active: boolean
}

interface AuthState {
  user: User
  isLoggedIn: boolean
  setUser: (user: User) => void
}

// Default guest user – authentication is disabled
const GUEST_USER: User = {
  id: '00000000-0000-0000-0000-000000000001',
  email: 'guest@edupilot.ai',
  full_name: 'Guest User',
  is_active: true,
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: GUEST_USER,
      isLoggedIn: true,
      setUser: (user) => set({ user, isLoggedIn: true }),
    }),
    { name: 'edupilot-auth' }
  )
)
