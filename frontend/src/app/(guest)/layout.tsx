import Footer from "@/components/layout/Footer";
import Topbar from "@/components/layout/Topbar";

export default function GuestLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen flex-col">
      <Topbar />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}
