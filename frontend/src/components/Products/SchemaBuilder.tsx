import { Plus, Trash2, GripVertical, Settings2, ShieldCheck } from "lucide-react"
import { useFieldArray, useFormContext } from "react-hook-form"
import { Button } from "@/components/ui/button"
import {
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
import { Switch } from "@/components/ui/switch"
import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"

export const SchemaBuilder = () => {
  const { control } = useFormContext()
  const { fields, append, remove } = useFieldArray({
    control,
    name: "product_details",
  })

  const addField = () => {
    append({
      key: `field_${fields.length + 1}`,
      label: "New Field",
      section: "GENERAL",
      field_type: "input",
      input_type: "text",
      required: false,
      show_in_risknote: true,
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">Form Schema Builder</h3>
          <p className="text-sm text-muted-foreground">
            Define the fields and sections that appear in the policy wizard and Risk Note.
          </p>
        </div>
        <Button type="button" variant="outline" size="sm" onClick={addField} className="gap-2">
          <Plus className="h-4 w-4" />
          Add Field
        </Button>
      </div>

      <Separator />

      <div className="space-y-4">
        {fields.map((field, index) => (
          <Card key={field.id} className="relative group overflow-hidden border-l-4 border-l-primary/20 hover:border-l-primary transition-colors">
            <CardContent className="p-4">
              <div className="flex items-start gap-4">
                <div className="mt-2 text-muted-foreground/30 cursor-grab active:cursor-grabbing">
                  <GripVertical className="h-5 w-5" />
                </div>

                <div className="flex-1 grid gap-4">
                  {/* Row 1: Label and Key */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <FormField
                      control={control}
                      name={`product_details.${index}.label`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[10px] uppercase font-bold text-muted-foreground">Label</FormLabel>
                          <FormControl>
                            <Input placeholder="Field Label (e.g. Reg No)" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={control}
                      name={`product_details.${index}.key`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[10px] uppercase font-bold text-muted-foreground">Database Key</FormLabel>
                          <FormControl>
                            <Input placeholder="key_name" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>

                  {/* Row 2: Section and Type */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <FormField
                      control={control}
                      name={`product_details.${index}.section`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[10px] uppercase font-bold text-muted-foreground">Section</FormLabel>
                          <FormControl>
                            <Input placeholder="e.g. VEHICLE DETAILS" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={control}
                      name={`product_details.${index}.field_type`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[10px] uppercase font-bold text-muted-foreground">Logic Type</FormLabel>
                          <Select onValueChange={field.onChange} defaultValue={field.value}>
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              <SelectItem value="input">User Input</SelectItem>
                              <SelectItem value="static">Fixed Text (Static)</SelectItem>
                              <SelectItem value="optional">Optional / Add-on</SelectItem>
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={control}
                      name={`product_details.${index}.input_type`}
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[10px] uppercase font-bold text-muted-foreground">Input Style</FormLabel>
                          <Select onValueChange={field.onChange} defaultValue={field.value}>
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              <SelectItem value="text">Short Text</SelectItem>
                              <SelectItem value="number">Number</SelectItem>
                              <SelectItem value="date">Date Picker</SelectItem>
                              <SelectItem value="boolean">Yes/No Toggle</SelectItem>
                              <SelectItem value="select">Dropdown (Soon)</SelectItem>
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>

                  {/* Row 3: Flags */}
                  <div className="flex items-center gap-6 pt-2">
                    <FormField
                      control={control}
                      name={`product_details.${index}.required`}
                      render={({ field }) => (
                        <FormItem className="flex items-center space-x-2 space-y-0">
                          <FormControl>
                            <Switch checked={field.value} onCheckedChange={field.onChange} />
                          </FormControl>
                          <FormLabel className="text-xs font-medium">Required</FormLabel>
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={control}
                      name={`product_details.${index}.show_in_risknote`}
                      render={({ field }) => (
                        <FormItem className="flex items-center space-x-2 space-y-0">
                          <FormControl>
                            <Switch checked={field.value} onCheckedChange={field.onChange} />
                          </FormControl>
                          <FormLabel className="text-xs font-medium flex items-center gap-1">
                            <ShieldCheck className="h-3 w-3 text-primary" />
                            Show in Risk Note
                          </FormLabel>
                        </FormItem>
                      )}
                    />
                  </div>
                </div>

                <div className="flex flex-col gap-2">
                    <Button 
                        type="button" 
                        variant="ghost" 
                        size="icon" 
                        className="text-destructive opacity-0 group-hover:opacity-100 transition-opacity"
                        onClick={() => remove(index)}
                    >
                        <Trash2 className="h-4 w-4" />
                    </Button>
                    <Button 
                        type="button" 
                        variant="ghost" 
                        size="icon" 
                        className="opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                        <Settings2 className="h-4 w-4" />
                    </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}

        {fields.length === 0 && (
          <div className="border-2 border-dashed rounded-lg p-12 text-center">
            <Settings2 className="mx-auto h-12 w-12 text-muted-foreground/20 mb-4" />
            <h4 className="font-medium text-muted-foreground">No fields defined</h4>
            <p className="text-sm text-muted-foreground mb-4">Start by adding fields to build your product form.</p>
            <Button type="button" variant="outline" onClick={addField}>
              Add First Field
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
