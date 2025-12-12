import { cn } from "@/lib/utils";

interface DetailProps {
  text: string;
  icon?: React.ElementType;
  className?: string;
}

export function Detail({ text, icon: Icon, className }: DetailProps) {
  return (
    <div className={cn("flex items-center space-x-1", className)}>
      {Icon && <Icon className="size-4" />}
      <span>{text}</span>
    </div>
  );
}
