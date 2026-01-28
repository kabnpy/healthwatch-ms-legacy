import { createFileRoute, redirect } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/clients/$clientId/")({
  beforeLoad: ({ params }) => {
    throw redirect({
      to: "/clients/$clientId/overview",
      params: { clientId: params.clientId },
      replace: true,
    })
  },
})
