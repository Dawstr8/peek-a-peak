import Link from "next/link";

import { LogIn } from "lucide-react";

import { Button } from "@/components/ui/button";

export default function LoginButton() {
  return (
    <Button asChild variant="outline">
      <Link href="/login">
        <LogIn className="h-4 w-4" />
        Sign In
      </Link>
    </Button>
  );
}
