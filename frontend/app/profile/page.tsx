//frontend/app/profile/page.tsx

import { auth, currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Navbar from "@/components/Navbar";
import EnterpriseProfileForm from "@/components/enterprise/EnterpriseProfileForm";

export default async function ProfilePage() {
    const { userId } = await auth();
    const user = await currentUser();

    if (!userId || !user) {
        redirect("/sign-in");
    }

    const role = user.unsafeMetadata?.role;

    if (role !== "enterprise") {
        return (
            <div className="min-h-screen bg-gray-50">
                <Navbar />
                <div className="max-w-4xl mx-auto px-6 py-10">
                    <p className="text-gray-600">
                        Startup profile editing will be available soon.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />
            <div className="max-w-4xl mx-auto px-6 py-10">
                <h1 className="text-3xl font-bold text-gray-900">
                    Enterprise Profile
                </h1>
                <p className="text-gray-600 mt-2">
                    Manage your organization details and startup preferences
                </p>

                <div className="mt-8">
                    <EnterpriseProfileForm />
                </div>
            </div>
        </div>
    );
}
