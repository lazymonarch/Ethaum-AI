import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const isPublic = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/post-signup",
]);

export default clerkMiddleware((auth, req) => {
  const { userId, sessionClaims } = auth();

  if (isPublic(req)) {
    return NextResponse.next();
  }

  if (!userId) {
    return NextResponse.redirect(new URL("/sign-in", req.url));
  }

  const role = (sessionClaims as any)?.role as string | undefined;

  if (req.nextUrl.pathname === "/dashboard" && role === "enterprise") {
    return NextResponse.redirect(new URL("/startups", req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ["/((?!_next|.*\\.(?:css|js|png|jpg|jpeg|svg|ico)).*)"],
};
