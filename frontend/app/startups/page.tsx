"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@clerk/nextjs";
import Navbar from "@/components/Navbar";
import { setAuthToken } from "@/lib/api";
import api from "@/lib/api";

import type { Startup } from "@/types";
import type { EnterpriseProfile } from "@/lib/api";
import StartupFilters from "@/components/enterprise/StartupFilters";

/* ---------------------------
   TYPES
---------------------------- */

type ScoredStartup = {
    startup: Startup;
    score: number;
    reasons: string[];
};

/* ---------------------------
   HELPERS
---------------------------- */

function getCredibilityStyle(score: number) {
    if (score >= 85)
        return { color: "text-green-600", badge: "High Trust", badgeStyle: "bg-green-100 text-green-700" };
    if (score >= 70)
        return { color: "text-blue-600", badge: "Trusted", badgeStyle: "bg-blue-100 text-blue-700" };
    if (score >= 50)
        return { color: "text-yellow-600", badge: "Emerging", badgeStyle: "bg-yellow-100 text-yellow-700" };
    return { color: "text-gray-500", badge: "Early", badgeStyle: "bg-gray-100 text-gray-600" };
}

function getRecommendationScore(startup: Startup, profile: EnterpriseProfile) {
    let score = 0;
    if (profile.interested_industries?.includes(startup.industry)) score += 2;
    if (profile.preferred_arr_ranges?.includes(startup.arr_range)) score += 1;
    return score;
}

function getRecommendationReasons(startup: Startup, profile: EnterpriseProfile) {
    const reasons: string[] = [];
    if (profile.interested_industries?.includes(startup.industry)) reasons.push("Industry match");
    if (profile.preferred_arr_ranges?.includes(startup.arr_range)) reasons.push("ARR range match");
    return reasons;
}

/* ---------------------------
   PAGE
---------------------------- */

export default function StartupsDiscoveryPage() {
    const router = useRouter();
    const { getToken, isLoaded } = useAuth();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [recommended, setRecommended] = useState<{ startup: Startup; reasons: string[] }[]>([]);
    const [others, setOthers] = useState<Startup[]>([]);
    const [enterpriseProfile, setEnterpriseProfile] = useState<EnterpriseProfile | null>(null);

    // Filters
    const [industry, setIndustry] = useState<string | undefined>();
    const [arrRange, setArrRange] = useState<string | undefined>();
    const [minScore, setMinScore] = useState<number | undefined>(undefined);
    const [sort, setSort] = useState<"credibility" | "recent">("credibility");

    // Debounced filters
    const [debouncedFilters, setDebouncedFilters] = useState({
        industry,
        arrRange,
        minScore,
        sort,
    });

    useEffect(() => {
        const t = setTimeout(() => {
            setDebouncedFilters({ industry, arrRange, minScore, sort });
        }, 300);
        return () => clearTimeout(t);
    }, [industry, arrRange, minScore, sort]);

    async function fetchDiscovery() {
        try {
            if (!isLoaded) return;

            const token = await getToken({ template: "backend" });
            if (!token) throw new Error("Auth token missing");
            setAuthToken(token);

            setLoading(true);
            setError(null);

            let profile: EnterpriseProfile | null = null;
            try {
                const res = await api.get("/enterprise-profile/me");
                profile = res.data;
                setEnterpriseProfile(profile);
            } catch {
                setEnterpriseProfile(null);
            }

            const params = {
                ...(debouncedFilters.industry && { industry: debouncedFilters.industry }),
                ...(debouncedFilters.arrRange && { arr_range: debouncedFilters.arrRange }),
                ...(debouncedFilters.minScore !== undefined && {
                    min_score: debouncedFilters.minScore,
                }),
                sort: debouncedFilters.sort,
            };


            const { data } = await api.get("/startups/discover", { params });

            if (profile) {
                const scored: ScoredStartup[] = data.map((s: Startup) => ({
                    startup: s,
                    score: getRecommendationScore(s, profile),
                    reasons: getRecommendationReasons(s, profile),
                }));

                setRecommended(
                    scored
                        .filter((i) => i.score >= 2)
                        .sort((a, b) => b.score - a.score)
                        .map((i) => ({ startup: i.startup, reasons: i.reasons }))
                );

                setOthers(scored.filter((i) => i.score < 2).map((i) => i.startup));
            } else {
                setRecommended([]);
                setOthers(data);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        fetchDiscovery();
    }, [debouncedFilters, isLoaded]);

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50">
                <Navbar />
                <div className="px-6 py-10 text-gray-500">Loading startups…</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-50">
                <Navbar />
                <div className="px-6 py-10 text-red-600">{error}</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />

            <div className="max-w-7xl mx-auto px-6 py-10 space-y-10">
                <StartupFilters
                    industry={industry}
                    arrRange={arrRange}
                    minScore={minScore}
                    sort={sort}
                    onIndustryChange={setIndustry}
                    onArrRangeChange={setArrRange}
                    onMinScoreChange={setMinScore}
                    onSortChange={setSort}
                    onClear={() => {
                        setIndustry(undefined);
                        setArrRange(undefined);
                        setMinScore(undefined);
                        setSort("credibility");
                    }}
                />

                {/* Recommended */}
                {recommended.length > 0 && (
                    <section>
                        <h2 className="text-xl font-semibold mb-4">Recommended for You</h2>
                        <StartupGrid
                            startups={recommended.map((r) => r.startup)}
                            reasonsMap={Object.fromEntries(
                                recommended.map((r) => [r.startup.id, r.reasons])
                            )}
                        />
                    </section>
                )}

                {/* All Startups */}
                <section>
                    <h2 className="text-xl font-semibold mb-4">All Startups</h2>
                    {others.length === 0 ? (
                        <p className="text-sm text-gray-500">No startups match your filters.</p>
                    ) : (
                        <StartupGrid startups={others} />
                    )}
                </section>
            </div>
        </div>
    );
}

