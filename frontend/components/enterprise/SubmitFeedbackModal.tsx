"use client";

import { useState } from "react";
import { submitFeedback } from "@/lib/api";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { Star } from "lucide-react";

interface SubmitFeedbackModalProps {
  startupId: string;
  onSuccess: () => void;
}

export default function SubmitFeedbackModal({
  startupId,
  onSuccess,
}: SubmitFeedbackModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [rating, setRating] = useState<number>(5);
  const [content, setContent] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!content.trim()) {
      setError("Please write some feedback before submitting.");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await submitFeedback({
        startup_id: startupId,
        rating,
        content,
      });

      // reset + close
      setIsOpen(false);
      setContent("");
      setRating(5);

      onSuccess();
    } catch (err: any) {
      console.error("❌ Failed to submit feedback:", err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        "Failed to submit feedback"
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      {/* Trigger */}
      <Button onClick={() => setIsOpen(true)}>
        Submit Enterprise Feedback
      </Button>

      {/* Modal */}
      <Modal
        isOpen={isOpen}
        title="Enterprise Feedback"
        onClose={() => setIsOpen(false)}
      >
        <div className="space-y-4">
          {/* Rating */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Rating
            </label>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <Star
                  key={star}
                  onClick={() => setRating(star)}
                  className={`w-6 h-6 cursor-pointer ${star <= rating
                      ? "text-yellow-500 fill-yellow-500"
                      : "text-gray-300"
                    }`}
                />
              ))}
            </div>
          </div>

          {/* Feedback */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Feedback
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={4}
              className="w-full border rounded-lg p-2 text-sm"
              placeholder="Describe your experience working with this startup..."
            />
          </div>

          {/* Error */}
          {error && (
            <p className="text-sm text-red-600">{error}</p>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-2 pt-2">
            <Button
              variant="outline"
              onClick={() => setIsOpen(false)}
              disabled={submitting}
            >
              Cancel
            </Button>

            <Button
              onClick={handleSubmit}
              disabled={submitting}
            >
              {submitting ? "Submitting..." : "Submit Feedback"}
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
}
