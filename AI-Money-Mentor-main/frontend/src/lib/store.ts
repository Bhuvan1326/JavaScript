import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  telegramId?: string
  email?: string
  name?: string
}

interface AppState {
  user: User | null
  setUser: (user: User | null) => void
  logout: () => void
  
  // Agent states
  activeAgent: string | null
  setActiveAgent: (agent: string | null) => void
  
  // Theme
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      user: null,
      setUser: (user) => set({ user }),
      logout: () => set({ user: null, activeAgent: null }),
      
      activeAgent: null,
      setActiveAgent: (agent) => set({ activeAgent: agent }),
      
      theme: 'light',
      toggleTheme: () => set((state) => ({ 
        theme: state.theme === 'light' ? 'dark' : 'light' 
      })),
    }),
    {
      name: 'ai-money-mentor-storage',
      partialize: (state) => ({ user: state.user, theme: state.theme }),
    }
  )
)
