import { DefaultDetailsFormatter } from "../common/formatter";
import { WeatherRecordDetailsKeys } from "./types";

class DefaultWeatherRecordDetailsFormatter extends DefaultDetailsFormatter {
  formatByKey(
    key: WeatherRecordDetailsKeys,
    value: number | string | undefined,
  ): string {
    switch (key) {
      case WeatherRecordDetailsKeys.TEMPERATURE:
        return this.formatNumber(value as number | undefined, " °C");

      case WeatherRecordDetailsKeys.WIND_SPEED:
        return this.formatNumber(value as number | undefined, " m/s");

      case WeatherRecordDetailsKeys.SUNRISE:
        return this.formatTime(value as string | undefined);

      case WeatherRecordDetailsKeys.SUNSET:
        return this.formatTime(value as string | undefined);

      default:
        return this.NOT_AVAILABLE;
    }
  }
}

export const weatherRecordDetailsFormatter =
  new DefaultWeatherRecordDetailsFormatter();
