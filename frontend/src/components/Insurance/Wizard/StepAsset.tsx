import { useForm } from "react-hook-form"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useProducts } from "@/hooks/useInsurance"

interface StepAssetProps {
  defaultValues: { product_id: string }
  onNext: (data: { product_id: string }) => void
}

export function StepAsset({ defaultValues, onNext }: StepAssetProps) {
  const { data: productsData } = useProducts()

  const form = useForm({
    defaultValues: {
      product_id: defaultValues?.product_id || "",
    },
  })

  const selectedProductId = form.watch("product_id")

  return (
    <Form {...(form as any)}>
      <form onSubmit={form.handleSubmit(onNext)} className="space-y-6">
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-100 mb-6">
          <p className="text-sm text-blue-700 font-medium">
            Step 1: Select Insurance Product
          </p>
          <p className="text-xs text-blue-600 mt-1">
            Choose the baseline product for this policy.
          </p>
        </div>

        <FormField
          control={form.control}
          name="product_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Insurance Product</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger className="h-12 text-base">
                    <SelectValue placeholder="Search or select a product..." />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {productsData?.data
                    .filter((p) =>
                      p.class_of_insurance.toLowerCase().includes("motor private"),
                    )
                    .map((product) => (
                      <SelectItem key={product.id} value={product.id}>
                        {product.name} ({product.class_of_insurance})
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex justify-end pt-8">
          <Button
            type="submit"
            disabled={!selectedProductId}
            size="lg"
            className="px-10"
          >
            Next: Product Details
          </Button>
        </div>
      </form>
    </Form>
  )
}
