import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import ClientLayout from "@/components/ClientLayout"
import NextTopLoader from "nextjs-toploader"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

export const metadata: Metadata = {
  title: "AI Money Mentor - Your Financial AI Assistant",
  description:
    "AI-powered financial advisory platform for Indian investors. Tax planning, mutual funds, FIRE planning, stock research, and more.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} font-sans min-h-screen flex flex-col antialiased bg-background text-foreground`}
      >
        <NextTopLoader color="#8b5cf6" showSpinner={false} />
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  )
}