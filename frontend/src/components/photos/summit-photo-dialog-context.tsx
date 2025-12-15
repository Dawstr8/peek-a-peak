"use client";

import { createContext, useContext, useState } from "react";

import type { SummitPhoto } from "@/lib/photos/types";

interface SummitPhotoDialogContextType {
  isOpen: boolean;
  selectedPhoto: SummitPhoto | null;
  openDialog: (photo: SummitPhoto, photos?: SummitPhoto[]) => void;
  closeDialog: () => void;
}

const SummitPhotoDialogContext = createContext<
  SummitPhotoDialogContextType | undefined
>(undefined);

export function SummitPhotoDialogProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedPhoto, setSelectedPhoto] = useState<SummitPhoto | null>(null);

  const openDialog = (photo: SummitPhoto) => {
    setSelectedPhoto(photo);
    setIsOpen(true);
  };

  const closeDialog = () => {
    setIsOpen(false);
    setTimeout(() => {
      setSelectedPhoto(null);
    }, 200);
  };

  return (
    <SummitPhotoDialogContext.Provider
      value={{
        isOpen,
        selectedPhoto,
        openDialog,
        closeDialog,
      }}
    >
      {children}
    </SummitPhotoDialogContext.Provider>
  );
}

export function useSummitPhotoDialog() {
  const context = useContext(SummitPhotoDialogContext);
  if (context === undefined) {
    throw new Error(
      "useSummitPhotoDialog must be used within SummitPhotoDialogContext",
    );
  }

  return context;
}
