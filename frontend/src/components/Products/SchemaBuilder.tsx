import { 
  Plus, 
  Trash2, 
  GripVertical, 
  Settings2, 
  ShieldCheck, 
  Type, 
  Hash, 
  Calendar, 
  ToggleLeft, 
  FileText, 
  Layers,
  ChevronDown,
  ChevronUp,
  Layout
} from "lucide-react"
import { useFieldArray, useFormContext } from "react-hook-form"
import { useState, useMemo } from "react"
import { Button } from "@/components/ui/button"
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
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
import { Separator } from "@/components/ui/separator"
import { cn } from "@/lib/utils"
import { slugify } from "@/utils"

// --- Constants ---

const FIELD_BEHAVIORS = [
  { value: "input-text", label: "Client Input (Text)", icon: Type, color: "text-blue-500" },
  { value: "input-number", label: "Client Input (Number)", icon: Hash, color: "text-orange-500" },
  { value: "input-date", label: "Client Input (Date)", icon: Calendar, color: "text-purple-500" },
  { value: "input-boolean", label: "Client Input (Yes/No Toggle)", icon: ToggleLeft, color: "text-green-500" },
  { value: "static", label: "Fixed Benefit / Text", icon: ShieldCheck, color: "text-emerald-600" },
]

// --- Components ---

