"use client";

import { RequireAuth } from "@/components/auth";
import Footer from "@/components/layout/footer";
import { Sidebar } from "@/components/layout/sidebar";
import UploadDialog from "@/components/layout/upload-dialog";
import { UploadDialogProvider } from "@/components/layout/upload-dialog-context";
import { SummitPhotoDialog } from "@/components/photos/summit-photo-dialog";
import { SummitPhotoDialogProvider } from "@/components/photos/summit-photo-dialog-context";
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
              <main className="container mx-auto flex-1 p-10">{children}</main>
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
