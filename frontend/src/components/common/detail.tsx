import { cn } from "@/lib/utils";

interface DetailProps {
  text: string;
  icon?: React.ElementType;
  className?: string;
  children?: React.ReactNode;
}

export function Detail({ text, icon: Icon, className, children }: DetailProps) {
  return (
    <div className={cn("flex items-center space-x-1", className)}>
      {Icon && <Icon className="size-4" />}
      <span>{text}</span>
      {children}
    </div>
  );
}
