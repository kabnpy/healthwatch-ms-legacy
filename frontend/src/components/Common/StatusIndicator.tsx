import { cn } from "@/lib/utils"

interface StatusIndicatorProps {
  isActive: boolean
  label?: string
}

export const StatusIndicator = ({ isActive, label }: StatusIndicatorProps) => {
  return (
    <div className="flex items-center gap-2">
      <span
        className={cn(
          "size-2 rounded-full",
          isActive ? "bg-green-500" : "bg-gray-400",
        )}
      />
      <span className={isActive ? "" : "text-muted-foreground"}>
        {label || (isActive ? "Active" : "Inactive")}
      </span>
    </div>
  )
}
