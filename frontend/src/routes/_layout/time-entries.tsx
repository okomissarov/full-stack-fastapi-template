import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { TimeEntriesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import AddTimeEntry from "@/components/TimeEntries/AddTimeEntry"
import { columns } from "@/components/TimeEntries/columns"
import PendingTimeEntries from "@/components/Pending/PendingTimeEntries"

function getTimeEntriesQueryOptions() {
  return {
    queryFn: () =>
      TimeEntriesService.readTimeEntries({ skip: 0, limit: 100 }),
    queryKey: ["time-entries"],
  }
}

export const Route = createFileRoute("/_layout/time-entries")({
  component: TimeEntries,
  head: () => ({
    meta: [
      {
        title: "Time Entries - FastAPI Template",
      },
    ],
  }),
})

function TimeEntriesTableContent() {
  const { data: timeEntries } = useSuspenseQuery(getTimeEntriesQueryOptions())

  if (timeEntries.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any time entries yet
        </h3>
        <p className="text-muted-foreground">
          Add a new time entry to get started
        </p>
      </div>
    )
  }

  return <DataTable columns={columns} data={timeEntries.data} />
}

function TimeEntriesTable() {
  return (
    <Suspense fallback={<PendingTimeEntries />}>
      <TimeEntriesTableContent />
    </Suspense>
  )
}

function TimeEntries() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Time Entries</h1>
          <p className="text-muted-foreground">
            Log and manage your time entries
          </p>
        </div>
        <AddTimeEntry />
      </div>
      <TimeEntriesTable />
    </div>
  )
}
