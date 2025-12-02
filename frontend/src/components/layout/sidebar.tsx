import { NotebookPen, User } from "lucide-react";

import {
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
  Sidebar as SidebarUI,
} from "@/components/ui/sidebar";

import { useAuthenticatedUser } from "@/hooks/use-authenticated-user";

import CallToAction from "./sidebar/call-to-action";
import Logo from "./sidebar/logo";
import Navigation from "./sidebar/navigation";
import Profile from "./sidebar/profile";

export function Sidebar() {
  const user = useAuthenticatedUser();

  const items = [
    { title: "Diary", url: `/diary/${user.username}`, icon: NotebookPen },
    { title: "Profile", url: "/profile", icon: User },
  ];

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
