import {
  Item,
  ItemContent,
  ItemDescription,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";

interface MetadataItemProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  className?: string;
}

export function MetadataItem({
  icon,
  title,
  description,
  className,
}: MetadataItemProps) {
  return (
    <Item className={className}>
      <ItemMedia className="text-muted-foreground h-full">{icon}</ItemMedia>
      <ItemContent>
        <ItemTitle className="text-muted-foreground text-sm font-medium">
          {title}:
        </ItemTitle>
        <ItemDescription className="text-foreground font-mono text-base">
          {description}
        </ItemDescription>
      </ItemContent>
    </Item>
  );
}
