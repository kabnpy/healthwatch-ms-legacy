import { useNavigate } from "@tanstack/react-router"
import {
  CreditCard,
  Library,
  Receipt as ReceiptIcon,
  Search,
  Settings,
  Shield,
  User,
  Users,
} from "lucide-react"
import * as React from "react"

import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command"
import { useInvoices, useReceipts } from "@/hooks/useFinancials"
import { useClients, usePolicies } from "@/hooks/useInsurance"
import { getPolicyDisplayName } from "@/utils/insurance"

export function CommandMenu() {
  const [open, setOpen] = React.useState(false)
  const navigate = useNavigate()

  const { data: clientsData } = useClients(0, 50)
  const { data: policiesData } = usePolicies(undefined, 0, 50)
  const { data: invoicesData } = useInvoices(undefined, 0, 50)
  const { data: receiptsData } = useReceipts(undefined, 0, 50)

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }

    document.addEventListener("keydown", down)
    return () => document.removeEventListener("keydown", down)
  }, [])

  const runCommand = React.useCallback((command: () => void) => {
    setOpen(false)
    command()
  }, [])

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="relative inline-flex items-center justify-start whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2 w-full max-w-sm"
      >
        <Search className="mr-2 h-4 w-4 shrink-0 opacity-50" />
        <span className="text-muted-foreground">
          Search clients, policies...
        </span>
        <kbd className="pointer-events-none absolute right-1.5 top-1.5 hidden h-6 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium opacity-100 sm:flex">
          <span className="text-xs">⌘</span>K
        </kbd>
      </button>
      <CommandDialog open={open} onOpenChange={setOpen}>
        <CommandInput placeholder="Type a command or search..." />
        <CommandList>
          <CommandEmpty>No results found.</CommandEmpty>

          <CommandGroup heading="Clients">
            {clientsData?.data.map((client) => (
              <CommandItem
                key={client.id}
                value={client.name}
                onSelect={() => {
                  runCommand(() =>
                    navigate({
                      to: "/clients/$clientId/overview",
                      params: { clientId: client.id },
                    }),
                  )
                }}
              >
                <User className="mr-2 h-4 w-4" />
                <span>{client.name}</span>
                <CommandShortcut>{client.kra_pin}</CommandShortcut>
              </CommandItem>
            ))}
          </CommandGroup>

          <CommandSeparator />

          <CommandGroup heading="Policies">
            {policiesData?.data.map((policy) => {
              const displayName = getPolicyDisplayName(policy)
              return (
                <CommandItem
                  key={policy.id}
                  value={`${policy.policy_number} ${displayName}`}
                  onSelect={() => {
                    runCommand(() =>
                      navigate({
                        to: "/clients/$clientId/policies/$policyId",
                        params: {
                          clientId: policy.client_id,
                          policyId: policy.id,
                        },
                      }),
                    )
                  }}
                >
                  <Shield className="mr-2 h-4 w-4" />
                  <div className="flex flex-col">
                    <span>{displayName}</span>
                    <span className="text-[10px] text-muted-foreground">
                      {policy.policy_number}
                    </span>
                  </div>
                  <CommandShortcut>{policy.status}</CommandShortcut>
                </CommandItem>
              )
            })}
          </CommandGroup>

          <CommandSeparator />

          <CommandGroup heading="Invoices">
            {invoicesData?.data.map((invoice) => (
              <CommandItem
                key={invoice.id}
                value={invoice.invoice_number}
                onSelect={() => {
                  runCommand(() =>
                    navigate({
                      to: "/clients/$clientId/invoices",
                      params: { clientId: invoice.client_id },
                    }),
                  )
                }}
              >
                <ReceiptIcon className="mr-2 h-4 w-4" />
                <span>{invoice.invoice_number}</span>
                <CommandShortcut>
                  KES {(invoice.total_amount || 0).toLocaleString()}
                </CommandShortcut>
              </CommandItem>
            ))}
          </CommandGroup>

          <CommandSeparator />

          <CommandGroup heading="Receipts">
            {receiptsData?.data.map((receipt) => (
              <CommandItem
                key={receipt.id}
                value={receipt.receipt_number}
                onSelect={() => {
                  runCommand(() =>
                    navigate({
                      to: "/clients/$clientId/invoices",
                      params: { clientId: receipt.client_id },
                    }),
                  )
                }}
              >
                <CreditCard className="mr-2 h-4 w-4" />
                <span>{receipt.receipt_number}</span>
                <CommandShortcut>{receipt.mode}</CommandShortcut>
              </CommandItem>
            ))}
          </CommandGroup>

          <CommandSeparator />

          <CommandGroup heading="Quick Links">
            <CommandItem
              onSelect={() => runCommand(() => navigate({ to: "/clients" }))}
            >
              <Users className="mr-2 h-4 w-4" />
              <span>Browse All Clients</span>
            </CommandItem>
            <CommandItem
              onSelect={() =>
                runCommand(() => navigate({ to: "/catalog/products" }))
              }
            >
              <Shield className="mr-2 h-4 w-4" />
              <span>Product Catalog</span>
            </CommandItem>
            <CommandItem
              onSelect={() =>
                runCommand(() => navigate({ to: "/catalog/insurers" }))
              }
            >
              <Library className="mr-2 h-4 w-4" />
              <span>Insurance Carriers</span>
            </CommandItem>
            <CommandItem
              onSelect={() => runCommand(() => navigate({ to: "/settings" }))}
            >
              <Settings className="mr-2 h-4 w-4" />
              <span>System Settings</span>
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </>
  )
}
