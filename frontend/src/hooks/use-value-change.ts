import { useCallback, useRef } from "react";

type EqualityFn<T> = (a: T, b: T) => boolean;

export function useValueChange<T>(
  value: T,
  isEqual: EqualityFn<T> = (a, b) => a === b,
) {
  const { current: originalValue } = useRef<T>(value);

  const hasValueChanged = useCallback(() => {
    return !isEqual(value, originalValue);
  }, [value, originalValue, isEqual]);

  return { originalValue, hasValueChanged };
}
