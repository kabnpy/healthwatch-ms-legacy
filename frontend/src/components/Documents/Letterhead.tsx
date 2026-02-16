export function Letterhead() {
  return (
    <div className="flex justify-between items-end mb-12 border-b-4 border-black pb-6">
      <div className="flex flex-col items-start">
        <h1 className="font-black text-3xl uppercase tracking-tighter mb-1 leading-none">
          HealthWatch
        </h1>
        <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-muted-foreground">
          Insurance Agency
        </p>
      </div>
      <div className="text-[10px] font-medium space-y-0.5 text-right text-slate-600 leading-tight uppercase tracking-wider">
        <p>1st Floor, Bishop Garden Towers, Nairobi</p>
        <p>P.O. Box 1966 - 00502 | +254 746 129 521</p>
        <p className="font-bold text-black">info@healthwatch.co.ke</p>
      </div>
    </div>
  )
}
