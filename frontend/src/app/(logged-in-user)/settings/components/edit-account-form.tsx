"use client";

import { useEffect, useMemo } from "react";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { UsersClient } from "@/lib/users/client";
import type { UserUpdate } from "@/lib/users/types";

import { useAuth } from "@/components/auth/auth-context";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Switch } from "@/components/ui/switch";

const schema = z.object({
  isPrivate: z.boolean(),
});

const defaultValues = {
  isPrivate: false,
};

type FormData = z.infer<typeof schema>;

export function EditAccountForm() {
  const { user } = useAuth();

  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues,
  });
  const { reset, handleSubmit, control, formState } = form;

  const {
    data: updatedUser,
    mutate,
    isPending,
    isError,
    error,
  } = useMutation({
    mutationFn: (userUpdate: UserUpdate) => {
      if (!user) throw new Error("No user logged in");

      return UsersClient.updateUser(user.username, userUpdate);
    },
  });

  const initial = useMemo(() => {
    const values = updatedUser ?? user ?? defaultValues;

    return {
      isPrivate: values.isPrivate,
    };
  }, [user, updatedUser]);

  useEffect(() => {
    reset(initial);
  }, [initial, reset]);

  const onSubmit = (data: FormData) => {
    mutate({ isPrivate: data.isPrivate } as UserUpdate);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Edit account</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={control}
              name="isPrivate"
              render={({ field }) => (
                <FormItem className="flex items-center justify-between">
                  <FormLabel>Private account</FormLabel>
                  <FormControl>
                    <Switch
                      checked={field.value}
                      onCheckedChange={(v) => field.onChange(v)}
                      aria-label="Private account"
                      disabled={!user || isPending}
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

            <div className="flex gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => reset(initial)}
                disabled={!user || !formState.isDirty || isPending}
              >
                Discard
              </Button>
              <Button
                type="submit"
                disabled={!user || !formState.isDirty || isPending}
              >
                {isPending ? "Saving..." : "Save"}
              </Button>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
