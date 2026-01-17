// lib/api.ts - API client with Clerk authentication

import axios from "axios";
import type {
  Startup,
  Launch,
  Review,
  EnterpriseFeedback,
  CredibilityScoreResponse,
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Create axios instance
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add auth token to requests
export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
};

// --- STARTUP ENDPOINTS ---

export const getMyStartup = async (): Promise<Startup> => {
  const { data } = await api.get("/startups/me");
  return data;
};

export const getAllStartups = async (): Promise<Startup[]> => {
  const { data } = await api.get("/startups");
  return data;
};

export const getStartupById = async (id: string): Promise<Startup> => {
  const { data } = await api.get(`/startups/${id}`);
  return data;
};

export const createStartup = async (
  startupData: Partial<Startup>
): Promise<Startup> => {
  const { data } = await api.post("/startups", startupData);
  return data;
};

export const updateStartup = async (
  updates: Partial<Startup>
): Promise<Startup> => {
  const { data } = await api.put("/startups/me", updates);
  return data;
};

// --- LAUNCH ENDPOINTS ---

export const getAllLaunches = async (): Promise<Launch[]> => {
  const { data } = await api.get("/launches");
  return data;
};

export const getMyLaunches = async (): Promise<Launch[]> => {
  try {
    const { data } = await api.get("/launches/me");
    return data;
  } catch (err: any) {
    if (err.response?.status === 404) {
      return [];
    }
    throw err;
  }
};


export const createLaunch = async (
  launchData: Partial<Launch>
): Promise<Launch> => {
  const { data } = await api.post("/launches/", launchData);
  return data;
};

export const upvoteLaunch = async (launchId: string): Promise<Launch> => {
  const { data } = await api.post(`/launches/${launchId}/upvote`);
  return data;
};

// --- REVIEW ENDPOINTS ---

export const getReviewsByStartup = async (
  startupId: string
): Promise<Review[]> => {
  const { data } = await api.get(`/reviews/startup/${startupId}`);
  return data;
};

export const createReview = async (
  reviewData: Partial<Review>
): Promise<Review> => {
  const { data } = await api.post("/reviews", reviewData);
  return data;
};

export const verifyReview = async (reviewId: string): Promise<Review> => {
  const { data } = await api.post(`/reviews/${reviewId}/verify`);
  return data;
};

// --- ENTERPRISE FEEDBACK ENDPOINTS ---

export const getFeedbackByStartup = async (
  startupId: string
): Promise<EnterpriseFeedback[]> => {
  const { data } = await api.get(
    `/enterprise-feedback/startup/${startupId}`
  );
  return data;
};

export const submitFeedback = async (
  feedbackData: Partial<EnterpriseFeedback>
): Promise<EnterpriseFeedback> => {
  const { data } = await api.post("/enterprise-feedback", feedbackData);
  return data;
};

// --- CREDIBILITY SCORE ENDPOINTS ---

export const getMyCredibilityScore =
  async (): Promise<CredibilityScoreResponse> => {
    const { data } = await api.get("/credibility-score/");
    return data;
  };

export const getStartupCredibilityScore = async (
  startupId: string
): Promise<CredibilityScoreResponse> => {
  const { data } = await api.get(`/credibility-score/${startupId}`);
  return data;
};

export default api;