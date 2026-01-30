import { zodResolver } from "@hookform/resolvers/zod"
import { useMemo, useEffect } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useProducts } from "@/hooks/useInsurance"

interface StepAssetProps {
  defaultValues: any
  onNext: (data: any) => void
}

export function StepAsset({ defaultValues, onNext }: StepAssetProps) {
  const { data: productsData } = useProducts()

  const form = useForm({
    defaultValues: {
      product_id: defaultValues?.product_id || "",
      asset: {
        description: defaultValues?.asset?.description || "",
        details: defaultValues?.asset?.details || {},
      },
    },
  })

  const selectedProductId = form.watch("product_id")

  const selectedProduct = useMemo(() => {
    return productsData?.data.find((p) => p.id === selectedProductId)
  }, [selectedProductId, productsData])

  const inputFields = useMemo(() => {
    return (selectedProduct?.product_details || []).filter(
      (f: any) => f.field_type === "input" || f.field_type === "optional"
    )
  }, [selectedProduct])

  // Helper to generate a summary description based on the fields
  useEffect(() => {
    const details = form.getValues("asset.details")
    if (selectedProduct && Object.keys(details).length > 0) {
      // Create a sensible description from the first 2-3 input fields
      const summaryParts = inputFields
        .slice(0, 2)
        .map(f => details[f.key])
        .filter(v => !!v)
      
      if (summaryParts.length > 0) {
        form.setValue("asset.description", summaryParts.join(" - "))
      }
    }
  }, [form.watch("asset.details"), selectedProduct, inputFields])

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onNext)} className="space-y-6">
        <FormField
          control={form.control}
          name="product_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Insurance Product</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a product" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {productsData?.data.map((product) => (
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

        {selectedProduct && (
          <div className="space-y-4 border-t pt-6">
            <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground">
              {selectedProduct.class_of_insurance} Details
            </h3>
            
            <div className="grid grid-cols-2 gap-4">
              {inputFields.map((field: any) => (
                <FormField
                  key={field.key}
                  control={form.control}
                  name={`asset.details.${field.key}`}
                  render={({ field: inputField }) => (
                    <FormItem>
                      <FormLabel>{field.label}</FormLabel>
                      <FormControl>
                        <Input
                          type={field.type === "number" ? "number" : "text"}
                          placeholder={field.description || `Enter ${field.label.toLowerCase()}`}
                          {...inputField}
                          value={inputField.value || ""}
                          onChange={(e) => 
                            inputField.onChange(field.type === "number" ? e.target.valueAsNumber : e.target.value)
                          }
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              ))}
            </div>

            <FormField
              control={form.control}
              name="asset.description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Summary Description</FormLabel>
                  <FormControl>
                    <Input placeholder="E.g. Toyota Harrier - KCA 123B" {...field} />
                  </FormControl>
                  <FormDescription className="text-[10px]">
                    This is how the asset will be displayed in lists.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        )}

        <div className="flex justify-end pt-4">
          <Button type="submit" disabled={!selectedProductId}>
            Next: Coverage & Financials
          </Button>
        </div>
      </form>
    </Form>
  )
}

function FormDescription({ children, className }: { children: React.ReactNode, className?: string }) {
  return <p className={`text-sm text-muted-foreground ${className}`}>{children}</p>
}