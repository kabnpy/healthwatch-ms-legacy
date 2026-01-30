import React from "react";

interface RiskNoteRowProps {
  label: string;
  value: React.ReactNode;
  className?: string;
  labelClassName?: string;
  valueClassName?: string;
}

export const RiskNoteRow = ({
  label,
  value,
  className = "",
  labelClassName = "",
  valueClassName = "",
}: RiskNoteRowProps) => {
  return (
    <div className={`grid grid-cols-12 border-x border-b border-black ${className}`}>
      <div
        className={`col-span-3 text-[10px] font-bold uppercase text-black bg-gray-50/50 p-2 border-r border-black flex items-center ${labelClassName}`}
      >
        {label}
      </div>
      <div className={`col-span-9 text-[11px] text-gray-900 p-2 ${valueClassName}`}>
        {value}
      </div>
    </div>
  );
};
