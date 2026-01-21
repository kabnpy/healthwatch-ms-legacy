import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { 
  ClientsService, 
  PoliciesService, 
  RiskNotesService,
  ProductsService,
  type RiskNoteCreate,
  type ClientCreate,
  type PolicyCreate
} from "../client";

// 1. CLIENTS
export const useClients = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["clients", { skip, limit }],
    queryFn: () => ClientsService.readClients({ skip, limit }),
  });
};

export const useClient = (id: string) => {
  return useQuery({
    queryKey: ["clients", id],
    queryFn: () => ClientsService.readClient({ id }),
    enabled: !!id,
  });
};

export const useCreateClient = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ClientCreate) => ClientsService.createClient({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clients"] });
    },
  });
};

// 2. POLICIES
export const usePolicies = (clientId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["policies", { clientId, skip, limit }],
    queryFn: () => PoliciesService.readPolicies({ clientId, skip, limit }),
  });
};

export const usePolicy = (id: string) => {
  return useQuery({
    queryKey: ["policies", id],
    queryFn: () => PoliciesService.readPolicy({ id }),
    enabled: !!id,
  });
};

export const useCreatePolicy = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PolicyCreate) => PoliciesService.createPolicy({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["policies"] });
    },
  });
};

// 3. RISK NOTES
export const useRiskNotes = (policyId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["risk-notes", { policyId, skip, limit }],
    queryFn: () => RiskNotesService.readRiskNotes({ policyId, skip, limit }),
  });
};

export const useCreateRiskNote = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: RiskNoteCreate) => RiskNotesService.createRiskNote({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["risk-notes"] });
      queryClient.invalidateQueries({ queryKey: ["policies"] });
    },
  });
};

// 4. PRODUCTS
export const useProducts = (insurerId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["products", { insurerId, skip, limit }],
    queryFn: () => ProductsService.readProducts({ insurerId, skip, limit }),
  });
};