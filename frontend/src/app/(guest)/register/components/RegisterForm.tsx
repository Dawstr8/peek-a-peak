"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { AuthClient } from "@/lib/auth/client";
import type { User, UserCreate } from "@/lib/users/types";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const registerSchema = z.object({
  email: z.email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

type RegisterFormData = z.infer<typeof registerSchema>;

type RegisterFormProps = {
  handleRegisterSuccess: () => void;
};

export function RegisterForm({ handleRegisterSuccess }: RegisterFormProps) {
  const form = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (registerForm: UserCreate) => AuthClient.register(registerForm),
    onSuccess: (user: User) => {
      handleRegisterSuccess();
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    mutate({
      email: data.email,
      password: data.password,
    });
  };

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-4"
        noValidate
      >
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  type="email"
                  placeholder="Enter your email"
                  {...field}
                  disabled={isPending}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input
                  type="password"
                  placeholder="Enter your password"
                  {...field}
                  disabled={isPending}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {isError && (
          <div className="text-destructive text-center text-sm">
            {error.message}
          </div>
        )}

        <Button type="submit" className="w-full" disabled={isPending}>
          {isPending ? "Signing Up..." : "Sign Up"}
        </Button>
      </form>
    </Form>
  );
}
