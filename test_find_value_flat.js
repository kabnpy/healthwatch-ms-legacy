const findValue = (obj) => {
  if (!obj || typeof obj !== "object") return 0
  for (const [k, v] of Object.entries(obj)) {
    if (/sum_insured|value|sum insured/i.test(k) && typeof v !== "object") {
      const cleanVal = typeof v === "string" ? v.replace(/[^0-9.]/g, "") : v
      return Number(cleanVal) || 0
    }
    if (typeof v === "object") {
      const found = findValue(v)
      if (found !== 0) return found
    }
  }
  return 0
}

const data = {
  "VEHICLE DETAILS.Value Kshs.": "5,000,000"
}

console.log("Result:", findValue(data))
