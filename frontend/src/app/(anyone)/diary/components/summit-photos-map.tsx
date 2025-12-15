"use client";

import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";

import { Location } from "@/lib/common/types";
import { UsersClient } from "@/lib/users/client";

import { InteractiveMap } from "@/components/common/interactive-map";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface SummitPhotosMapProps {
  username: string;
  className?: string;
}

export default function SummitPhotosMap({
  username,
  className,
}: SummitPhotosMapProps) {
  const { data: summitPhotosLocations } = useQuery({
    queryKey: ["users", username, "photos", "locations"],
    queryFn: () => UsersClient.getPhotosLocationsByUser(username),
  });

  const locations: Location[] = useMemo(() => {
    const locs: Location[] = [];
    if (!summitPhotosLocations) return locs;

    summitPhotosLocations.forEach((location) => {
      if (!location.lat || !location.lng) return;

      locs.push({ lat: location.lat, lng: location.lng });
    });

    return locs;
  }, [summitPhotosLocations]);

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Photo locations</CardTitle>
      </CardHeader>
      <CardContent>
        <InteractiveMap locations={locations} cluster />
      </CardContent>
    </Card>
  );
}
