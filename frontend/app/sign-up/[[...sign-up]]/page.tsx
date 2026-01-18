"use client";

import { SignUp } from "@clerk/nextjs";
import { useState } from "react";

export default function SignUpPage() {
  const [selectedRole, setSelectedRole] = useState<"startup" | "enterprise">(
    "startup"
  );

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Join EthAum.ai
          </h1>
          <p className="text-gray-600">
            Create your account and start building credibility
          </p>
        </div>

        {/* Role Selection */}
        <div className="bg-white rounded-lg shadow border border-gray-200 p-6 mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            I am signing up as:
          </label>

          <div className="space-y-3">
            {/* Startup */}
            <label className="flex items-start p-4 border-2 rounded-lg cursor-pointer transition hover:border-blue-300 hover:bg-blue-50">
              <input
                type="radio"
                name="role"
                value="startup"
                checked={selectedRole === "startup"}
                onChange={() => setSelectedRole("startup")}
                className="mt-1 w-4 h-4 text-blue-600"
              />
              <div className="ml-3">
                <div className="font-semibold text-gray-900">
                  🚀 Startup Founder
                </div>
                <div className="text-xs text-gray-600">
                  Launch products, build credibility, connect with enterprises
                </div>
              </div>
            </label>

            {/* Enterprise */}
            <label className="flex items-start p-4 border-2 rounded-lg cursor-pointer transition hover:border-blue-300 hover:bg-blue-50">
              <input
                type="radio"
                name="role"
                value="enterprise"
                checked={selectedRole === "enterprise"}
                onChange={() => setSelectedRole("enterprise")}
                className="mt-1 w-4 h-4 text-blue-600"
              />
              <div className="ml-3">
                <div className="font-semibold text-gray-900">
                  🏢 Enterprise Buyer
                </div>
                <div className="text-xs text-gray-600">
                  Discover validated startups, evaluate credibility
                </div>
              </div>
            </label>
          </div>
        </div>

        {/* Clerk Form */}
        <SignUp
          unsafeMetadata={{
            role: selectedRole,
          }}
        />
      </div>
    </div>
  );
}