export const SchemaBuilder = () => {
  const { control, watch, setValue } = useFormContext()
  const { fields, append, remove, move } = useFieldArray({
    control,
    name: "product_details",
  })
  
  const [expandedFields, setExpandedFields] = useState<Record<string, boolean>>({})
  const [showTechnical, setShowTechnical] = useState(false)

  // Group fields by section
  const productDetails = watch("product_details") || []
  const sections = useMemo(() => {
    const map: Record<string, number[]> = {}
    productDetails.forEach((field: any, index: number) => {
      const section = field.section || "GENERAL"
      if (!map[section]) map[section] = []
      map[section].push(index)
    })
    return map
  }, [productDetails])

  const addFieldToSection = (sectionName: string) => {
    append({
      key: `field_${Date.now()}`,
      label: "New Policy Field",
      section: sectionName,
      field_type: "input",
      input_type: "text",
      required: false,
      show_in_risknote: true,
    })
  }

  const addSection = () => {
    const name = window.prompt("Enter section name (e.g. BENEFITS, EXCESS, VEHICLE DETAILS)")
    if (name) addFieldToSection(name.toUpperCase())
  }

  const handleLabelChange = (index: number, value: string) => {
    setValue(`product_details.${index}.label`, value)
    const currentKey = watch(`product_details.${index}.key`)
    if (!currentKey || currentKey.startsWith("field_") || currentKey === slugify(watch(`product_details.${index}.label`) || "")) {
        setValue(`product_details.${index}.key`, slugify(value))
    }
  }

  const getBehaviorValue = (index: number) => {
    const fType = watch(`product_details.${index}.field_type`)
    const iType = watch(`product_details.${index}.input_type`)
    if (fType === "static") return "static"
    return `input-${iType || 'text'}`
  }

  const setBehaviorValue = (index: number, behavior: string) => {
    if (behavior === "static") {
        setValue(`product_details.${index}.field_type`, "static")
    } else {
        const iType = behavior.replace("input-", "")
        setValue(`product_details.${index}.field_type`, "input")
        setValue(`product_details.${index}.input_type`, iType)
    }
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto pb-40">
      {/* TOOLBAR */}
      <div className="flex items-center justify-between sticky top-20 z-20 bg-background/95 backdrop-blur-sm p-4 border rounded-xl shadow-sm">
        <div className="flex items-center gap-4">
            <Button type="button" variant="outline" size="sm" onClick={addSection} className="gap-2 font-bold uppercase text-[10px] tracking-widest">
                <Plus className="h-3 w-3" /> New Section
            </Button>
            <Separator orientation="vertical" className="h-6" />
            <div className="flex items-center gap-2">
                <Switch checked={showTechnical} onCheckedChange={setShowTechnical} id="technical-mode" className="scale-75" />
                <label htmlFor="technical-mode" className="text-[10px] uppercase font-bold text-muted-foreground cursor-pointer">Technical Keys</label>
            </div>
        </div>
        <p className="text-[10px] uppercase font-black tracking-tighter text-muted-foreground/50">Risk Note Template Builder</p>
      </div>

      {/* THE "PAPER" */}
      <div className="bg-white shadow-2xl border border-slate-200 min-h-[800px] rounded-sm flex flex-col overflow-hidden">
        {/* Paper Header Placeholder */}
        <div className="p-8 border-b-2 border-black/5 bg-slate-50/30">
            <div className="h-4 w-32 bg-slate-200 rounded mb-2" />
            <div className="h-8 w-64 bg-slate-100 rounded" />
        </div>

        <div className="flex-1 p-0">
            {Object.entries(sections).map(([sectionName, fieldIndices]) => (
                <div key={sectionName} className="group/section">
                    {/* SECTION HEADER */}
                    <div className="bg-slate-100/80 border-y border-black px-4 py-1.5 flex items-center justify-between group-hover/section:bg-slate-200 transition-colors">
                        <h4 className="text-[10px] font-black uppercase tracking-[0.2em] text-black">{sectionName}</h4>
                        <div className="opacity-0 group-hover/section:opacity-100 transition-opacity flex gap-2">
                            <Button 
                                type="button" 
                                variant="ghost" 
                                size="sm" 
                                className="h-6 px-2 text-[9px] uppercase font-bold hover:bg-black/5"
                                onClick={() => addFieldToSection(sectionName)}
                            >
                                <Plus className="h-3 w-3 mr-1" /> Add Row
                            </Button>
                        </div>
                    </div>

                    {/* ROWS */}
                    <div className="divide-y divide-black/10 border-b border-black/10">
                        {fieldIndices.map((globalIndex) => {
                            const fieldId = fields[globalIndex]?.id
                            const isExpanded = expandedFields[fieldId]
                            const behavior = getBehaviorValue(globalIndex)
                            const selectedBehavior = FIELD_BEHAVIORS.find(b => b.value === behavior)
                            const fieldType = watch(`product_details.${globalIndex}.field_type`)

                            return (
                                <div key={fieldId} className="group/row relative">
                                    <div className={cn(
                                        "grid grid-cols-12 items-stretch min-h-[40px] hover:bg-slate-50 transition-colors",
                                        isExpanded && "bg-slate-50"
                                    )}>
                                        {/* Label Cell */}
                                        <div className="col-span-4 border-r border-black/10 p-2 px-4 flex items-center bg-slate-50/30">
                                            <Input 
                                                value={watch(`product_details.${globalIndex}.label`)}
                                                onChange={(e) => handleLabelChange(globalIndex, e.target.value)}
                                                className="h-7 border-transparent hover:border-black/10 focus:border-primary focus:bg-white bg-transparent text-[11px] font-bold uppercase tracking-tight p-1"
                                                placeholder="Enter Label..."
                                            />
                                        </div>

                                        {/* Value / Placeholder Cell */}
                                        <div className="col-span-6 p-2 px-4 flex items-center gap-3">
                                            {fieldType === "static" ? (
                                                <Input 
                                                    value={watch(`product_details.${globalIndex}.value`) || ""}
                                                    onChange={(e) => setValue(`product_details.${globalIndex}.value`, e.target.value)}
                                                    className="h-7 border-transparent hover:border-black/10 focus:border-primary focus:bg-white bg-transparent text-[11px] p-1 italic text-slate-700"
                                                    placeholder="Fixed benefit value (e.g. KES 1M)"
                                                />
                                            ) : (
                                                <div className="text-[10px] text-slate-400 font-mono italic flex-1 truncate">
                                                    [ User will enter {behavior.replace('input-', '')} data here ]
                                                </div>
                                            )}
                                        </div>

                                        {/* Actions Cell */}
                                        <div className="col-span-2 p-1 pr-2 flex items-center justify-end gap-1 opacity-0 group-hover/row:opacity-100 transition-opacity">
                                            <Select 
                                                value={behavior} 
                                                onValueChange={(val) => setBehaviorValue(globalIndex, val)}
                                            >
                                                <SelectTrigger className="h-7 w-7 p-0 border-none bg-transparent hover:bg-black/5 flex justify-center">
                                                    <Layout className="h-3.5 w-3.5 text-slate-400" />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    {FIELD_BEHAVIORS.map(b => (
                                                        <SelectItem key={b.value} value={b.value}>
                                                            <div className="flex items-center gap-2">
                                                                <b.icon className={cn("h-3 w-3", b.color)} />
                                                                <span className="text-xs">{b.label}</span>
                                                            </div>
                                                        </SelectItem>
                                                    ))}
                                                </SelectContent>
                                            </Select>
                                            
                                            <Button 
                                                type="button" 
                                                variant="ghost" 
                                                size="icon" 
                                                className={cn("h-7 w-7", isExpanded && "bg-slate-200")}
                                                onClick={() => setExpandedFields(prev => ({ ...prev, [fieldId]: !prev[fieldId] }))}
                                            >
                                                <Settings2 className="h-3.5 w-3.5" />
                                            </Button>
                                            <Button 
                                                type="button" 
                                                variant="ghost" 
                                                size="icon" 
                                                className="h-7 w-7 text-destructive/40 hover:text-destructive"
                                                onClick={() => remove(globalIndex)}
                                            >
                                                <Trash2 className="h-3.5 w-3.5" />
                                            </Button>
                                        </div>
                                    </div>

                                    {/* INLINE SETTINGS DRAWER */}
                                    {isExpanded && (
                                        <div className="bg-slate-100/50 p-4 border-y border-black/5 shadow-inner animate-in slide-in-from-top-2 duration-200">
                                            <div className="flex flex-wrap items-center gap-8">
                                                <div className="flex items-center gap-6">
                                                    <FormField
                                                        control={control}
                                                        name={`product_details.${globalIndex}.required`}
                                                        render={({ field }) => (
                                                            <FormItem className="flex items-center space-x-2 space-y-0">
                                                                <FormControl>
                                                                    <Switch checked={field.value} onCheckedChange={field.onChange} className="scale-75" />
                                                                </FormControl>
                                                                <FormLabel className="text-[10px] font-bold uppercase text-slate-500">Required Field</FormLabel>
                                                            </FormItem>
                                                        )}
                                                    />
                                                    <FormField
                                                        control={control}
                                                        name={`product_details.${globalIndex}.show_in_risknote`}
                                                        render={({ field }) => (
                                                            <FormItem className="flex items-center space-x-2 space-y-0">
                                                                <FormControl>
                                                                    <Switch checked={field.value} onCheckedChange={field.onChange} className="scale-75" />
                                                                </FormControl>
                                                                <FormLabel className="text-[10px] font-bold uppercase text-slate-500">Show on Risk Note</FormLabel>
                                                            </FormItem>
                                                        )}
                                                    />
                                                </div>

                                                {showTechnical && (
                                                    <div className="flex-1 flex gap-4 items-center border-l pl-6">
                                                        <div className="flex flex-col gap-1 flex-1">
                                                            <span className="text-[9px] font-black text-slate-400 uppercase">Database Key</span>
                                                            <Input 
                                                                {...control.register(`product_details.${globalIndex}.key`)}
                                                                className="h-7 font-mono text-[10px] bg-white"
                                                            />
                                                        </div>
                                                        <div className="flex flex-col gap-1 flex-1">
                                                            <span className="text-[9px] font-black text-slate-400 uppercase">Section Header</span>
                                                            <Input 
                                                                {...control.register(`product_details.${globalIndex}.section`)}
                                                                className="h-7 text-[10px] bg-white"
                                                            />
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </div>
            ))}

            {Object.keys(sections).length === 0 && (
                <div className="p-20 text-center flex flex-col items-center">
                    <div className="bg-slate-50 w-24 h-24 rounded-full flex items-center justify-center mb-6 border-2 border-dashed border-slate-200">
                        <FileText className="h-10 w-10 text-slate-300" />
                    </div>
                    <h4 className="text-xl font-bold text-slate-900 tracking-tight">Empty Template</h4>
                    <p className="text-slate-500 mt-2 max-w-xs mx-auto text-sm">
                        Design your policy document by adding sections and rows.
                    </p>
                    <Button type="button" variant="default" onClick={addSection} className="mt-8 px-8">
                        Create First Section
                    </Button>
                </div>
            )}
        </div>

        {/* Paper Footer Placeholder */}
        <div className="p-12 mt-auto border-t-4 border-black/5 opacity-30 grayscale">
            <div className="h-4 w-full bg-slate-100 rounded mb-2" />
            <div className="h-4 w-3/4 bg-slate-100 rounded" />
        </div>
      </div>
    </div>
  )
}
