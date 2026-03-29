"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Moon, Sun, User, LogOut, Menu, X } from "lucide-react"
import { toast, Toaster } from "sonner"

export default function ClientLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [user, setUser] = useState<any>(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [theme, setTheme] = useState<"light" | "dark">("light")
  const [mounted, setMounted] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const storedUser = localStorage.getItem("user")
    const storedLoggedIn = localStorage.getItem("isLoggedIn")
    const storedTheme = localStorage.getItem("theme") as "light" | "dark" | null

    if (storedUser) setUser(JSON.parse(storedUser))
    if (storedLoggedIn === "true") setIsLoggedIn(true)
    if (storedTheme) setTheme(storedTheme)
    setMounted(true)
  }, [])

  useEffect(() => {
    if (mounted) {
      document.documentElement.classList.toggle("dark", theme === "dark")
      localStorage.setItem("theme", theme)
    }
  }, [theme, mounted])

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener("scroll", handleScroll, { passive: true })
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem("user")
    localStorage.removeItem("isLoggedIn")
    // Clear dashboard statistics on logout
    localStorage.removeItem("dashboard_portfolio")
    localStorage.removeItem("dashboard_tax_saved")
    localStorage.removeItem("dashboard_fire")
    localStorage.removeItem("dashboard_health")

    setUser(null)
    setIsLoggedIn(false)
    toast.success("Logged out successfully")
    window.location.href = "/"
  }

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light")
  }

  if (!mounted) return null

  return (
    <>
      <header
        className={`sticky top-0 z-50 transition-all duration-300 gradient-border ${
          scrolled
            ? "bg-background/80 backdrop-blur-xl shadow-lg"
            : "bg-background/60 backdrop-blur-md"
        }`}
      >
        <nav className="container mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 group">
            <span className="text-2xl transition-transform duration-300 group-hover:scale-110">💰</span>
            <span className="hidden sm:inline text-xl font-bold gradient-text">AI Money Mentor</span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden sm:flex items-center gap-3">
            <Link
              href="/agents"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors relative after:absolute after:bottom-0 after:left-0 after:h-0.5 after:w-0 hover:after:w-full after:bg-primary after:transition-all after:duration-300"
            >
              Agents
            </Link>
            {isLoggedIn ? (
              <>
                <Link
                  href="/profile"
                  className="text-sm hover:text-primary transition-colors flex items-center gap-1"
                >
                  <User className="w-4 h-4" />
                  <span className="hidden md:inline">{user?.name || "Profile"}</span>
                </Link>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="text-muted-foreground hover:text-foreground"
                >
                  <LogOut className="w-4 h-4" />
                </Button>
              </>
            ) : (
              <Link href="/login">
                <Button
                  size="sm"
                  className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white border-0 shadow-md hover:shadow-lg transition-all duration-300"
                >
                  Login
                </Button>
              </Link>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              className="text-muted-foreground hover:text-foreground hover:bg-accent transition-all duration-200"
            >
              {theme === "light" ? (
                <Moon className="w-4 h-4" />
              ) : (
                <Sun className="w-4 h-4" />
              )}
            </Button>
          </div>

          {/* Mobile Toggle */}
          <div className="flex sm:hidden items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              className="text-muted-foreground"
            >
              {theme === "light" ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-muted-foreground"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </nav>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="sm:hidden border-t border-border bg-background/95 backdrop-blur-xl animate-fade-in">
            <div className="container mx-auto px-4 py-3 space-y-2">
              <Link
                href="/agents"
                className="block py-2 text-sm font-medium hover:text-primary transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                🤖 AI Agents
              </Link>
              {isLoggedIn ? (
                <>
                  <Link
                    href="/profile"
                    className="block py-2 text-sm hover:text-primary transition-colors"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    👤 {user?.name || "Profile"}
                  </Link>
                  <button
                    className="block py-2 text-sm text-destructive hover:opacity-80 transition-colors"
                    onClick={() => { handleLogout(); setMobileMenuOpen(false) }}
                  >
                    🚪 Logout
                  </button>
                </>
              ) : (
                <Link
                  href="/login"
                  className="block py-2 text-sm font-medium text-primary"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  🔑 Login / Sign Up
                </Link>
              )}
            </div>
          </div>
        )}
      </header>

      <main className="flex-1 container mx-auto px-4 py-6">{children}</main>

      <footer className="border-t border-border bg-card/80 backdrop-blur-sm py-6">
        <div className="container mx-auto px-4 text-center space-y-2">
          <p className="text-sm text-muted-foreground">
            ⚠️ SEBI Disclaimer: This is for educational purposes only. Not financial advice.
          </p>
          <p className="text-xs text-muted-foreground/60">
            © 2026 AI Money Mentor | ET AI Hackathon
          </p>
        </div>
      </footer>

      <Toaster richColors position="top-right" />
    </>
  )
}
