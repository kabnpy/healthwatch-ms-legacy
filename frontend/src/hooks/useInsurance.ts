import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  type ClientCreate,
  ClientsService,
  type ClientUpdate,
  FinancialsService,
  PoliciesService,
  type PolicyCreateExtended,
  type PolicyUpdate,
  ProductsService,
  type QuoteRequest,
  type RiskNoteCreate,
  RiskNotesService,
  type RiskNoteUpdate,
} from "../client"

// 1. CLIENTS
export const useClients = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["clients", { skip, limit }],
    queryFn: () => ClientsService.readClients({ skip, limit }),
  })
}

export const useClient = (id: string) => {
  return useQuery({
    queryKey: ["clients", id],
    queryFn: () => ClientsService.readClient({ id }),
    enabled: !!id,
  })
}

export const useCreateClient = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: ClientCreate) =>
      ClientsService.createClient({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clients"] })
    },
  })
}

export const useUpdateClient = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ClientUpdate }) =>
      ClientsService.updateClient({ id, requestBody: data }),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ["clients"] })
      queryClient.invalidateQueries({ queryKey: ["clients", id] })
    },
  })
}

export const useDeleteClient = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => ClientsService.deleteClient({ id }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clients"] })
    },
  })
}

// 2. POLICIES
export const usePolicies = (clientId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["policies", { clientId, skip, limit }],
    queryFn: () => PoliciesService.readPolicies({ clientId, skip, limit }),
  })
}

export const usePolicy = (id: string) => {
  return useQuery({
    queryKey: ["policies", id],
    queryFn: () => PoliciesService.readPolicy({ id }),
    enabled: !!id,
  })
}

export const useCreatePolicy = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: PolicyCreateExtended) =>
      PoliciesService.createPolicy({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["policies"] })
    },
  })
}

export const useUpdatePolicy = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: PolicyUpdate }) =>
      PoliciesService.updatePolicy({ id, requestBody: data }),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ["policies"] })
      queryClient.invalidateQueries({ queryKey: ["policies", id] })
    },
  })
}

// 3. RISK NOTES
export const useRiskNotes = (
  policyId?: string,
  skip = 0,
  limit = 100,
  clientId?: string,
  uninvoicedOnly?: boolean,
) => {
  return useQuery({
    queryKey: [
      "risk-notes",
      { policyId, skip, limit, clientId, uninvoicedOnly },
    ],
    queryFn: () =>
      RiskNotesService.readRiskNotes({
        policyId,
        skip,
        limit,
        clientId,
        uninvoicedOnly,
      }),
  })
}

export const useRiskNote = (id: string) => {
  return useQuery({
    queryKey: ["risk-notes", id],
    queryFn: () => RiskNotesService.readRiskNote({ id }),
    enabled: !!id,
  })
}

export const useCreateRiskNote = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: RiskNoteCreate) =>
      RiskNotesService.createRiskNote({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["risk-notes"] })
      queryClient.invalidateQueries({ queryKey: ["policies"] })
    },
  })
}

export const useUpdateRiskNote = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: RiskNoteUpdate }) =>
      RiskNotesService.updateRiskNote({ id, requestBody: data }),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ["risk-notes"] })
      queryClient.invalidateQueries({ queryKey: ["risk-notes", id] })
    },
  })
}

// 4. PRODUCTS
export const useProducts = (insurerId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["products", { insurerId, skip, limit }],
    queryFn: () => ProductsService.readProducts({ insurerId, skip, limit }),
  })
}

// 5. DASHBOARD AGGREGATOR
export const usePolicyDashboard = (policyId: string) => {
  const policyQuery = usePolicy(policyId)
  const riskNotesQuery = useRiskNotes(policyId)

  // The backend now provides the active_note directly in the policy response
  const policy = policyQuery.data
  const latestRiskNote = policy?.active_note || riskNotesQuery.data?.data?.[0]

  // Enhanced Policy for UI backwards compatibility where needed,
  // but pointing to the new atomic locations.
  const enhancedPolicy = policy
    ? {
        ...policy,
        // Legacy field mapping for existing components
        current_risk_details: latestRiskNote?.cover_snapshot || {},
        total_premium: latestRiskNote?.total_amount || 0,
        coverage_start: latestRiskNote?.coverage_start,
        coverage_end: latestRiskNote?.coverage_end,
      }
    : undefined

  return {
    policy: enhancedPolicy,
    latestRiskNote,
    riskNotes: riskNotesQuery.data?.data || [],
    isLoading: policyQuery.isLoading || riskNotesQuery.isLoading,
    error: policyQuery.error || riskNotesQuery.error,
  }
}

// 6. CORRESPONDENCE / DOCUMENTS
export const useCorrespondences = (clientId: string) => {
  return useQuery({
    queryKey: ["correspondences", clientId],
    queryFn: () => ClientsService.readClientCorrespondences({ id: clientId }),
    enabled: !!clientId,
  })
}

export const useCreateCorrespondence = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ clientId, data }: { clientId: string; data: any }) =>
      ClientsService.createClientCorrespondence({
        id: clientId,
        requestBody: data,
      }),
    onSuccess: (_, { clientId }) => {
      queryClient.invalidateQueries({ queryKey: ["correspondences", clientId] })
    },
  })
}

// 7. FINANCIALS (Invoices & Receipts)
export const useInvoices = (clientId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["invoices", { clientId, skip, limit }],
    queryFn: () => FinancialsService.readInvoices({ clientId, skip, limit }),
  })
}

export const useReceipts = (clientId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["receipts", { clientId, skip, limit }],
    queryFn: () => FinancialsService.readReceipts({ clientId, skip, limit }),
  })
}

// 8. RATING / QUOTES
export const useQuote = () => {
  return useMutation({
    mutationFn: async (data: QuoteRequest) =>
      await PoliciesService.getPolicyQuote({ requestBody: data }),
  })
}

export const useQuoteQuery = (data: QuoteRequest | null) => {
  return useQuery({
    queryKey: ["quote", data],
    queryFn: async () => {
      if (!data) return Promise.reject("No data")
      return await PoliciesService.getPolicyQuote({ requestBody: data })
    },
    enabled: !!data && !!data.product_id,
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}
