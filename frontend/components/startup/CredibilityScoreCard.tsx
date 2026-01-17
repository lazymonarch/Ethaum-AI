// components/startup/CredibilityScoreCard.tsx

"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import { CredibilityScoreResponse } from "@/types";
import { getCredibilityBadge, formatDate } from "@/lib/utils";

interface CredibilityScoreCardProps {
  data: CredibilityScoreResponse;
}

export default function CredibilityScoreCard({ data }: CredibilityScoreCardProps) {
  const badge = getCredibilityBadge(data.overall_score);

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Your Credibility Score</CardTitle>
          <Badge
            variant={
              data.overall_score >= 85
                ? "success"
                : data.overall_score >= 70
                ? "info"
                : data.overall_score >= 50
                ? "warning"
                : "default"
            }
          >
            {badge.label}
          </Badge>
        </div>
      </CardHeader>

      <CardContent>
        {/* Big Score Display */}
        <div className="text-center mb-8">
          <div className="text-6xl font-bold text-gray-900 mb-2">
            {data.overall_score}
            <span className="text-3xl text-gray-400">/100</span>
          </div>
          <p className="text-sm text-gray-500">
            Last updated: {formatDate(data.last_updated)}
          </p>
        </div>

        {/* Breakdown */}
        <div className="space-y-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">
            Score Breakdown
          </h4>

          {/* Launch Engagement */}
          <ScoreBreakdownItem
            label="Launch Engagement"
            score={data.breakdown.launch_engagement.score}
            max={data.breakdown.launch_engagement.max}
            details={`${data.breakdown.launch_engagement.details.total_upvotes} upvotes across ${data.breakdown.launch_engagement.details.launch_count} launches`}
          />

          {/* Peer Reviews */}
          <ScoreBreakdownItem
            label="Peer Reviews"
            score={data.breakdown.peer_reviews.score}
            max={data.breakdown.peer_reviews.max}
            details={`${data.breakdown.peer_reviews.details.verified_reviews} verified out of ${data.breakdown.peer_reviews.details.total_reviews} total`}
          />

          {/* Enterprise Feedback */}
          <ScoreBreakdownItem
            label="Enterprise Feedback"
            score={data.breakdown.enterprise_feedback.score}
            max={data.breakdown.enterprise_feedback.max}
            details={
              data.breakdown.enterprise_feedback.details.avg_rating
                ? `Average rating: ${data.breakdown.enterprise_feedback.details.avg_rating.toFixed(1)}/5 (${data.breakdown.enterprise_feedback.details.feedback_count} feedbacks)`
                : "No enterprise feedback yet"
            }
          />

          {/* Profile Completeness */}
          <ScoreBreakdownItem
            label="Profile Completeness"
            score={data.breakdown.profile_completeness.score}
            max={data.breakdown.profile_completeness.max}
            details={
              data.breakdown.profile_completeness.details.missing_fields?.length > 0
                ? `Missing: ${data.breakdown.profile_completeness.details.missing_fields.join(", ")}`
                : "All fields complete"
            }
          />
        </div>
      </CardContent>
    </Card>
  );
}

// Sub-component for breakdown items
function ScoreBreakdownItem({
  label,
  score,
  max,
  details,
}: {
  label: string;
  score: number;
  max: number;
  details: string;
}) {
  const percentage = (score / max) * 100;

  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className="text-sm font-semibold text-gray-900">
          {score}/{max}
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
        <div
          className="bg-blue-600 h-2 rounded-full transition-all"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <p className="text-xs text-gray-500">{details}</p>
    </div>
  );
}