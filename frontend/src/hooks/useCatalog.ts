import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  type InsurerCreate,
  InsurersService,
  type InsurerUpdate,
  type ProductCreate,
  ProductsService,
  type ProductUpdate,
} from "../client"

// 1. INSURERS
export const useInsurers = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["insurers", { skip, limit }],
    queryFn: () => InsurersService.readInsurers({ skip, limit }),
  })
}

export const useInsurer = (id: string) => {
  return useQuery({
    queryKey: ["insurers", id],
    queryFn: () => InsurersService.readInsurer({ id }),
    enabled: !!id,
  })
}

export const useCreateInsurer = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: InsurerCreate) =>
      InsurersService.createInsurer({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["insurers"] })
    },
  })
}

export const useUpdateInsurer = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: InsurerUpdate }) =>
      InsurersService.updateInsurer({ id, requestBody: data }),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ["insurers"] })
      queryClient.invalidateQueries({ queryKey: ["insurers", id] })
    },
  })
}

export const useDeleteInsurer = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => InsurersService.deleteInsurer({ id }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["insurers"] })
    },
  })
}

// 2. PRODUCTS
export const useProducts = (insurerId?: string, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ["products", { insurerId, skip, limit }],
    queryFn: () => ProductsService.readProducts({ insurerId, skip, limit }),
  })
}

export const useProduct = (id: string) => {
  return useQuery({
    queryKey: ["products", id],
    queryFn: () => ProductsService.readProduct({ id }),
    enabled: !!id,
  })
}

export const useCreateProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: ProductCreate) =>
      ProductsService.createProduct({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] })
    },
  })
}

export const useUpdateProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ProductUpdate }) =>
      ProductsService.updateProduct({ id, requestBody: data }),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ["products"] })
      queryClient.invalidateQueries({ queryKey: ["products", id] })
    },
  })
}

export const useDeleteProduct = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => ProductsService.deleteProduct({ id }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] })
    },
  })
}
