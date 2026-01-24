//frontend/components/enterprise/StartupDetails.tsx

"use client";

import { useEffect, useState, useCallback } from "react";
import {
    setAuthToken,
    getStartupById,
    getStartupCredibilityScore,
    getReviewsByStartup,
    getFeedbackByStartup,
} from "@/lib/api";

import SubmitFeedbackModal from "./SubmitFeedbackModal";
import Badge from "@/components/ui/Badge";

import type {
    Startup,
    CredibilityScoreResponse,
    Review,
    EnterpriseFeedback,
} from "@/types";

interface StartupDetailsProps {
    startupId: string;
    token: string | null;
}

export default function StartupDetails({
    startupId,
    token,
}: StartupDetailsProps) {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [startup, setStartup] = useState<Startup | null>(null);
    const [credibility, setCredibility] =
        useState<CredibilityScoreResponse | null>(null);
    const [reviews, setReviews] = useState<Review[]>([]);
    const [feedback, setFeedback] = useState<EnterpriseFeedback[]>([]);

    const fetchData = useCallback(async () => {
        if (!token) {
            setError("Authentication token missing");
            setLoading(false);
            return;
        }

        try {
            setAuthToken(token);

            const [
                startupData,
                credibilityData,
                reviewsData,
                feedbackData,
            ] = await Promise.all([
                getStartupById(startupId),
                getStartupCredibilityScore(startupId),
                getReviewsByStartup(startupId),
                getFeedbackByStartup(startupId),
            ]);

            setStartup(startupData);
            setCredibility(credibilityData);
            setReviews(reviewsData);
            setFeedback(feedbackData);
        } catch (err: any) {
            console.error("❌ Failed to load startup details:", err);
            setError(
                err.response?.data?.detail ||
                err.message ||
                "Failed to load startup details"
            );
        } finally {
            setLoading(false);
        }
    }, [startupId, token]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    if (loading) {
        return <LoadingState />;
    }

    if (error || !startup || !credibility) {
        return <ErrorState message={error || "Startup not found"} />;
    }

    const verifiedReviews = reviews.filter((r) => r.verified);

    const avgRating =
        feedback.length > 0
            ? (
                feedback.reduce((sum, f) => sum + f.rating, 0) / feedback.length
            ).toFixed(1)
            : null;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-start justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">
                        {startup.name}
                    </h1>
                    <p className="text-gray-600 mt-1">
                        {startup.industry} · {startup.arr_range}
                    </p>
                </div>

                {/* Enterprise action */}
                <SubmitFeedbackModal
                    startupId={startupId}
                    onSuccess={fetchData}
                />
            </div>

            {/* Description */}
            <div className="bg-white border rounded-lg p-6">
                <p className="text-gray-700">{startup.description}</p>
            </div>

            {/* Credibility Score */}
            <div className="bg-white border rounded-lg p-6">
                <h2 className="text-xl font-semibold mb-4">
                    Credibility Score
                </h2>

                <div className="text-5xl font-bold mb-2">
                    {credibility.overall_score}
                    <span className="text-gray-400 text-2xl"> / 100</span>
                </div>

                <div className="space-y-3 mt-4">
                    {Object.entries(credibility.breakdown).map(
                        ([key, value]: any) => (
                            <div key={key}>
                                <div className="flex justify-between text-sm mb-1">
                                    <span className="capitalize">
                                        {key.replace("_", " ")}
                                    </span>
                                    <span>
                                        {value.score}/{value.max}
                                    </span>
                                </div>
                                <div className="w-full bg-gray-200 h-2 rounded">
                                    <div
                                        className="bg-blue-600 h-2 rounded"
                                        style={{
                                            width: `${(value.score / value.max) * 100}%`,
                                        }}
                                    />
                                </div>
                            </div>
                        )
                    )}
                </div>
            </div>

            {/* Reviews & Feedback */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Reviews */}
                <div className="bg-white border rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-3">
                        Verified Reviews ({verifiedReviews.length})
                    </h3>

                    {verifiedReviews.length === 0 ? (
                        <p className="text-sm text-gray-500">
                            No verified reviews yet
                        </p>
                    ) : (
                        <div className="space-y-3">
                            {verifiedReviews.slice(0, 3).map((review) => (
                                <div
                                    key={review.id}
                                    className="border rounded p-3"
                                >
                                    <Badge variant="success">Verified</Badge>
                                    <p className="text-sm mt-2">
                                        {review.content}
                                    </p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Enterprise Feedback */}
                <div className="bg-white border rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-3">
                        Enterprise Feedback ({feedback.length})
                    </h3>

                    {avgRating && (
                        <div className="mb-3 text-sm">
                            ⭐ Average rating{" "}
                            <span className="font-semibold">
                                {avgRating}/5
                            </span>
                        </div>
                    )}

                    {feedback.length === 0 ? (
                        <p className="text-sm text-gray-500">
                            No enterprise feedback yet
                        </p>
                    ) : (
                        <div className="space-y-3">
                            {feedback.slice(0, 3).map((fb) => (
                                <div
                                    key={fb.id}
                                    className="border rounded p-3"
                                >
                                    <div className="text-sm mb-1">
                                        ⭐ {fb.rating}/5
                                    </div>
                                    <p className="text-sm">{fb.content}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

/* -------------------- */
/* UI STATES            */
/* -------------------- */

function LoadingState() {
    return (
        <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-200 rounded w-1/3" />
            <div className="h-24 bg-gray-200 rounded" />
        </div>
    );
}

function ErrorState({ message }: { message: string }) {
    return (
        <div className="bg-red-50 border border-red-200 p-6 rounded-lg">
            <h3 className="font-semibold text-red-900 mb-2">
                Error Loading Startup
            </h3>
            <p className="text-red-700 text-sm">{message}</p>
        </div>
    );
}
