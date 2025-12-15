import { format } from "date-fns/format";

import { DetailType } from "./types";

const NOT_AVAILABLE = "N/A";

export function formatByType(
  type: DetailType,
  value: number | string | undefined,
): string {
  switch (type) {
    case DetailType.TEMPERATURE:
      return formatNumber(value as number | undefined, "°C");

    case DetailType.SPEED:
      return formatNumber(value as number | undefined, " m/s");

    case DetailType.TIME:
      return formatTime(value as string | undefined);

    case DetailType.HEIGHT:
      return formatNumber(value as number | undefined, " m");

    case DetailType.DATE:
      return formatTime(value as string | undefined);

    case DetailType.COORDINATE:
      return formatCoordinate(value as number | undefined);

    default:
      return NOT_AVAILABLE;
  }
}

function formatNumber(value: number | undefined, suffix?: string): string {
  if (value === undefined || value === null) return NOT_AVAILABLE;

  return `${value.toFixed(1)}${suffix ?? ""}`;
}

function formatTime(value: string | undefined): string {
  if (value === undefined || value === null) return NOT_AVAILABLE;

  try {
    const date = new Date(value);
    return format(date, "HH:mm");
  } catch {
    return NOT_AVAILABLE;
  }
}

function formatCoordinate(value?: number): string {
  if (value === undefined || value === null) return NOT_AVAILABLE;

  return `${value.toFixed(6)}°`;
}
