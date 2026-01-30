import React from "react";

interface RiskNoteSectionProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export const RiskNoteSection = ({
  title,
  children,
  className = "",
}: RiskNoteSectionProps) => {
  return (
    <div className={`${className}`}>
      <div className="border-x border-b border-black bg-gray-100/50 px-2 py-1">
        <h3 className="text-[9px] font-black uppercase tracking-widest text-black">
          {title}
        </h3>
      </div>
      <div>{children}</div>
    </div>
  );
};