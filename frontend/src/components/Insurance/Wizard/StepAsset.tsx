import { zodResolver } from "@hookform/resolvers/zod"
import { useMemo } from "react"
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

const assetSchema = z.object({
  product_id: z.string().min(1, "Product is required"),
  asset: z.object({
    identifier: z.string().min(1, "Identifier is required").toUpperCase(),
    description: z.string().min(1, "Description is required"),
    details: z
      .object({
        chassis: z.string().optional().default(""),
        engine: z.string().optional().default(""),
        note: z.string().optional().default(""),
      })
      .default({ chassis: "", engine: "", note: "" }),
  }),
})

interface StepAssetProps {
  defaultValues: any
  onNext: (data: any) => void
}

export function StepAsset({ defaultValues, onNext }: StepAssetProps) {
  const { data: productsData } = useProducts()

  const form = useForm({
    resolver: zodResolver(assetSchema),
    defaultValues: {
      product_id: defaultValues?.product_id || "",
      asset: {
        identifier: defaultValues?.asset?.identifier || "",
        description:
          defaultValues?.asset?.description ||
          defaultValues?.asset?.makeModel ||
          "",
        details: {
          chassis: defaultValues?.asset?.details?.chassis || "",
          engine: defaultValues?.asset?.details?.engine || "",
          note: defaultValues?.asset?.details?.note || "",
        },
      },
    },
  })

  const selectedProductId = form.watch("product_id")

  const selectedProduct = useMemo(() => {
    return productsData?.data.find((p) => p.id === selectedProductId)
  }, [selectedProductId, productsData])

  const isMotor = selectedProduct?.class_of_insurance
    .toLowerCase()
    .includes("motor")

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

        <div className="grid grid-cols-2 gap-4 border-t pt-6">
          <FormField
            control={form.control}
            name="asset.identifier"
            render={({ field }) => (
              <FormItem>
                <FormLabel>
                  {isMotor
                    ? "Registration Number"
                    : "Identifier (Serial/Plot No)"}
                </FormLabel>
                <FormControl>
                  <Input
                    placeholder={isMotor ? "KCA 123B" : "Asset ID"}
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="asset.description"
            render={({ field }) => (
              <FormItem>
                <FormLabel>
                  {isMotor ? "Make & Model" : "Asset Description"}
                </FormLabel>
                <FormControl>
                  <Input
                    placeholder={
                      isMotor ? "Toyota Harrier" : "Brief description"
                    }
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        {isMotor && (
          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="asset.details.chassis"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Chassis Number</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="JMZ..."
                      {...field}
                      value={(field.value as string) || ""}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="asset.details.engine"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Engine Number</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="2AZ..."
                      {...field}
                      value={(field.value as string) || ""}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        )}

        {!isMotor && selectedProductId && (
          <div className="p-4 bg-muted/20 border rounded-md">
            <p className="text-sm text-muted-foreground italic">
              Additional details for {selectedProduct?.class_of_insurance} can
              be added here.
            </p>
            <FormField
              control={form.control}
              name="asset.details.note"
              render={({ field }) => (
                <FormItem className="mt-2">
                  <FormLabel>Additional Notes</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Specify location, serial numbers etc"
                      {...field}
                      value={(field.value as string) || ""}
                    />
                  </FormControl>
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
