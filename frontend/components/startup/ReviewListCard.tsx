// components/startup/ReviewListCard.tsx

"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import { Review } from "@/types";
import { formatDate } from "@/lib/utils";
import { CheckCircle, Clock } from "lucide-react";

interface ReviewListCardProps {
  reviews: Review[];
}

export default function ReviewListCard({ reviews }: ReviewListCardProps) {
  const verifiedCount = reviews.filter((r) => r.verified).length;

  if (reviews.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Customer Reviews</CardTitle>
        </CardHeader>
        <CardContent>
          <EmptyState />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Customer Reviews ({reviews.length})</CardTitle>
          <span className="text-sm text-gray-600">
            {verifiedCount} verified
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {reviews.map((review) => (
            <ReviewItem key={review.id} review={review} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function ReviewItem({ review }: { review: Review }) {
  return (
    <div className="p-4 border border-gray-200 rounded-lg">
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          <Badge variant={review.verified ? "success" : "default"}>
            {review.verified ? (
              <>
                <CheckCircle className="w-3 h-3 mr-1" />
                Verified
              </>
            ) : (
              <>
                <Clock className="w-3 h-3 mr-1" />
                Pending
              </>
            )}
          </Badge>
          <span className="text-xs text-gray-500 capitalize">
            {review.reviewer_role}
          </span>
        </div>
        <span className="text-xs text-gray-500">
          {formatDate(review.created_at)}
        </span>
      </div>

      <p className="text-sm text-gray-700">{review.content}</p>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="text-center py-12">
      <div className="text-4xl mb-4">⭐</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        No Reviews Yet
      </h3>
      <p className="text-gray-600 text-sm mb-4">
        Request testimonials from customers to boost your credibility
      </p>
    </div>
  );
}