import { createFileRoute, redirect } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/catalog/")({
  loader: () => {
    throw redirect({
      to: "/catalog/insurers",
    })
  },
})
