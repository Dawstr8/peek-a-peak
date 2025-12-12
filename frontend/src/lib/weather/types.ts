export interface WeatherCondition {
  main?: string;
  description?: string;
  icon?: string;
}

export interface WeatherRecord {
  sunrise?: string;
  sunset?: string;
  temp?: number;
  feelsLike?: number;
  dewPoint?: number;
  pressure?: number;
  humidity?: number;
  clouds?: number;
  visibility?: number;
  windSpeed?: number;
  windDeg?: number;
  rain?: number;
  snow?: number;
  conditions: WeatherCondition[];
}

export enum WeatherRecordDetailsKeys {
  TEMPERATURE = "temperature",
  WIND_SPEED = "windSpeed",
  SUNRISE = "sunrise",
  SUNSET = "sunset",
}
