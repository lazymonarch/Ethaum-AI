// lib/utils.ts - Utility functions

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(date);
}

export function getCredibilityBadge(score: number): {
  label: string;
  color: string;
  bgColor: string;
} {
  if (score >= 85) {
    return {
      label: "Market Leader",
      color: "text-green-700",
      bgColor: "bg-green-50 border-green-200",
    };
  }
  if (score >= 70) {
    return {
      label: "Established",
      color: "text-blue-700",
      bgColor: "bg-blue-50 border-blue-200",
    };
  }
  if (score >= 50) {
    return {
      label: "Emerging",
      color: "text-yellow-700",
      bgColor: "bg-yellow-50 border-yellow-200",
    };
  }
  return {
    label: "Insufficient Data",
    color: "text-gray-700",
    bgColor: "bg-gray-50 border-gray-200",
  };
}