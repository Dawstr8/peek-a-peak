import Link from "next/link";

import { Github, Mail } from "lucide-react";

import { Button } from "@/components/ui/button";

const socials = [
  {
    href: "https://github.com/Dawstr8/peek-a-peak",
    label: "GitHub",
    icon: Github,
  },
  {
    href: "mailto:dawid.strojek@gmail.com",
    label: "Email",
    icon: Mail,
  },
];

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer>
      <div className="mx-auto max-w-7xl px-6 py-4">
        <div className="flex flex-col items-center justify-around gap-2 md:flex-row">
          <p className="text-muted-foreground order-1 text-sm md:order-0">
            &copy; {currentYear} Peek-a-Peak
          </p>
          <div className="flex items-center space-x-4">
            {socials.map((social) => (
              <Button key={social.label} variant="ghost" size="sm" asChild>
                <Link href={social.href} aria-label={social.label}>
                  <social.icon className="size-4" />
                </Link>
              </Button>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
