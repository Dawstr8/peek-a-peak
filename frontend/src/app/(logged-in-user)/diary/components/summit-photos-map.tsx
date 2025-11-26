"use client";

import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";
import { LatLng } from "leaflet";

import { UsersClient } from "@/lib/users/client";
import { User } from "@/lib/users/types";

import { InteractiveMap } from "@/components/common/interactive-map";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface SummitPhotosMapProps {
  user?: User;
  className?: string;
}

export default function SummitPhotosMap({
  user,
  className,
}: SummitPhotosMapProps) {
  const { data: summitPhotos } = useQuery({
    queryKey: ["users", user?.username, "photos"],
    queryFn: () => UsersClient.getPhotosByUser(user!.username),
    enabled: !!user,
  });

  const locations: LatLng[] = useMemo(() => {
    const locs: LatLng[] = [];
    if (!summitPhotos) return locs;

    summitPhotos.forEach((photo) => {
      if (!photo.lat || !photo.lng) return;

      locs.push(new LatLng(photo.lat, photo.lng));
    });

    return locs;
  }, [summitPhotos]);

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
