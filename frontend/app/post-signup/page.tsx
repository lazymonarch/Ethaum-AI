"use client";

import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function PostSignupPage() {
    const { user, isLoaded } = useUser();
    const router = useRouter();

    useEffect(() => {
        if (!isLoaded || !user) return;

        const role = user.unsafeMetadata?.role as
            | "startup"
            | "enterprise"
            | undefined;

        if (!role) {
            router.replace("/sign-in");
            return;
        }

        router.replace("/dashboard");
    }, [isLoaded, user, router]);

    return (
        <div className="min-h-screen flex items-center justify-center text-gray-600">
            Finalizing your account…
        </div>
    );
}
