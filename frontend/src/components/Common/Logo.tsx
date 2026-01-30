import { Link } from "@tanstack/react-router"

import { useTheme } from "@/components/theme-provider"
import { cn } from "@/lib/utils"
import icon from "/assets/images/fastapi-icon.svg"
import iconLight from "/assets/images/fastapi-icon-light.svg"
import logo from "/assets/images/fastapi-logo.svg"
import logoLight from "/assets/images/fastapi-logo-light.svg"

interface LogoProps {
  variant?: "full" | "icon" | "responsive"
  className?: string
  asLink?: boolean
}

export function Logo({
  variant = "full",
  className,
  asLink = true,
}: LogoProps) {
  const { resolvedTheme } = useTheme()
  const isDark = resolvedTheme === "dark"

  // For Documents/Print, we use a specialized branding style
  if (variant === "full" && !asLink) {
    return (
      <div className={cn("flex items-center gap-2 font-sans", className)}>
        <div className="flex flex-col leading-none">
          <span className="text-xl font-black tracking-tighter uppercase">
            HealthWatch
          </span>
          <span className="text-[8px] font-bold tracking-[0.3em] uppercase text-muted-foreground ml-0.5">
            Insurance Agency
          </span>
        </div>
      </div>
    )
  }

  const fullLogo = isDark ? logoLight : logo
  const iconLogo = isDark ? iconLight : icon

  const content =
    variant === "responsive" ? (
      <>
        <img
          src={fullLogo}
          alt="FastAPI"
          className={cn(
            "h-6 w-auto group-data-[collapsible=icon]:hidden",
            className,
          )}
        />
        <img
          src={iconLogo}
          alt="FastAPI"
          className={cn(
            "size-5 hidden group-data-[collapsible=icon]:block",
            className,
          )}
        />
      </>
    ) : (
      <img
        src={variant === "full" ? fullLogo : iconLogo}
        alt="FastAPI"
        className={cn(variant === "full" ? "h-6 w-auto" : "size-5", className)}
      />
    )

  if (!asLink) {
    return content
  }

  return <Link to="/">{content}</Link>
}
