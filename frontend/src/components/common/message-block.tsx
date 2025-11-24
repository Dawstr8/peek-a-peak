import { cn } from "@/lib/utils";

interface MessageBlockProps {
  iconComponent: React.ElementType;
  title: string;
  description: string;
  className?: string;
}

export function MessageBlock({
  iconComponent: IconComponent,
  title,
  description,
  className,
}: MessageBlockProps) {
  return (
    <div className={cn("space-y-3 text-center", className)}>
      <div className="bg-primary/20 text-primary mx-auto flex h-16 w-16 items-center justify-center rounded-full">
        <IconComponent className="h-8 w-8" />
      </div>
      <h3 className="text-foreground text-xl font-semibold">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}
