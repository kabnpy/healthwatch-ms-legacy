import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Download, Printer } from "lucide-react"
import { Suspense } from "react"
import { z } from "zod"

import { OpenAPI, RiskNotesService } from "@/client"
import { HTMLViewer } from "@/components/Common/HTMLViewer"
import PendingItems from "@/components/Pending/PendingItems"
import { Button } from "@/components/ui/button"

const searchSchema = z.object({
  mode: z
    .enum(["invoice", "certificate", "renewal"])
    .default("invoice")
    .optional(),
})

function getRiskNoteQueryOptions(id: string) {
  return {
    queryFn: () => RiskNotesService.readRiskNote({ id }),
    queryKey: ["risk-notes", id],
  }
}

export const Route = createFileRoute("/print/risk-notes/$id")({
  component: RiskNotePrint,
  validateSearch: (search) => searchSchema.parse(search),
})

function RiskNotePrintContent({ id }: { id: string }) {
  const { mode } = Route.useSearch()
  const navigate = Route.useNavigate()
  const { data: riskNote } = useSuspenseQuery(getRiskNoteQueryOptions(id))

  const currentMode = mode || "invoice"

  // Construct URLs based on mode
  const baseUrl = (OpenAPI.BASE || "").replace(/\/$/, "")
  let htmlUrl = ""
  let pdfUrl = ""
  let title = ""

  if (currentMode === "renewal") {
    htmlUrl = `${baseUrl}/api/v1/policies/${riskNote.policy_id}/renewal-invitation/html`
    pdfUrl = `${baseUrl}/api/v1/policies/${riskNote.policy_id}/renewal-invitation/pdf`
    title = "Renewal Invitation"
  } else {
    // Risk Note (Invoice mode in frontend = Risk Note in backend)
    htmlUrl = `${baseUrl}/api/v1/risk-notes/${id}/html`
    pdfUrl = `${baseUrl}/api/v1/risk-notes/${id}/pdf`
    title = "Risk Note"
  }

  const handleDownloadPDF = () => {
    const token = localStorage.getItem("access_token")
    // Use a hidden link to trigger download with auth
    fetch(pdfUrl, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.href = url
        a.download = `${title.replace(/\s+/g, "_")}_${id.substring(0, 8)}.pdf`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
      })
      .catch((err) => console.error("PDF Download Error:", err))
  }

  return (
    <div className="max-w-[850px] mx-auto bg-white shadow-lg print:shadow-none min-h-screen relative">
      <HTMLViewer
        apiUrl={htmlUrl}
        title={title}
        className="w-full min-h-screen"
      />

      <div className="fixed bottom-8 right-8 print:hidden flex flex-col gap-3">
        {/* Toggle Buttons */}
        <div className="flex bg-white rounded-lg shadow-xl overflow-hidden border p-1 gap-1">
          <Button
            variant={currentMode === "invoice" ? "secondary" : "ghost"}
            size="sm"
            className="font-bold uppercase text-[10px] tracking-widest"
            onClick={() => navigate({ search: { mode: "invoice" } })}
          >
            Risk Note
          </Button>
          <Button
            variant={currentMode === "renewal" ? "secondary" : "ghost"}
            size="sm"
            className="font-bold uppercase text-[10px] tracking-widest"
            onClick={() => navigate({ search: { mode: "renewal" } })}
          >
            Renewal
          </Button>
        </div>

        <div className="flex flex-col gap-2">
          <Button
            onClick={handleDownloadPDF}
            variant="outline"
            size="lg"
            className="shadow-xl rounded-full gap-2 bg-white"
          >
            <Download className="size-5" />
            PDF
          </Button>

          <Button
            onClick={() => window.print()}
            size="lg"
            className="shadow-xl rounded-full gap-2"
          >
            <Printer className="size-5" />
            Print
          </Button>
        </div>
      </div>
    </div>
  )
}

function RiskNotePrint() {
  const { id } = Route.useParams()

  return (
    <div className="bg-gray-100 min-h-screen print:bg-white pb-20">
      <Suspense fallback={<PendingItems />}>
        <RiskNotePrintContent id={id} />
      </Suspense>
    </div>
  )
}
