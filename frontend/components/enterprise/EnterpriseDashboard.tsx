//frontend/components/enterprise/EnterpriseDashboard.tsx

"use client";

import { useEffect, useState } from "react";
import {
    setAuthToken,
    getAllStartups,
    getMyEnterpriseFeedback,
} from "@/lib/api";
import Link from "next/link";
import type { Startup } from "@/types";

interface Props {
    token: string;
}

export default function EnterpriseDashboard({ token }: Props) {
    const [loading, setLoading] = useState(true);
    const [startups, setStartups] = useState<Startup[]>([]);
    const [reviewedCount, setReviewedCount] = useState(0);

    useEffect(() => {
        async function load() {
            try {
                setAuthToken(token);

                // 1️⃣ Fetch all startups (global, allowed)
                const allStartups = await getAllStartups();
                setStartups(allStartups);

                // 2️⃣ Fetch ONLY this enterprise's feedback
                const myFeedback = await getMyEnterpriseFeedback();

                // 3️⃣ Count unique startups reviewed by THIS enterprise
                const reviewedStartupIds = new Set(
                    myFeedback.map((f) => f.startup_id)
                );

                setReviewedCount(reviewedStartupIds.size);
            } catch (err) {
                console.error("Failed to load enterprise dashboard:", err);
            } finally {
                setLoading(false);
            }
        }

        load();
    }, [token]);

    if (loading) {
        return (
            <p className="text-gray-500 mt-6">
                Loading enterprise insights…
            </p>
        );
    }

    const highCred = startups.filter(
        (s) => s.credibility_score >= 80
    );

    const topStartups = [...startups]
        .sort((a, b) => b.credibility_score - a.credibility_score)
        .slice(0, 5);

    return (
        <div className="space-y-8 mt-6">
            {/* Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatCard label="Total Startups" value={startups.length} />
                <StatCard
                    label="High Credibility (80+)"
                    value={highCred.length}
                />
                <StatCard
                    label="Reviewed by You"
                    value={reviewedCount}
                />
            </div>

            {/* Recommended */}
            <div>
                <h2 className="text-xl font-semibold mb-4">
                    Recommended Startups
                </h2>

                <div className="space-y-3">
                    {topStartups.map((s) => (
                        <div
                            key={s.id}
                            className="bg-white border rounded-lg p-4 flex justify-between items-center"
                        >
                            <div>
                                <p className="font-semibold">{s.name}</p>
                                <p className="text-sm text-gray-500">
                                    {s.industry}
                                </p>
                            </div>

                            <div className="flex items-center gap-4">
                                <span className="font-bold text-lg">
                                    {s.credibility_score}/100
                                </span>
                                <Link
                                    href={`/startups/${s.id}`}
                                    className="text-blue-600 text-sm font-medium"
                                >
                                    View →
                                </Link>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* CTA */}
            <div className="bg-blue-50 p-6 rounded-lg">
                <h3 className="font-semibold mb-2">
                    Want to explore more?
                </h3>
                <Link
                    href="/startups"
                    className="text-blue-600 font-medium"
                >
                    Go to Discover Startups →
                </Link>
            </div>
        </div>
    );
}

function StatCard({
    label,
    value,
}: {
    label: string;
    value: number;
}) {
    return (
        <div className="bg-white border rounded-lg p-6">
            <p className="text-sm text-gray-500">{label}</p>
            <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
    );
}
