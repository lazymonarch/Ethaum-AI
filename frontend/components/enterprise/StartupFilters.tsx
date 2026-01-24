"use client";

interface StartupFiltersProps {
    industry?: string;
    arrRange?: string;
    minScore?: number;
    sort: "credibility" | "recent";

    onIndustryChange: (v?: string) => void;
    onArrRangeChange: (v?: string) => void;
    onMinScoreChange: (v?: number) => void;
    onSortChange: (v: "credibility" | "recent") => void;
    onClear: () => void;
}

const INDUSTRIES = ["Fintech", "SaaS", "AI", "Healthtech", "E-commerce"];
const ARR_RANGES = ["0-5 Cr", "5-25 Cr", "25-100 Cr", "100+ Cr"];
const MIN_SCORES = [50, 60, 70, 80];

export default function StartupFilters({
    industry,
    arrRange,
    minScore,
    sort,
    onIndustryChange,
    onArrRangeChange,
    onMinScoreChange,
    onSortChange,
    onClear,
}: StartupFiltersProps) {
    return (
        <div className="bg-white border rounded-lg p-4 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                <FilterSelect
                    label="Industry"
                    value={industry}
                    options={INDUSTRIES}
                    placeholder="All industries"
                    onChange={onIndustryChange}
                />

                <FilterSelect
                    label="ARR Range"
                    value={arrRange}
                    options={ARR_RANGES}
                    placeholder="All ARR ranges"
                    onChange={onArrRangeChange}
                />

                {/* Min Score */}
                <FilterSelect
                    label="Min Credibility"
                    value={minScore !== undefined ? minScore.toString() : ""}
                    options={MIN_SCORES.map(String)}
                    placeholder="Any score"
                    onChange={(v) =>
                        onMinScoreChange(v ? Number(v) : undefined)
                    }
                />

                {/* Sort */}
                <div>
                    <label className="block text-sm text-gray-600 mb-1">Sort By</label>
                    <select
                        value={sort}
                        onChange={(e) =>
                            onSortChange(e.target.value as "credibility" | "recent")
                        }
                        className="w-full border rounded-lg px-3 py-2 text-sm"
                    >
                        <option value="credibility">Credibility</option>
                        <option value="recent">Most Recent</option>
                    </select>
                </div>

                {/* Clear */}
                <div className="flex items-end">
                    <button
                        onClick={onClear}
                        className="w-full text-sm font-medium text-gray-600 border rounded-lg px-3 py-2 hover:bg-gray-50"
                    >
                        Clear Filters
                    </button>
                </div>
            </div>
        </div>
    );
}

/* ---------------------------
   Helper
---------------------------- */

function FilterSelect({
    label,
    value,
    options,
    placeholder,
    onChange,
}: {
    label: string;
    value?: string;
    options: string[];
    placeholder: string;
    onChange: (v?: string) => void;
}) {
    return (
        <div>
            <label className="block text-sm text-gray-600 mb-1">{label}</label>
            <select
                value={value ?? ""}
                onChange={(e) => onChange(e.target.value || undefined)}
                className="w-full border rounded-lg px-3 py-2 text-sm"
            >
                <option value="">{placeholder}</option>
                {options.map((opt) => (
                    <option key={opt} value={opt}>
                        {opt}
                    </option>
                ))}
            </select>
        </div>
    );
}
