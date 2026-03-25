import { useQuery } from "@tanstack/react-query"
import { useState } from "react"

import { TimeEntriesService } from "@/client"
import type { TimeEntrySummary } from "@/client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

type DateRange = "week" | "month" | "all"

function getDateRange(range: DateRange): {
  startDate?: string
  endDate?: string
} {
  const now = new Date()
  if (range === "all") return {}
  const end = now.toISOString()
  if (range === "week") {
    const start = new Date(now)
    start.setDate(now.getDate() - now.getDay())
    start.setHours(0, 0, 0, 0)
    return { startDate: start.toISOString(), endDate: end }
  }
  // month
  const start = new Date(now.getFullYear(), now.getMonth(), 1)
  return { startDate: start.toISOString(), endDate: end }
}

function SummaryCardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-4 w-24" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-8 w-16" />
      </CardContent>
    </Card>
  )
}

function TableSkeleton() {
  return (
    <div className="space-y-2">
      {Array.from({ length: 3 }).map((_, i) => (
        <Skeleton key={i} className="h-10 w-full" />
      ))}
    </div>
  )
}

export default function TimeDashboard() {
  const [range, setRange] = useState<DateRange>("week")
  const { startDate, endDate } = getDateRange(range)

  const { data, isLoading } = useQuery({
    queryKey: ["time-entries-summary", range],
    queryFn: () =>
      TimeEntriesService.readTimeEntriesSummary({ startDate, endDate }),
  })

  const summary: TimeEntrySummary[] = data ?? []
  const totalHours = summary.reduce((sum, s) => sum + s.total_hours, 0)
  const activeProjects = summary.filter((s) => s.total_hours > 0).length

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Time Dashboard</h1>
          <p className="text-muted-foreground">
            Track your time across projects
          </p>
        </div>
        <Select
          value={range}
          onValueChange={(v) => setRange(v as DateRange)}
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="week">This Week</SelectItem>
            <SelectItem value="month">This Month</SelectItem>
            <SelectItem value="all">All Time</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {isLoading ? (
          <>
            <SummaryCardSkeleton />
            <SummaryCardSkeleton />
            <SummaryCardSkeleton />
          </>
        ) : (
          <>
            <Card>
              <CardHeader>
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Total Hours ({range === "week" ? "This Week" : range === "month" ? "This Month" : "All Time"})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold">{totalHours.toFixed(1)}</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Active Projects
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold">{activeProjects}</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Avg Hours / Project
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold">
                  {activeProjects > 0
                    ? (totalHours / activeProjects).toFixed(1)
                    : "0.0"}
                </p>
              </CardContent>
            </Card>
          </>
        )}
      </div>

      {/* Hours by Project Table */}
      <div>
        <h2 className="mb-4 text-lg font-semibold">Hours by Project</h2>
        {isLoading ? (
          <TableSkeleton />
        ) : summary.length === 0 ? (
          <p className="text-muted-foreground py-8 text-center">
            No time entries found for this period.
          </p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Project</TableHead>
                <TableHead className="text-right">Hours</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {summary.map((s) => (
                <TableRow key={s.project_id}>
                  <TableCell>{s.project_name}</TableCell>
                  <TableCell className="text-right">
                    {s.total_hours.toFixed(1)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  )
}
