import { cn } from "@/lib/utils";

interface RangeProps {
  start: string | number;
  end: string | number;
  suffix?: string;
  icon?: React.ReactNode;
  className?: string;
}

export function Range({
  start,
  end,
  icon,
  className,
  suffix = "",
}: RangeProps) {
  return (
    <div className={cn("flex items-center space-x-1", className)}>
      {icon}
      <span>
        {start === end ? `${start}${suffix}` : `${start} - ${end}${suffix}`}
      </span>
    </div>
  );
}
