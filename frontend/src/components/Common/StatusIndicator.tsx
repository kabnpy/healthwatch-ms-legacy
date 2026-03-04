import { cn } from "@/lib/utils"

interface StatusIndicatorProps {
  isActive: boolean
  label?: string
}

export const StatusIndicator = ({ isActive, label }: StatusIndicatorProps) => {
  const getStatusColor = () => {
    if (isActive) return "bg-green-500"
    switch (label) {
      case "Renewal Invited":
        return "bg-blue-500"
      case "Renewal Confirmed":
        return "bg-teal-500"
      case "Lapsed":
      case "Expired":
        return "bg-red-500"
      case "Cancelled":
        return "bg-orange-500"
      default:
        return "bg-gray-400"
    }
  }

  return (
    <div className="flex items-center gap-2">
      <span className={cn("size-2 rounded-full", getStatusColor())} />
      <span
        className={cn(
          "font-medium",
          isActive ? "text-foreground" : "text-muted-foreground",
        )}
      >
        {label || (isActive ? "Active" : "Inactive")}
      </span>
    </div>
  )
}
