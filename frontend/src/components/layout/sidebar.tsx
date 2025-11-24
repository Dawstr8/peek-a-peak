import { NotebookPen, User } from "lucide-react";

import { useAuth } from "@/components/auth/auth-context";
import {
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
  Sidebar as SidebarUI,
} from "@/components/ui/sidebar";

import CallToAction from "./sidebar/call-to-action";
import Logo from "./sidebar/logo";
import Navigation from "./sidebar/navigation";
import Profile from "./sidebar/profile";

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
