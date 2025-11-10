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
            alt="Peak-a-Peak Mountains"
            width={55}
            height={35}
            priority
            className="mb-1 h-5 w-auto"
          />
          <span className="text-primary font-semibold tracking-tight whitespace-nowrap">
            <span className="text-primary">Peek</span>
            <span className="text-foreground">-a-</span>
            <span className="text-chart-1">Peak</span>
          </span>
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
