import { type ClassValue, clsx } from "clsx";
import { LatLng } from "leaflet";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function latLngEqual(
  a: LatLng | undefined,
  b: LatLng | undefined,
): boolean {
  if (!a && !b) return true;
  if (!a || !b) return false;

  return a.equals(b);
}

export function dateEqual(a: Date | undefined, b: Date | undefined): boolean {
  if (!a && !b) return true;
  if (!a || !b) return false;

  return a.getTime() === b.getTime();
}
