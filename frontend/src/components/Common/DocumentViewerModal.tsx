import { Printer, X } from "lucide-react";
import { type ReactNode, useEffect, useRef, useState } from "react";
import { useReactToPrint } from "react-to-print";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface DocumentViewerModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function DocumentViewerModal({
  isOpen,
  onClose,
  title,
  children,
}: DocumentViewerModalProps) {
  const printRef = useRef<HTMLDivElement>(null);
  const viewportRef = useRef<HTMLDivElement>(null);
  const [scaleFactor, setScaleFactor] = useState(1);

  const handlePrint = useReactToPrint({
    contentRef: printRef,
    documentTitle: title,
  });

  useEffect(() => {
    if (!viewportRef.current) return;

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const containerWidth = entry.contentRect.width;
        // A4 width is 210mm. In px at 96dpi, that's ~794px.
        // We subtract padding (p-8 = 2rem * 2 = 64px)
        const targetWidth = 794;
        const availableWidth = containerWidth - 64;
        const newScale = Math.min(1, availableWidth / targetWidth);
        setScaleFactor(newScale);
      }
    });

    observer.observe(viewportRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className="h-[95vh] sm:max-w-[95vw] lg:max-w-7xl flex flex-col p-0 gap-0"
        showCloseButton={false}
      >
        <DialogHeader className="px-6 py-4 border-b flex flex-row items-center justify-between space-y-0">
          <DialogTitle>{title}</DialogTitle>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePrint()}
              className="gap-2"
            >
              <Printer className="size-4" />
              Print
            </Button>
            <DialogClose asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <X className="size-4" />
                <span className="sr-only">Close</span>
              </Button>
            </DialogClose>
          </div>
        </DialogHeader>

        <div
          ref={viewportRef}
          className="flex-1 overflow-auto bg-gray-100 p-8 flex flex-col items-center"
        >
          {/* The Document Container - A4-ish proportions with scaling */}
          <div
            style={{
              width: `${210 * scaleFactor}mm`,
              height: `${297 * scaleFactor}mm`,
              minHeight: `${297 * scaleFactor}mm`,
              transition: "all 0.2s ease-out",
            }}
            className="relative"
          >
            <div
              ref={printRef}
              style={{
                transform: `scale(${scaleFactor})`,
                transformOrigin: "top left",
                width: "210mm",
                height: "297mm",
              }}
              className="bg-white shadow-lg relative print:w-full print:h-full print:shadow-none print:transform-none print:static"
            >
              {children}
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
