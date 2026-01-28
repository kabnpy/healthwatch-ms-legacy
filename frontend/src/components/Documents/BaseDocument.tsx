import React from "react"

interface BaseDocumentProps {
  title: string
  subtitle?: string
  documentNumber: string
  date: string
  children: React.ReactNode
  footerExtra?: React.ReactNode
}

export const BaseDocument = ({
  title,
  subtitle,
  documentNumber,
  date,
  children,
  footerExtra,
}: BaseDocumentProps) => {
  return (
    <div className="w-full h-full bg-white text-black p-8 font-serif overflow-auto relative shadow-sm border mx-auto max-w-[210mm]">
      {/* Universal Header */}
      <div className="flex justify-between items-start mb-8 border-b-2 border-black pb-6">
        <div>
          <h1 className="text-3xl font-bold uppercase tracking-tight">
            {title}
          </h1>
          {subtitle && <p className="text-sm font-bold mt-2">{subtitle}</p>}
          <p className="text-sm font-bold mt-1">HealthWatch Insurance Agency</p>
          <p className="text-xs">P.O. Box 12345-00100, Nairobi, Kenya</p>
          <p className="text-xs">Tel: +254 700 000 000 | Email: info@healthwatch.co.ke</p>
        </div>
        <div className="text-right">
          <p className="font-mono text-xl font-bold">
            {documentNumber}
          </p>
          <p className="text-sm mt-1">
            Date: {date}
          </p>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="min-h-[600px]">
        {children}
      </div>

      {/* Universal Footer */}
      <div className="mt-12 pt-8 border-t text-center text-[10px] text-gray-400">
        <div className="mb-4">
          {footerExtra}
        </div>
        <p>
          This is a computer-generated document and is valid without a physical signature.
        </p>
        <p>HealthWatch Management System • Generated on {new Date().toLocaleString()}</p>
      </div>
    </div>
  )
}
