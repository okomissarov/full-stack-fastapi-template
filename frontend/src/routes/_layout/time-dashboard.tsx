import { createFileRoute } from "@tanstack/react-router"

import TimeDashboard from "@/components/TimeDashboard/TimeDashboard"

export const Route = createFileRoute("/_layout/time-dashboard")({
  component: TimeDashboard,
  head: () => ({
    meta: [
      {
        title: "Time Dashboard - FastAPI Template",
      },
    ],
  }),
})
