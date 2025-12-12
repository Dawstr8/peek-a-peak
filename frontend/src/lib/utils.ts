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

export const getMinMax = <T>(items: T[]): [T | undefined, T | undefined] => {
  if (items.length === 0) {
    return [undefined, undefined];
  }

  const first = items[0];

  if (first instanceof Date) {
    const dates = items as Date[];
    const min = new Date(Math.min(...dates.map((d) => d.getTime())));
    const max = new Date(Math.max(...dates.map((d) => d.getTime())));
    return [min as T, max as T];
  }

  if (typeof first === "number") {
    const numbers = items as number[];
    return [Math.min(...numbers) as T, Math.max(...numbers) as T];
  }

  if (typeof first === "string") {
    const strings = items as string[];
    return [
      strings.reduce((a, b) => (a < b ? a : b)) as T,
      strings.reduce((a, b) => (a > b ? a : b)) as T,
    ];
  }

  return [undefined, undefined];
};

export const getRangeDisplay = <T>(
  min: T | undefined,
  max: T | undefined,
): string => {
  return min === max ? `${min}` : `${min} - ${max}`;
};
