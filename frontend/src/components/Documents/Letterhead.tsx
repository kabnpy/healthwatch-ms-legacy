export function Letterhead() {
  return (
    <div className="flex flex-col items-center text-center mb-8">
      {/* <Logo asLink={false} className="h-16 w-auto mb-4" /> */}
      <h1 className="font-bold text-xl uppercase tracking-widest mb-1">
        HealthWatch Insurance Agency
      </h1>
      <div className="text-sm font-sans space-y-1 text-slate-900 leading-tight">
        <p>1st Floor, Bishop Garden Towers, Bishop Road-1st Ngong Avenues</p>
        <p>P O Box 1966 - 00502, Nairobi | Mobile: 0746129521/ 0733980566</p>
        <p>Email: info@healthwatch.co.ke</p>
      </div>
    </div>
  )
}
