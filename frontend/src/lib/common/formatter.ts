import { format } from "date-fns/format";

import { DetailType, DetailsFormatter } from "./types";

export class DefaultDetailsFormatter implements DetailsFormatter {
  NOT_AVAILABLE = "N/A";

  formatByType(type: DetailType, value: number | string | undefined): string {
    switch (type) {
      case DetailType.TEMPERATURE:
        return this.formatNumber(value as number | undefined, "°C");

      case DetailType.SPEED:
        return this.formatNumber(value as number | undefined, " m/s");

      case DetailType.TIME:
        return this.formatTime(value as string | undefined);

      case DetailType.HEIGHT:
        return this.formatNumber(value as number | undefined, " m");

      case DetailType.DATE:
        return this.formatTime(value as string | undefined);

      case DetailType.COORDINATE:
        return this.formatCoordinate(value as number | undefined);

      default:
        return this.NOT_AVAILABLE;
    }
  }

  private formatNumber(value: number | undefined, suffix?: string): string {
    if (value === undefined || value === null) return this.NOT_AVAILABLE;

    return `${value.toFixed(1)}${suffix ?? ""}`;
  }

  private formatTime(value: string | undefined): string {
    if (value === undefined || value === null) return this.NOT_AVAILABLE;

    try {
      const date = new Date(value);
      return format(date, "HH:mm");
    } catch {
      return this.NOT_AVAILABLE;
    }
  }

  private formatCoordinate(value?: number): string {
    if (value === undefined || value === null) return this.NOT_AVAILABLE;

    return `${value.toFixed(6)}°`;
  }
}

export const detailsFormatter = new DefaultDetailsFormatter();
