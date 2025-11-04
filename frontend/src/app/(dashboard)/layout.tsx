"use client";

import { redirect } from "next/navigation";

import { useAuth } from "@/components/auth/AuthContext";
import Footer from "@/components/layout/Footer";
import Topbar from "@/components/layout/Topbar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isLoading } = useAuth();

  if (!isLoading && !user) {
    redirect("/login");
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Topbar />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}
