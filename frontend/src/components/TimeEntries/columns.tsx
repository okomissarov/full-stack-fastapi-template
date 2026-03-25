import type { ColumnDef } from "@tanstack/react-table"
import { Check, X } from "lucide-react"

import type { TimeEntryPublic } from "@/client"
import { TimeEntryActionsMenu } from "./TimeEntryActionsMenu"

export const columns: ColumnDef<TimeEntryPublic>[] = [
  {
    accessorKey: "date",
    header: "Date",
    cell: ({ row }) => <span>{row.original.date}</span>,
  },
  {
    accessorKey: "project_id",
    header: "Project",
    cell: ({ row }) => (
      <span className="text-muted-foreground">{row.original.project_id}</span>
    ),
  },
  {
    accessorKey: "hours",
    header: "Hours",
    cell: ({ row }) => <span>{row.original.hours}</span>,
  },
  {
    accessorKey: "description",
    header: "Description",
    cell: ({ row }) => (
      <span className="max-w-xs truncate block text-muted-foreground">
        {row.original.description || "—"}
      </span>
    ),
  },
  {
    accessorKey: "billable",
    header: "Billable",
    cell: ({ row }) =>
      row.original.billable ? (
        <Check className="size-4 text-green-500" />
      ) : (
        <X className="size-4 text-muted-foreground" />
      ),
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <TimeEntryActionsMenu timeEntry={row.original} />
      </div>
    ),
  },
]
