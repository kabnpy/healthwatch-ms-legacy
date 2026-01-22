import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const assetSchema = z.object({
  identifier: z.string().min(1, "Registration is required").toUpperCase(),
  makeModel: z.string().min(1, "Make & Model is required"),
  details: z.object({
    chassis: z.string().optional(),
    engine: z.string().optional(),
  }),
})

interface StepAssetProps {
  defaultValues: any
  onNext: (data: any) => void
}

export function StepAsset({ defaultValues, onNext }: StepAssetProps) {
  const form = useForm({
    resolver: zodResolver(assetSchema),
    defaultValues,
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onNext)} className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="identifier"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Registration Number</FormLabel>
                <FormControl>
                  <Input placeholder="KCA 123B" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="makeModel"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Make & Model</FormLabel>
                <FormControl>
                  <Input placeholder="Toyota Harrier" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="details.chassis"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Chassis Number</FormLabel>
                <FormControl>
                  <Input placeholder="JMZ..." {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="details.engine"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Engine Number</FormLabel>
                <FormControl>
                  <Input placeholder="2AZ..." {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="flex justify-end pt-4">
          <Button type="submit">Next: Coverage & Financials</Button>
        </div>
      </form>
    </Form>
  )
}
