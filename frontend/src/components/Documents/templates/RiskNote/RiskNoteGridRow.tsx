import type React from "react"

interface GridField {
  label: string
  value: React.ReactNode
}

interface RiskNoteGridRowProps {
  label: string // Section Label on the left
  fields: GridField[]
  className?: string
}

export const RiskNoteGridRow = ({
  label,
  fields,
  className = "",
}: RiskNoteGridRowProps) => {
  return (
    <div
      className={`grid grid-cols-12 border-x border-b border-black bg-white ${className}`}
    >
      <div className="col-span-3 text-[10px] font-bold uppercase text-black bg-gray-50/50 p-2 border-r border-black flex items-center">
        {label}
      </div>
      <div
        className="col-span-9 grid"
        style={{ gridTemplateColumns: `repeat(${fields.length}, 1fr)` }}
      >
        {fields.map((field, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${
              idx !== fields.length - 1 ? "border-r border-black" : ""
            }`}
          >
            <div className="text-[9px] font-bold uppercase bg-gray-50/30 p-1 px-2 border-b border-black/10 text-black/70">
              {field.label}
            </div>
            <div className="text-[10px] p-2 px-2 text-gray-900 font-medium leading-tight">
              {field.value}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
