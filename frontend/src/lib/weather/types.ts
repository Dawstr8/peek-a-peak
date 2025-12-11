export interface WeatherCondition {
  main?: string;
  description?: string;
  icon?: string;
}

export interface WeatherRecord {
  sunrise?: string;
  sunset?: string;
  temp?: number;
  feels_like?: number;
  dew_point?: number;
  pressure?: number;
  humidity?: number;
  clouds?: number;
  visibility?: number;
  wind_speed?: number;
  wind_deg?: number;
  rain?: number;
  snow?: number;
  conditions: WeatherCondition[];
}
