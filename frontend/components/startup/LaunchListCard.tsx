// components/startup/LaunchListCard.tsx

"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import { Launch } from "@/types";
import { formatDate } from "@/lib/utils";
import { ArrowUp } from "lucide-react";

interface LaunchListCardProps {
  launches: Launch[];
}

export default function LaunchListCard({ launches }: LaunchListCardProps) {
  if (launches.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Launches</CardTitle>
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
        <CardTitle>Your Launches ({launches.length})</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {launches.map((launch) => (
            <LaunchItem key={launch.id} launch={launch} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function LaunchItem({ launch }: { launch: Launch }) {
  return (
    <div className="p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition">
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h4 className="font-semibold text-gray-900">{launch.title}</h4>
            {launch.featured && (
              <Badge variant="warning">Featured</Badge>
            )}
          </div>
          <p className="text-sm text-gray-600 mb-2">{launch.tagline}</p>
          <p className="text-xs text-gray-500">
            Launched {formatDate(launch.created_at)}
          </p>
        </div>

        {/* Upvote Count */}
        <div className="flex flex-col items-center ml-4">
          <div className="flex items-center justify-center w-12 h-12 bg-gray-100 rounded-lg">
            <ArrowUp className="w-5 h-5 text-gray-600" />
          </div>
          <span className="text-sm font-semibold text-gray-700 mt-1">
            {launch.upvotes}
          </span>
        </div>
      </div>

      {launch.description && (
        <p className="text-sm text-gray-600 mt-2 line-clamp-2">
          {launch.description}
        </p>
      )}
    </div>
  );
}

function EmptyState() {
  return (
    <div className="text-center py-12">
      <div className="text-4xl mb-4">🚀</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        No Launches Yet
      </h3>
      <p className="text-gray-600 text-sm mb-4">
        Launch your first product to start building credibility
      </p>
    </div>
  );
}