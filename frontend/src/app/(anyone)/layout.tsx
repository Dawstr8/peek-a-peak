"use client";

import { RequireAuth, useAuth } from "@/components/auth";
import Footer from "@/components/layout/footer";
import { Sidebar } from "@/components/layout/sidebar";
import Topbar from "@/components/layout/topbar";
import UploadDialog from "@/components/layout/upload-dialog";
import { UploadDialogProvider } from "@/components/layout/upload-dialog-context";
import { SummitPhotoDialog } from "@/components/photos/summit-photo-dialog";
import { SummitPhotoDialogProvider } from "@/components/photos/summit-photo-dialog-context";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Spinner } from "@/components/ui/spinner";

export default function AnyoneLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="absolute inset-0 flex items-center justify-center">
        <Spinner className="size-8" />
      </div>
    );
  }

  if (user) {
    return (
      <SummitPhotoDialogProvider>
        <RequireAuth>
          <UploadDialogProvider>
            <SidebarProvider>
              <Sidebar />
              <SidebarInset>
                <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
                  <div className="px-4">
                    <SidebarTrigger />
                  </div>
                </header>
                <main className="container mx-auto flex-1 p-10">
                  {children}
                </main>
                <UploadDialog />
                <SummitPhotoDialog />
                <Footer />
              </SidebarInset>
            </SidebarProvider>
          </UploadDialogProvider>
        </RequireAuth>
      </SummitPhotoDialogProvider>
    );
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Topbar />
      <SummitPhotoDialogProvider>
        <main className="container mx-auto flex-1 p-10">{children}</main>
        <SummitPhotoDialog />
      </SummitPhotoDialogProvider>
      <Footer />
    </div>
  );
}
