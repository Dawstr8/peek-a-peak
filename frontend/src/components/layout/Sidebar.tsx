import { Images, LayoutDashboard, Mountain, Upload } from "lucide-react";

import { useAuth } from "@/components/auth/AuthContext";
import {
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
  Sidebar as SidebarUI,
} from "@/components/ui/sidebar";

import Logo from "./sidebar/Logo";
import Navigation from "./sidebar/Navigation";
import Profile from "./sidebar/Profile";

export const items = [
  { title: "Dashboard", url: "/dashboard", icon: LayoutDashboard },
  { title: "Gallery", url: "/gallery", icon: Images },
  { title: "Peaks", url: "/peaks", icon: Mountain },
  { title: "Upload", url: "/upload", icon: Upload },
];

export function Sidebar() {
  const { user } = useAuth();

  return (
    <SidebarUI collapsible="icon">
      <SidebarHeader>
        <Logo />
      </SidebarHeader>
      <SidebarContent>
        <Navigation items={items} />
      </SidebarContent>
      <SidebarFooter>{user && <Profile user={user} />}</SidebarFooter>
      <SidebarRail />
    </SidebarUI>
  );
}
