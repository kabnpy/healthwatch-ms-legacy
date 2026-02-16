import { Letterhead } from "./Letterhead"

interface BaseDocumentProps {
  children: React.ReactNode
}

export const BaseDocument = ({ children }: BaseDocumentProps) => {
  return (
    <div className="w-full h-full bg-white text-black p-16 font-sans relative shadow-sm border">
      {/* Universal Letterhead */}
      <Letterhead />

      {/* Main Content Area */}
      <div className="min-h-[700px]">{children}</div>

      {/* Universal Footer */}
      <div className="mt-16 pt-10 border-t border-slate-100 flex justify-between items-center text-[9px] text-gray-400 uppercase tracking-widest font-bold">
        <p>
          Computer generated &bull; Valid without signature
        </p>
        <p>
          HealthWatch MS &bull; {new Date().toLocaleDateString('en-GB')}
        </p>
      </div>
    </div>
  )
}
