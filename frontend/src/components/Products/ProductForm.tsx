import { zodResolver } from "@hookform/resolvers/zod"
import { useForm, useFormContext } from "react-hook-form"
import { z } from "zod"
import type { ProductCreate, ProductPublic, ProductUpdate } from "@/client"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { LoadingButton } from "@/components/ui/loading-button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useInsurers } from "@/hooks/useCatalog"

const formSchema = z.object({
  insurer_id: z.string().uuid("Please select an insurer"),
  name: z.string().min(1, "Product name is required"),
  class_of_insurance: z.string().min(1, "Class of insurance is required"),
  default_commission_rate: z.coerce.number().min(0).max(100),
  product_details: z.record(z.string(), z.any()).default({}),
})

type FormData = z.infer<typeof formSchema>

interface ProductFormProps {
  initialData?: ProductPublic
  onSubmit: (data: ProductCreate | ProductUpdate) => void
  onCancel?: () => void
  isLoading?: boolean
  submitLabel?: string
  fixedInsurerId?: string
  useContext?: boolean
}

export const ProductForm = ({
  initialData,
  onSubmit,
  onCancel,
  isLoading,
  submitLabel = "Save Product",
  fixedInsurerId,
  useContext = false,
}: ProductFormProps) => {
  const { data: insurersData } = useInsurers()
  const insurers = insurersData?.data || []

  // If useContext is true, we expect to be wrapped in a FormProvider
  const context = useFormContext<FormData>()
  
  const localForm = useForm<FormData>({
    resolver: zodResolver(formSchema) as any,
    defaultValues: {
      insurer_id: fixedInsurerId || initialData?.insurer_id || "",
      name: initialData?.name || "",
      class_of_insurance: initialData?.class_of_insurance || "",
      default_commission_rate: initialData?.default_commission_rate ?? 10.0,
      product_details: (initialData?.product_details as any) || {},
    },
  })

  const form = useContext && context ? context : (localForm as any)

  const handleFormSubmit = (data: FormData) => {
    onSubmit(data as any)
  }

  const content = (
    <form
      onSubmit={(form as any).handleSubmit(handleFormSubmit as any)}
      className="space-y-4"
    >
              {!fixedInsurerId && (
                <FormField
                  control={(form as any).control}
                  name="insurer_id"
                  render={({ field }) => (
      
            <FormItem>
              <FormLabel>Insurer</FormLabel>
              <Select
                onValueChange={field.onChange}
                defaultValue={field.value}
                disabled={!!initialData}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select insurance carrier" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {insurers.map((insurer) => (
                    <SelectItem key={insurer.id} value={insurer.id}>
                      {insurer.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
      )}

      <FormField
        control={(form as any).control}
        name="name"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Product Name</FormLabel>
            <FormControl>
              <Input placeholder="e.g. Motor Comprehensive - Gold" {...field} />
            </FormControl>
            <FormDescription>
              The public name of the insurance product.
            </FormDescription>
            <FormMessage />
          </FormItem>
        )}
      />

      <div className="grid grid-cols-2 gap-4">
        <FormField
          control={(form as any).control}
          name="class_of_insurance"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Class of Insurance</FormLabel>
              <Select
                onValueChange={field.onChange}
                defaultValue={field.value}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select class" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="Motor Private">Motor Private</SelectItem>
                  <SelectItem value="Motor Commercial">Motor Commercial</SelectItem>
                  <SelectItem value="Fire">Fire</SelectItem>
                  <SelectItem value="Domestic Package">Domestic Package</SelectItem>
                  <SelectItem value="Personal Accident">Personal Accident</SelectItem>
                  <SelectItem value="Marine">Marine</SelectItem>
                  <SelectItem value="Medical">Medical</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={(form as any).control}
          name="default_commission_rate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Default Commission %</FormLabel>
              <FormControl>
                <Input type="number" step="0.01" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>

      <div className="flex justify-end gap-4 pt-4">
        {onCancel && (
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <LoadingButton type="submit" loading={isLoading}>
          {submitLabel}
        </LoadingButton>
      </div>
    </form>
  )

  // Only wrap in <Form> if we are NOT using external context
  if (useContext && context) {
    return content
  }

  return <Form {...form}>{content}</Form>
}
