// frontend/components/enterprise/EnterpriseProfileForm.tsx

"use client";

import { useEffect, useState } from "react";
import {
    getMyEnterpriseProfile,
    createEnterpriseProfile,
    updateEnterpriseProfile,
    EnterpriseProfile,
} from "@/lib/api";

const INDUSTRIES = [
    "Fintech",
    "SaaS",
    "AI",
    "Healthtech",
    "E-commerce",
];

const ARR_RANGES = [
    "0-5 Cr",
    "5-25 Cr",
    "25-100 Cr",
    "100+ Cr",
];

export default function EnterpriseProfileForm() {
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [exists, setExists] = useState(false);

    const [form, setForm] = useState<Omit<EnterpriseProfile, "id">>({
        company_name: "",
        industry: "",
        company_size: "",
        location: "",
        interested_industries: [],
        preferred_arr_ranges: [],
        engagement_stage: "",
    });

    useEffect(() => {
        async function load() {
            try {
                const profile = await getMyEnterpriseProfile();
                setForm(profile);
                setExists(true);
            } catch {
                // 404 = no profile yet
            } finally {
                setLoading(false);
            }
        }
        load();
    }, []);

    const updateField = (key: keyof typeof form, value: any) => {
        setForm((f) => ({ ...f, [key]: value }));
    };

    const toggleMulti = (
        key: "interested_industries" | "preferred_arr_ranges",
        value: string
    ) => {
        setForm((f) => ({
            ...f,
            [key]: f[key].includes(value)
                ? f[key].filter((v) => v !== value)
                : [...f[key], value],
        }));
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            exists
                ? await updateEnterpriseProfile(form)
                : await createEnterpriseProfile(form);
            alert("Profile saved");
            setExists(true);
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <p className="text-gray-500">Loading profile…</p>;
    }

    return (
        <div className="space-y-8">
            {/* Company Info */}
            <Section title="Company Information">
                <Input label="Company Name" value={form.company_name}
                    onChange={(v) => updateField("company_name", v)} />

                <Input label="Industry" value={form.industry}
                    onChange={(v) => updateField("industry", v)} />

                <Input label="Company Size" value={form.company_size}
                    onChange={(v) => updateField("company_size", v)} />

                <Input label="Location" value={form.location}
                    onChange={(v) => updateField("location", v)} />
            </Section>

            {/* Preferences */}
            <Section title="Startup Preferences">
                <MultiSelect
                    label="Interested Industries"
                    options={INDUSTRIES}
                    values={form.interested_industries}
                    onToggle={(v) => toggleMulti("interested_industries", v)}
                />

                <MultiSelect
                    label="Preferred ARR Ranges"
                    options={ARR_RANGES}
                    values={form.preferred_arr_ranges}
                    onToggle={(v) => toggleMulti("preferred_arr_ranges", v)}
                />

                <Input
                    label="Engagement Stage (optional)"
                    value={form.engagement_stage || ""}
                    onChange={(v) => updateField("engagement_stage", v)}
                />
            </Section>

            <button
                onClick={handleSave}
                disabled={saving}
                className="bg-blue-600 text-white px-6 py-2 rounded"
            >
                {saving ? "Saving…" : "Save Profile"}
            </button>
        </div>
    );
}

/* ---------- helpers ---------- */

function Section({
    title,
    children,
}: {
    title: string;
    children: React.ReactNode;
}) {
    return (
        <div className="bg-white border rounded-lg p-6 space-y-4">
            <h2 className="text-lg font-semibold">{title}</h2>
            {children}
        </div>
    );
}

function Input({
    label,
    value,
    onChange,
}: {
    label: string;
    value: string;
    onChange: (v: string) => void;
}) {
    return (
        <div>
            <label className="block text-sm text-gray-600 mb-1">{label}</label>
            <input
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="w-full border rounded px-3 py-2"
            />
        </div>
    );
}

function MultiSelect({
    label,
    options,
    values,
    onToggle,
}: {
    label: string;
    options: string[];
    values: string[];
    onToggle: (v: string) => void;
}) {
    return (
        <div>
            <p className="text-sm text-gray-600 mb-2">{label}</p>
            <div className="flex flex-wrap gap-2">
                {options.map((opt) => (
                    <button
                        key={opt}
                        onClick={() => onToggle(opt)}
                        className={`px-3 py-1 rounded border text-sm ${values.includes(opt)
                            ? "bg-blue-600 text-white"
                            : "bg-white"
                            }`}
                    >
                        {opt}
                    </button>
                ))}
            </div>
        </div>
    );
}
