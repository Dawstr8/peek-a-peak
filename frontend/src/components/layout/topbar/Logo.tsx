import Image from "next/image";
import Link from "next/link";

export default function Logo() {
  return (
    <Link
      href="/"
      className="flex items-center transition-opacity hover:opacity-80"
    >
      <Image
        src="/logo.svg"
        alt="Peek-a-Peak Mountains"
        width={55}
        height={35}
        priority
        className="mb-1 h-7 w-auto"
      />
      <span className="ml-3 scroll-m-20 text-xl font-semibold tracking-tight whitespace-nowrap">
        <span className="text-primary">Peek</span>
        <span className="text-foreground">-a-</span>
        <span className="text-chart-1">Peak</span>
      </span>
    </Link>
  );
}
