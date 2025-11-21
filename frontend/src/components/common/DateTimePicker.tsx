"use client";

import { useEffect, useState } from "react";

import { Calendar as CalendarIcon, Eraser, RotateCcw, X } from "lucide-react";

import { cn, dateEqual } from "@/lib/utils";

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

const DEFAULT_TIME = "12:00:00";

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
  const [date, setDate] = useState<Date | undefined>(value);
  const [time, setTime] = useState<string>(() => {
    return value?.toTimeString().slice(0, 8) || DEFAULT_TIME;
  });

  useEffect(() => {
    onChange?.(date && time ? combineDateAndTime(date, time) : undefined);
  }, [date, time, onChange]);

  const combineDateAndTime = (date: Date, time: string): Date => {
    const newDate = new Date(date);
    const [hours, minutes, seconds] = time.split(":").map(Number);
    newDate.setHours(hours, minutes, seconds || 0);

    return newDate;
  };

  const handleTimeChange = (newTime: string) => {
    const dateToUse = date || originalValue || new Date();
    setTime(newTime);
    setDate(dateToUse);
  };

  const handleResetDateTime = () => {
    setDate(originalValue);
    setTime(
      originalValue ? originalValue.toTimeString().slice(0, 8) : DEFAULT_TIME,
    );
  };

  const unsetDateTime = () => {
    setDate(undefined);
    setTime(DEFAULT_TIME);
  };

  const displayValue = date
    ? combineDateAndTime(date, time).toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      })
    : null;

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          id="date-picker"
          className="w-full cursor-pointer justify-between"
        >
          <span className={cn(!displayValue && "text-muted-foreground")}>
            {displayValue || "When was this taken?"}
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
                  onClick={handleResetDateTime}
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
                  onClick={unsetDateTime}
                  disabled={!date}
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
            disabled={(date) => date > new Date()}
            selected={date}
            captionLayout="dropdown"
            onSelect={setDate}
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
