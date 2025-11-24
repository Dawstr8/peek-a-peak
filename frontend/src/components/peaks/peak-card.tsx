"use client";

import { MapPin, Mountain } from "lucide-react";

import type { Peak } from "@/lib/peaks/types";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface PeakCardProps {
  peak: Peak;
  children?: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export function PeakCard({
  peak,
  children,
  className,
  onClick,
}: PeakCardProps) {
  return (
    <Card key={peak.id} className={className} onClick={onClick}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Mountain className="h-4 w-4" />
          {peak.name}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="text-muted-foreground flex items-center gap-2 text-sm">
          <MapPin className="h-3 w-3" />
          <span>{peak.elevation}m elevation</span>
        </div>
        {children}
      </CardContent>
    </Card>
  );
}
