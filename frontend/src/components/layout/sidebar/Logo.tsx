import Image from "next/image";

import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

export default function Logo() {
  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton>
          <Image
            src="/logo.svg"
            alt="Polish Peaks Mountains"
            width={55}
            height={35}
            priority
            className="mb-1 h-5 w-auto"
          />
          <span>Polish Peaks</span>
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
