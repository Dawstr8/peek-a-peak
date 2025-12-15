import { format } from "date-fns/format";

import { DetailsFormatter } from "./types";

export class DefaultDetailsFormatter implements DetailsFormatter {
  NOT_AVAILABLE = "N/A";

  formatNumber(value: number | undefined, suffix?: string): string {
    if (value === undefined || value === null) return this.NOT_AVAILABLE;

    return `${value.toFixed(1)}${suffix ?? ""}`;
  }

  formatTime(value: string | undefined): string {
    if (value === undefined || value === null) return this.NOT_AVAILABLE;

    try {
      const date = new Date(value);
      return format(date, "HH:mm");
    } catch {
      return this.NOT_AVAILABLE;
    }
  }

  formatCoordinate(value?: number): string {
    if (value === undefined || value === null) return this.NOT_AVAILABLE;

    return `${value.toFixed(6)}°`;
  }
}

export const detailsFormatter = new DefaultDetailsFormatter();
