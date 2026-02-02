import type React from "react"

interface RiskNoteListItemProps {
  label: string
  value: React.ReactNode
  className?: string
  noBorderRight?: boolean
  showLabel?: boolean
}

export const RiskNoteListItem = ({
  label,
  value,
  className = "",
  noBorderRight = false,
  showLabel = true,
}: RiskNoteListItemProps) => {
  return (
    <div
      className={`border-l border-b border-black p-1.5 px-3 text-[10px] flex items-start gap-2 bg-white ${
        !noBorderRight ? "border-r" : ""
      } ${className}`}
    >
      <div className="mt-1 h-1 w-1 rounded-full bg-black/60 shrink-0" />
      <div className="flex-1 leading-tight">
        {showLabel && label && (
          <span className="font-bold text-black uppercase text-[8px] mr-1.5">
            {label}:
          </span>
        )}
        <span className="text-gray-800">{value}</span>
      </div>
    </div>
  )
}
