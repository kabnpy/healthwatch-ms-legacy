import * as React from "react"
import { Input } from "@/components/ui/input"

interface CurrencyInputProps extends React.ComponentProps<"input"> {
  value: number
  onValueChange: (value: number) => void
}

export const CurrencyInput = React.forwardRef<HTMLInputElement, CurrencyInputProps>(
  ({ value, onValueChange, ...props }, ref) => {
    const [displayValue, setDisplayValue] = React.useState("")

    // Format number to string with commas
    const format = (val: number) => {
      if (isNaN(val) || val === 0) return ""
      return new Intl.NumberFormat("en-KE").format(val)
    }

    // Initialize display value
    React.useEffect(() => {
      const formatted = format(value)
      if (formatted !== displayValue.replace(/,/g, "")) {
         setDisplayValue(formatted)
      }
    }, [value])

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const raw = e.target.value.replace(/,/g, "")
      if (raw === "" || !isNaN(Number(raw))) {
        const num = raw === "" ? 0 : Number(raw)
        setDisplayValue(e.target.value.replace(/[^\d]/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ","))
        onValueChange(num)
      }
    }

    return (
      <Input
        {...props}
        ref={ref}
        value={displayValue}
        onChange={handleChange}
        placeholder="0"
      />
    )
  }
)

CurrencyInput.displayName = "CurrencyInput"
