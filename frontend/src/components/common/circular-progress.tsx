"use client";

import { RadialBar, RadialBarChart } from "recharts";

import { ChartConfig, ChartContainer } from "@/components/ui/chart";

const chartConfig = {
  progress: {
    label: "Progress",
    color: "var(--chart-2)",
  },
  total: {
    label: "Total",
  },
} satisfies ChartConfig;

interface CircularProgressProps {
  value?: number;
  title?: string;
}

export default function CircularProgress({
  value,
  title,
}: CircularProgressProps) {
  const chartData = [{ progress: value || 0, total: 100 }];

  return (
    <div className="relative">
      <ChartContainer
        config={chartConfig}
        className="aspect-square h-32 w-full"
      >
        <RadialBarChart
          accessibilityLayer
          data={chartData}
          innerRadius="70%"
          outerRadius="130%"
        >
          <RadialBar dataKey="total" maxBarSize={0} />
          <RadialBar
            dataKey="progress"
            fill="var(--color-progress)"
            background
            cornerRadius={10}
          />
        </RadialBarChart>
      </ChartContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-foreground text-lg font-semibold">
          {title || `${value || 0}%`}
        </span>
      </div>
    </div>
  );
}
