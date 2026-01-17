// components/startup/CreateLaunchModal.tsx

"use client";

import { useState } from "react";
import Modal from "@/components/ui/Modal";
import Button from "@/components/ui/Button";
import Toast from "@/components/ui/Toast";
import { createLaunch } from "@/lib/api";
import { Rocket } from "lucide-react";

interface CreateLaunchModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export default function CreateLaunchModal({
    isOpen,
    onClose,
    onSuccess,
}: CreateLaunchModalProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [showSuccessToast, setShowSuccessToast] = useState(false);

    const [form, setForm] = useState({
        title: "",
        tagline: "",
        description: "",
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await createLaunch(form);

            // Reset form
            setForm({ title: "", tagline: "", description: "" });

            // Show success toast
            setShowSuccessToast(true);

            // Close modal
            onClose();

            // Call success callback (will refresh dashboard)
            setTimeout(() => {
                onSuccess();
            }, 300);
        } catch (err: any) {
            console.error("Launch creation error:", err);
            setError(
                err.response?.data?.detail || "Failed to create launch. Please try again."
            );
        } finally {
            setLoading(false);
        }
    };

    const handleClose = () => {
        if (!loading) {
            setForm({ title: "", tagline: "", description: "" });
            setError(null);
            onClose();
        }
    };

    return (
        <>
            <Modal isOpen={isOpen} onClose={handleClose} title="Launch New Product">
                <form onSubmit={handleSubmit} className="space-y-5">
                    {/* Info Banner */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <div className="flex items-start gap-3">
                            <Rocket className="w-5 h-5 text-blue-600 mt-0.5" />
                            <div>
                                <h4 className="text-sm font-semibold text-blue-900 mb-1">
                                    Launch Impact
                                </h4>
                                <p className="text-xs text-blue-700">
                                    Launching a product increases your <strong>Launch Engagement</strong> score.
                                    Upvotes from the community will further boost your credibility.
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Error Display */}
                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3">
                            {error}
                        </div>
                    )}

                    {/* Title */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Product Title *
                        </label>
                        <input
                            type="text"
                            value={form.title}
                            onChange={(e) => setForm({ ...form, title: e.target.value })}
                            placeholder="e.g., Razorpay Smart Collect"
                            required
                            maxLength={100}
                            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                            {form.title.length}/100 characters
                        </p>
                    </div>

                    {/* Tagline */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Tagline *
                        </label>
                        <input
                            type="text"
                            value={form.tagline}
                            onChange={(e) => setForm({ ...form, tagline: e.target.value })}
                            placeholder="e.g., Automated collections platform for recurring payments"
                            required
                            maxLength={150}
                            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                            A brief one-liner explaining your product ({form.tagline.length}/150)
                        </p>
                    </div>

                    {/* Description */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Description *
                        </label>
                        <textarea
                            value={form.description}
                            onChange={(e) => setForm({ ...form, description: e.target.value })}
                            placeholder="Describe your product's key features, benefits, and value proposition..."
                            required
                            rows={6}
                            maxLength={1000}
                            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                            {form.description.length}/1000 characters
                        </p>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={handleClose}
                            disabled={loading}
                        >
                            Cancel
                        </Button>
                        <Button type="submit" disabled={loading}>
                            {loading ? "Launching..." : "Launch Product"}
                        </Button>
                    </div>
                </form>
            </Modal>

            {/* Success Toast */}
            <Toast
                message="🚀 Product launched successfully! Your credibility score is updating..."
                type="success"
                isVisible={showSuccessToast}
                onClose={() => setShowSuccessToast(false)}
                duration={4000}
            />
        </>
    );
}