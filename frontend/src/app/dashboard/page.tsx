import { redirect } from "next/navigation";

import { checkIfAuthenticated } from "@/lib/auth/utils";

export default async function Dashboard() {
  const isAuthenticated = await checkIfAuthenticated();
  if (!isAuthenticated) redirect("/login");

  return <></>;
}
