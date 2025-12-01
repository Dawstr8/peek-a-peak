import { EditAccountForm } from "./components/edit-account-form";

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div>
        <h2 className="text-4xl font-semibold md:text-3xl xl:text-4xl">
          Account settings
        </h2>
      </div>
      <EditAccountForm />
    </div>
  );
}