/* ---------------------------
   COMPONENTS
---------------------------- */

function StartupGrid({
    startups,
    reasonsMap,
}: {
    startups: Startup[];
    reasonsMap?: Record<string, string[]>;
}) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {startups.map((s) => (
                <StartupCard key={s.id} startup={s} reasons={reasonsMap?.[s.id]} />
            ))}
        </div>
    );
}

function StartupCard({ startup, reasons }: { startup: Startup; reasons?: string[] }) {
    const score = startup.credibility_score ?? 0;
    const cred = getCredibilityStyle(score);

    return (
        <div className="bg-white border rounded-lg p-5 hover:shadow-md transition">
            <div className="flex justify-between items-start gap-2">
                <h3 className="font-semibold">{startup.name}</h3>

                <div className="flex items-center gap-2">
                    {reasons && (
                        <div className="relative group">
                            <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded cursor-help">
                                Why?
                            </span>
                            <div className="absolute right-0 mt-2 hidden group-hover:block bg-gray-900 text-white text-xs rounded p-2 w-48">
                                <ul className="list-disc list-inside">
                                    {reasons.map((r) => (
                                        <li key={r}>{r}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}
                    <span className={`text-xs px-2 py-1 rounded ${cred.badgeStyle}`}>
                        {cred.badge}
                    </span>
                </div>
            </div>

            <p className="text-sm text-gray-500 mt-1">
                {startup.industry} · {startup.arr_range}
            </p>

            <div className="mt-6 flex justify-between items-end">
                <div>
                    <div className={`text-3xl font-bold ${cred.color}`}>
                        {score}
                        <span className="text-sm text-gray-400 ml-1">/100</span>
                    </div>
                    <p className="text-xs text-gray-500">Credibility</p>
                </div>

                <a href={`/startups/${startup.id}`} className="text-sm text-blue-600 hover:underline">
                    View →
                </a>
            </div>
        </div>
    );
}
