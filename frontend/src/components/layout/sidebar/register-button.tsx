import Link from "next/link";

import { UserPlus } from "lucide-react";

import { Button } from "@/components/ui/button";

export default function RegisterButton() {
  return (
    <Button asChild>
      <Link href="/register">
        <UserPlus className="h-4 w-4" />
        Sign Up
      </Link>
    </Button>
  );
}
