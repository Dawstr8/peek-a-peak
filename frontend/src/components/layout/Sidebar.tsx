import { NotebookPen, User } from "lucide-react";

import { useAuth } from "@/components/auth/AuthContext";
import {
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
  Sidebar as SidebarUI,
} from "@/components/ui/sidebar";

import CallToAction from "./sidebar/CallToAction";
import Logo from "./sidebar/Logo";
import Navigation from "./sidebar/Navigation";
import Profile from "./sidebar/Profile";

export const items = [
  { title: "Diary", url: "/diary", icon: NotebookPen },
  { title: "Profile", url: "/profile", icon: User },
];

export function Sidebar() {
  const { user } = useAuth();

  return (
    <SidebarUI collapsible="icon">
      <SidebarHeader>
        <Logo />
      </SidebarHeader>
      <SidebarContent>
        <CallToAction />
        <Navigation items={items} />
      </SidebarContent>
      <SidebarFooter>
        <Profile user={user} />
      </SidebarFooter>
      <SidebarRail />
    </SidebarUI>
  );
}
