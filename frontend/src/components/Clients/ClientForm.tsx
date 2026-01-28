import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import type { ClientCreate, ClientPublic, ClientUpdate } from "@/client"
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
import { LoadingButton } from "@/components/ui/loading-button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const formSchema = z.object({
  client_type: z.enum(["Individual", "Corporate"]),
  name: z.string().min(1, "Name is required"),
  kra_pin: z.string().min(11, "KRA PIN must be 11 characters").max(11),
  email: z.string().email("Invalid email").or(z.literal("")),
  phone: z.string().min(10, "Phone number is required"),
  postal_address: z.string().optional(),
  contact_person: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

interface ClientFormProps {
  initialData?: ClientPublic
  onSubmit: (data: ClientCreate | ClientUpdate) => void
  onCancel?: () => void
  isLoading?: boolean
  submitLabel?: string
}

export const ClientForm = ({
  initialData,
  onSubmit,
  onCancel,
  isLoading,
  submitLabel = "Save Client",
}: ClientFormProps) => {
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema) as any,
    defaultValues: {
      client_type: (initialData?.client_type as any) || "Individual",
      name: initialData?.name || "",
      kra_pin: initialData?.kra_pin || "",
      email: initialData?.email || "",
      phone: initialData?.phone || "",
      postal_address: initialData?.postal_address || "",
      contact_person: initialData?.contact_person || "",
    },
  })

  const handleFormSubmit = (data: FormData) => {
    const formattedData = {
      ...data,
      email: data.email === "" ? null : data.email,
      postal_address: data.postal_address || null,
      contact_person: data.contact_person || null,
    }
    onSubmit(formattedData as any)
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(handleFormSubmit)}
        className="space-y-4"
      >
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="client_type"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Client Type</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  defaultValue={field.value}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="Individual">Individual</SelectItem>
                    <SelectItem value="Corporate">Corporate</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="kra_pin"
            render={({ field }) => (
              <FormItem>
                <FormLabel>KRA PIN</FormLabel>
                <FormControl>
                  <Input placeholder="A00..." {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Client Name</FormLabel>
              <FormControl>
                <Input placeholder="Full Name or Company Name" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input
                    type="email"
                    placeholder="client@example.com"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="phone"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Phone Number</FormLabel>
                <FormControl>
                  <Input placeholder="07..." {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="postal_address"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Postal Address</FormLabel>
              <FormControl>
                <Input placeholder="P.O. Box 1234, Nairobi" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {form.watch("client_type") === "Corporate" && (
          <FormField
            control={form.control}
            name="contact_person"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Contact Person</FormLabel>
                <FormControl>
                  <Input placeholder="Name of contact person" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

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
    </Form>
  )
}
