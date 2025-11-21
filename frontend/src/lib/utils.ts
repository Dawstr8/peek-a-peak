import { type ClassValue, clsx } from "clsx";
import { LatLng } from "leaflet";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const latLngEqual = (
  a: LatLng | undefined,
  b: LatLng | undefined,
): boolean => {
  if (!a && !b) return true;
  if (!a || !b) return false;

  return a.equals(b);
};

export const dateEqual = (
  a: Date | undefined,
  b: Date | undefined,
): boolean => {
  if (!a && !b) return true;
  if (!a || !b) return false;

  return a.getTime() === b.getTime();
};

export const getTimeFromDate = (date: Date | undefined): string => {
  return date ? date.toTimeString().slice(0, 8) : "00:00:00";
};

export const combineDateAndTime = (date: Date, time: string): Date => {
  const newDate = new Date(date);
  const [hours, minutes, seconds] = time.split(":").map(Number);
  newDate.setHours(hours, minutes, seconds || 0);

  return newDate;
};
