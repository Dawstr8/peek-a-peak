import Image from "next/image";

import { AspectRatio } from "@radix-ui/react-aspect-ratio";

interface PhotoAspectRatioProps {
  src: string;
  alt: string;
  ratio?: number;
  className?: string;
  children?: React.ReactNode;
}

export function PhotoAspectRatio({
  src,
  alt,
  ratio = 3 / 4,
  className,
  children,
}: PhotoAspectRatioProps) {
  return (
    <AspectRatio ratio={ratio} className={className}>
      <div className="relative h-full w-full">
        <Image src={src} alt={alt} fill className="object-cover" />
      </div>
      {children}
    </AspectRatio>
  );
}
