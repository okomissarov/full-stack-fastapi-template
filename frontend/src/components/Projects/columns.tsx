import type { ColumnDef } from "@tanstack/react-table"

import type { ProjectPublic } from "@/client"
import { cn } from "@/lib/utils"
import { ProjectActionsMenu } from "./ProjectActionsMenu"

export const columns: ColumnDef<ProjectPublic>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => (
      <span className="font-medium">{row.original.name}</span>
    ),
  },
  {
    accessorKey: "description",
    header: "Description",
    cell: ({ row }) => {
      const description = row.original.description
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !description && "italic",
          )}
        >
          {description || "No description"}
        </span>
      )
    },
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => (
      <span className="capitalize">{row.original.status ?? "active"}</span>
    ),
  },
  {
    accessorKey: "created_at",
    header: "Created",
    cell: ({ row }) => {
      const date = row.original.created_at
      return (
        <span className="text-muted-foreground">
          {date ? new Date(date).toLocaleDateString() : "—"}
        </span>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <ProjectActionsMenu project={row.original} />
      </div>
    ),
  },
]
