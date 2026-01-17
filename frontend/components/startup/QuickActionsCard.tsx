// components/startup/QuickActionsCard.tsx

"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import CreateLaunchModal from "./CreateLaunchModal";
import { Rocket, Star, Building2 } from "lucide-react";

interface QuickActionsCardProps {
  onLaunchCreated: () => void;
}

export default function QuickActionsCard({ onLaunchCreated }: QuickActionsCardProps) {
  const [isLaunchModalOpen, setIsLaunchModalOpen] = useState(false);

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <ActionButton
              icon={<Rocket className="w-5 h-5" />}
              title="Launch Product"
              description="Publish a new product launch"
              onClick={() => setIsLaunchModalOpen(true)}
            />
            <ActionButton
              icon={<Star className="w-5 h-5" />}
              title="Request Reviews"
              description="Ask customers for testimonials"
              onClick={() => alert("Request reviews feature coming soon!")}
            />
            <ActionButton
              icon={<Building2 className="w-5 h-5" />}
              title="Get Enterprise Feedback"
              description="Connect with enterprise buyers"
              onClick={() => alert("Enterprise connection coming soon!")}
            />
          </div>
        </CardContent>
      </Card>

      {/* Launch Modal */}
      <CreateLaunchModal
        isOpen={isLaunchModalOpen}
        onClose={() => setIsLaunchModalOpen(false)}
        onSuccess={onLaunchCreated}
      />
    </>
  );
}

function ActionButton({
  icon,
  title,
  description,
  onClick,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition text-left"
    >
      <div className="flex items-center gap-3 mb-2">
        <div className="text-blue-600">{icon}</div>
        <h4 className="font-semibold text-gray-900 text-sm">{title}</h4>
      </div>
      <p className="text-xs text-gray-600">{description}</p>
    </button>
  );
}