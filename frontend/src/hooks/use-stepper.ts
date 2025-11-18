import { useState } from "react";

export function useStepper(maxSteps: number) {
  const [step, setStep] = useState(0);

  const next = () => setStep((s) => Math.min(s + 1, maxSteps - 1));
  const back = () => setStep((s) => Math.max(s - 1, 0));
  const reset = () => setStep(0);
  const goTo = (targetStep: number) =>
    setStep(Math.max(0, Math.min(targetStep, maxSteps - 1)));

  return { step, next, back, reset, goTo };
}
