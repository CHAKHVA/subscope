// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/layout/Header"; // Import Header
import Footer from "@/components/layout/Footer"; // Import Footer
import { cn } from "@/lib/utils"; // Import cn utility

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" }); // Add variable for font

export const metadata: Metadata = {
  title: "Subscope - Manage Your Subscriptions", // Update title
  description: "Your personal subscription and bill reminder assistant.", // Update description
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      {/* suppressHydrationWarning is often useful with themes */}
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased",
          inter.variable, // Apply font variable
        )}
      >
        <div className="relative flex min-h-screen flex-col">
          <Header />
          <main className="flex-grow container mx-auto px-4 py-8 md:px-6">
            {" "}
            {/* Main content area */}
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  );
}
