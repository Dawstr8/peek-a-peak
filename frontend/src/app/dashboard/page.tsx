import { checkIfAuthenticated } from "@/lib/auth/utils";
import { redirect } from "next/navigation";

export default async function Dashboard() {
  const isAuthenticated = await checkIfAuthenticated();
  if (!isAuthenticated) redirect("/login");

  return <></>;
}
