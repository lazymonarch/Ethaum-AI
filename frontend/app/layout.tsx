// app/layout.tsx - Root layout with Clerk authentication

import { ClerkProvider } from "@clerk/nextjs";
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EthAum.ai - Credibility Platform for B2B Startups",
  description:
    "AI-powered credibility and validation platform for Series A-D B2B startups",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="antialiased bg-gray-50">{children}</body>
      </html>
    </ClerkProvider>
  );
}