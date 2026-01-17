// types/index.ts - Frontend TypeScript types matching backend schemas

export type UserRole = "startup" | "enterprise" | "admin";

export interface User {
  id: string;
  clerk_user_id: string;
  email: string;
  role: UserRole;
  created_at: string;
}

export interface Startup {
  id: string;
  user_id: string;
  name: string;
  industry: string;
  arr_range: string;
  description: string;
  credibility_score: number;
  created_at: string;
}

export interface Launch {
  id: string;
  startup_id: string;
  title: string;
  tagline: string;
  description: string;
  upvotes: number;
  featured: boolean;
  created_at: string;
}

export interface Review {
  id: string;
  startup_id: string;
  user_id: string;
  reviewer_role: "enterprise" | "customer";
  content: string;
  verified: boolean;
  created_at: string;
}

export interface EnterpriseFeedback {
  id: string;
  startup_id: string;
  enterprise_id: string;
  rating: number;
  content: string;
  verified: boolean;
  created_at: string;
}

export interface ScoreDetails {
  score: number;
  max: number;
  details: {
    [key: string]: any;
  };
}

export interface CredibilityBreakdown {
  launch_engagement: ScoreDetails;
  peer_reviews: ScoreDetails;
  enterprise_feedback: ScoreDetails;
  profile_completeness: ScoreDetails;
}

export interface CredibilityScoreResponse {
  startup_id: string;
  overall_score: number;
  breakdown: CredibilityBreakdown;
  last_updated: string;
}