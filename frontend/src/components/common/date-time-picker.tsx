"use client";

import { useEffect, useState } from "react";

import { Calendar as CalendarIcon, Eraser, RotateCcw, X } from "lucide-react";

import {
  cn,
  combineDateAndTime,
  dateEqual,
  getTimeFromDate,
} from "@/lib/utils";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { useValueChange } from "@/hooks/use-value-change";

interface DateTimePickerProps {
  value?: Date;
  onChange?: (date: Date | undefined) => void;
}

export function DateTimePicker({ value, onChange }: DateTimePickerProps) {
  const { originalValue, hasValueChanged } = useValueChange<Date | undefined>(
    value,
    dateEqual,
  );

  const [open, setOpen] = useState(false);
  const [time, setTime] = useState<string>(getTimeFromDate(value));

  useEffect(() => {
    setTime(getTimeFromDate(value));
  }, [value]);

  const handleTimeChange = (newTime: string) => {
    const dateToUse = value || originalValue || new Date();
    onChange?.(combineDateAndTime(dateToUse, newTime));
  };

  const displayValue = value?.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          id="date-picker"
          className="w-full cursor-pointer justify-between"
        >
          <span className={cn(!displayValue && "text-muted-foreground")}>
            {displayValue || "When was this taken? *"}
          </span>
          <CalendarIcon className="size-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-fit p-0 lg:w-[var(--radix-popover-trigger-width)]"
        align="start"
        sideOffset={4}
      >
        <div className="flex items-center justify-between space-x-2 px-3 py-3">
          <h3 className="mr-auto text-sm font-medium whitespace-normal">
            Select date & time
          </h3>
          <div className="flex items-center justify-center">
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onChange?.(originalValue)}
                  disabled={!hasValueChanged()}
                  className="cursor-pointer opacity-75 hover:opacity-100"
                >
                  <RotateCcw className="size-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>Reset</TooltipContent>
            </Tooltip>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onChange?.(undefined)}
                  disabled={!value}
                  className="cursor-pointer opacity-75 hover:opacity-100"
                >
                  <Eraser className="size-4" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>Clear</TooltipContent>
            </Tooltip>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setOpen(false)}
              className="cursor-pointer opacity-75 hover:opacity-100"
            >
              <X className="size-4" />
            </Button>
          </div>
        </div>
        <Separator />
        <div className="flex flex-col lg:flex-row">
          <Calendar
            mode="single"
            captionLayout="dropdown"
            disabled={(date) => date > new Date()}
            selected={value}
            onSelect={(newDate: Date | undefined) =>
              newDate && onChange?.(combineDateAndTime(newDate, time))
            }
          />
          <div className="w-full flex-1 space-y-2 p-3">
            <Label
              htmlFor="popover-time-picker"
              className="text-sm font-medium"
            >
              Time
            </Label>
            <Input
              type="time"
              id="popover-time-picker"
              step="1"
              value={time}
              onChange={(e) => handleTimeChange(e.target.value)}
              className="bg-background appearance-none [&::-webkit-calendar-picker-indicator]:hidden [&::-webkit-calendar-picker-indicator]:appearance-none"
            />
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
