"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

import { toast } from "sonner";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { RegisterForm } from "./components/RegisterForm";

export default function RegisterPage() {
  const router = useRouter();

  const handleRegisterSuccess = () => {
    toast.success("Account created successfully! You can now log in.");
    router.push("/login");
  };

  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-center text-2xl font-bold">
            Sign Up
          </CardTitle>
          <CardDescription className="text-center">
            Create your account to get started
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-1">
          <RegisterForm handleRegisterSuccess={handleRegisterSuccess} />
          <p className="text-muted-foreground text-center text-sm">
            Already have an account?{" "}
            <Link href="/login" className="underline">
              Sign in
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
