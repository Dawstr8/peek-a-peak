"use client";

import { useMemo } from "react";

import { useQuery } from "@tanstack/react-query";
import { LatLng } from "leaflet";

import { PhotoClient } from "@/lib/photos/client";

import { useAuth } from "@/components/auth/auth-context";
import { InteractiveMap } from "@/components/common/interactive-map";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface SummitPhotosMapProps {
  className?: string;
}

export default function SummitPhotosMap({ className }: SummitPhotosMapProps) {
  const { user } = useAuth();

  const { data: summitPhotos } = useQuery({
    queryKey: ["photos", "user", user?.username],
    queryFn: () => PhotoClient.getPhotosByUser(user!.username),
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
