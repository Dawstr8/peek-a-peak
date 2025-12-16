import Image from "next/image";

import { WeatherCondition } from "@/lib/weather/types";

interface WeatherConditionsRowProps {
  conditions?: WeatherCondition[];
  className?: string;
}

export function WeatherConditionsList({
  conditions,
  className,
}: WeatherConditionsRowProps) {
  return (
    <ul className={className}>
      {(!conditions || conditions.length === 0) && (
        <li>No weather conditions available.</li>
      )}

      {conditions?.map((condition) => (
        <li key={condition.id} className="flex items-center gap-1">
          <Image
            src={`https://openweathermap.org/img/wn/${condition.icon}@2x.png`}
            alt={condition.description}
            width={24}
            height={24}
          />
          <span className="capitalize">{condition.description}</span>
        </li>
      ))}
    </ul>
  );
}
