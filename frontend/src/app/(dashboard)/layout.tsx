"use client";

import { redirect, usePathname } from "next/navigation";

import { useAuth } from "@/components/auth/AuthContext";
import Footer from "@/components/layout/Footer";
import { Sidebar } from "@/components/layout/Sidebar";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isLoading } = useAuth();

  const pathname = usePathname();

  if (!isLoading && !user) {
    const searchParams = new URLSearchParams();
    searchParams.set("returnTo", pathname);
    redirect(`/login?${searchParams.toString()}`);
  }

  return (
    <SidebarProvider>
      <Sidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
          <div className="px-4">
            <SidebarTrigger />
          </div>
        </header>
        <main className="flex-1">{children}</main>
        <Footer />
      </SidebarInset>
    </SidebarProvider>
  );
}
