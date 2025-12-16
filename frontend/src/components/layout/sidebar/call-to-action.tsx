import { Plus } from "lucide-react";

import { useUploadDialog } from "@/components/layout/upload-dialog-context";
import { Button } from "@/components/ui/button";
import {
  SidebarGroup,
  SidebarMenu,
  SidebarMenuButton,
} from "@/components/ui/sidebar";

export default function CallToAction() {
  const { openDialog } = useUploadDialog();

  return (
    <SidebarGroup>
      <SidebarMenu>
        <SidebarMenuButton asChild tooltip="Add memory" onClick={openDialog}>
          <Button className="flex justify-start">
            <Plus />
            <span>Add memory</span>
          </Button>
        </SidebarMenuButton>
      </SidebarMenu>
    </SidebarGroup>
  );
}
