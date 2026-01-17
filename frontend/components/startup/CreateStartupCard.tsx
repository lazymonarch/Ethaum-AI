///Users/lakshan/ethaum-ai/frontend/components/startup/CreateStartupCard.tsx

"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { createStartup } from "@/lib/api";

interface Props {
  onCreated: () => void;
}

export default function CreateStartupCard({ onCreated }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [form, setForm] = useState({
    name: "",
    industry: "",
    arr_range: "",
    description: "",
  });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createStartup(form);
      onCreated();
    } catch (err: any) {
      setError(
        err.response?.data?.detail || "Failed to create startup profile"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Create Your Startup Profile</CardTitle>
      </CardHeader>

      <CardContent>
        <p className="text-sm text-gray-600 mb-6">
          This information is used to calculate your credibility score and
          present your startup to enterprises.
        </p>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded p-3 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Startup Name"
            value={form.name}
            onChange={(v) => setForm({ ...form, name: v })}
            required
          />

          <Input
            label="Industry"
            value={form.industry}
            onChange={(v) => setForm({ ...form, industry: v })}
            placeholder="Fintech, SaaS, AI, HealthTech"
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              ARR Range (₹)
            </label>

            <select
              value={form.arr_range}
              onChange={(e) =>
                setForm({ ...form, arr_range: e.target.value })
              }
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select ARR Range</option>
              <option value="0-5 Cr">0–5 Cr</option>
              <option value="5-25 Cr">5–25 Cr</option>
              <option value="25-100 Cr">25–100 Cr</option>
              <option value="100+ Cr">100+ Cr</option>
            </select>
          </div>


          <Textarea
            label="Description"
            value={form.description}
            onChange={(v) => setForm({ ...form, description: v })}
            required
          />

          <Button
            type="submit"
            disabled={loading}
            className="w-full"
          >
            {loading ? "Creating..." : "Create Startup Profile"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

function Input({
  label,
  value,
  onChange,
  required,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  required?: boolean;
  placeholder?: string;
}) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      <input
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
        placeholder={placeholder}
      />
    </div>
  );
}

function Textarea({
  label,
  value,
  onChange,
  required,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  required?: boolean;
}) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      <textarea
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm min-h-[100px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
      />
    </div>
  );
}
