import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  type ClientCreate,
  ClientsService,
  PoliciesService,
  type PolicyCreate,
  ProductsService,
  type RiskNoteCreate,
  RiskNotesService,
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
    mutationFn: (data: PolicyCreate) =>
      PoliciesService.createPolicy({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["policies"] })
    },
  })
}

// 3. RISK NOTES
export const useRiskNotes = (policyId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["risk-notes", { policyId, skip, limit }],
    queryFn: () => RiskNotesService.readRiskNotes({ policyId, skip, limit }),
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

// 4. PRODUCTS
export const useProducts = (insurerId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["products", { insurerId, skip, limit }],
    queryFn: () => ProductsService.readProducts({ insurerId, skip, limit }),
  })
}

// 5. RISK ITEMS
export const useRiskItems = (policyId: string) => {
  return useQuery({
    queryKey: ["risk-items", policyId],
    queryFn: () => PoliciesService.readPolicyRiskItems({ id: policyId }),
    enabled: !!policyId,
  })
}

export const useCreateRiskItem = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ policyId, data }: { policyId: string; data: any }) =>
      PoliciesService.createPolicyRiskItem({ id: policyId, requestBody: data }),
    onSuccess: (_, { policyId }) => {
      queryClient.invalidateQueries({ queryKey: ["risk-items", policyId] })
    },
  })
}

// 6. DASHBOARD AGGREGATOR
export const usePolicyDashboard = (policyId: string) => {
  const policyQuery = usePolicy(policyId)
  const riskNotesQuery = useRiskNotes(policyId)
  const riskItemsQuery = useRiskItems(policyId)

  // Helper to find latest risk note (most recent start date)
  const latestRiskNote = riskNotesQuery.data?.data?.sort(
    (a, b) =>
      new Date(b.start_date).getTime() - new Date(a.start_date).getTime(),
  )[0]

  // Helper to find active risk item (assuming first one is active for MVP or filtered)
  // Real implementation might filter by 'is_active' or date range
  const activeItem = riskItemsQuery.data?.data?.[0]

  return {
    policy: policyQuery.data,
    latestRiskNote,
    activeItem,
    riskNotes: riskNotesQuery.data?.data || [],
    riskItems: riskItemsQuery.data?.data || [],
    isLoading:
      policyQuery.isLoading ||
      riskNotesQuery.isLoading ||
      riskItemsQuery.isLoading,
    error: policyQuery.error || riskNotesQuery.error || riskItemsQuery.error,
  }
}

// 7. CORRESPONDENCE / DOCUMENTS
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
