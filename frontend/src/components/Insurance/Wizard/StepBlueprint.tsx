import { useMemo } from "react"
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
import { Input } from "@/components/ui/input"
import { useProducts } from "@/hooks/useInsurance"
import { extractWizardFields } from "@/utils/documentData"
import { ArrowLeft } from "lucide-react"

interface StepBlueprintProps {
  productId: string
  defaultValues: any
  onNext: (data: any) => void
  onBack: () => void
}

export function StepBlueprint({ productId, defaultValues, onNext, onBack }: StepBlueprintProps) {
  const { data: productsData } = useProducts()
  
  const selectedProduct = useMemo(() => {
    return productsData?.data.find((p) => p.id === productId)
  }, [productId, productsData])

  const wizardFields = useMemo(() => {
    if (!selectedProduct) return []
    return extractWizardFields(selectedProduct.product_details)
  }, [selectedProduct])

  const form = useForm({
    defaultValues: defaultValues || {},
  })

  if (!selectedProduct) return null

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onNext)} className="space-y-6">
        <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 mb-6">
            <p className="text-sm text-slate-700 font-medium">{selectedProduct.name}</p>
            <p className="text-xs text-slate-500 mt-1">Please provide the necessary details below.</p>
        </div>

        {wizardFields.length === 0 ? (
            <div className="py-10 text-center border-2 border-dashed rounded-lg">
                <p className="text-muted-foreground italic">This product requires no additional inputs. Click next to continue.</p>
            </div>
        ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {wizardFields.map((field) => (
                    <FormField
                        key={field.label}
                        control={form.control}
                        name={field.label} // For now, mapping inputs to labels for simplicity
                        render={({ field: inputField }) => (
                            <FormItem>
                                <FormLabel>{field.label}</FormLabel>
                                <FormControl>
                                    <Input 
                                        type={field.type === 'number' ? 'number' : 'text'} 
                                        placeholder={`Enter ${field.label.toLowerCase()}...`}
                                        {...inputField} 
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                ))}
            </div>
        )}

        <div className="flex justify-between pt-8">
          <Button type="button" variant="outline" onClick={onBack}>
            <ArrowLeft className="h-4 w-4 mr-2" /> Back
          </Button>
          <Button type="submit" size="lg" className="px-10">
            Next: Financials
          </Button>
        </div>
      </form>
    </Form>
  )
}
