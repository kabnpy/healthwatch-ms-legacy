import { ArrowLeft } from "lucide-react"
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
import { Textarea } from "@/components/ui/textarea"

interface StepTermsProps {
  defaultValues: {
    benefits_and_limits: string
    excesses: string
    special_clauses: string
  }
  onNext: (data: any) => void
  onBack: () => void
}

export function StepTerms({ defaultValues, onNext, onBack }: StepTermsProps) {
  const form = useForm({
    defaultValues: {
      terms: defaultValues,
    },
  })

  return (
    <Form {...(form as any)}>
      <form onSubmit={form.handleSubmit(onNext)} className="space-y-6">
        <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 mb-6">
          <p className="text-sm text-slate-700 font-medium">Document Terms</p>
          <p className="text-xs text-slate-500 mt-1">
            Review and customize the text that will appear on the final Risk Note.
          </p>
        </div>

        <div className="space-y-6">
          <FormField
            control={form.control as any}
            name="terms.benefits_and_limits"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Benefits & Limits</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Enter benefits..."
                    className="min-h-[100px] font-mono text-xs"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control as any}
            name="terms.excesses"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Excesses</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Enter excesses..."
                    className="min-h-[100px] font-mono text-xs"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control as any}
            name="terms.special_clauses"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Special Clauses</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Enter special clauses..."
                    className="min-h-[100px] font-mono text-xs"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

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
