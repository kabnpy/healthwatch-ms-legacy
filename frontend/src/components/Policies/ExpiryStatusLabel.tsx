import type React from "react"

interface ExpiryStatusLabelProps {
  days: number
}

export const ExpiryStatusLabel: React.FC<ExpiryStatusLabelProps> = ({
  days,
}) => {
  if (days < 0) {
    return (
      <span className="text-destructive font-bold">
        Policy
        <br />
        Expired
      </span>
    )
  }

  if (days === 0) {
    return (
      <span className="text-destructive font-bold">
        Expires
        <br />
        Today
      </span>
    )
  }

  return (
    <>
      Days until
      <br />
      Expiry
    </>
  )
}
