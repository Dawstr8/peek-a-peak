"use client";

import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";
import { LatLng } from "leaflet";

import { UsersClient } from "@/lib/users/client";

import { InteractiveMap } from "@/components/common/interactive-map";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface SummitPhotosMapProps {
  username?: string;
  className?: string;
}

export default function SummitPhotosMap({
  username,
  className,
}: SummitPhotosMapProps) {
  const { data: summitPhotosLocations } = useQuery({
    queryKey: ["users", username, "photos", "locations"],
    queryFn: () => UsersClient.getPhotosLocationsByUser(username!),
    enabled: !!username,
  });

  const locations: LatLng[] = useMemo(() => {
    const locs: LatLng[] = [];
    if (!summitPhotosLocations) return locs;

    summitPhotosLocations.forEach((location) => {
      if (!location.lat || !location.lng) return;

      locs.push(new LatLng(location.lat, location.lng));
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
