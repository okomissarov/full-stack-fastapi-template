import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { ProjectsService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import PendingProjects from "@/components/Pending/PendingProjects"
import AddProject from "@/components/Projects/AddProject"
import { columns } from "@/components/Projects/columns"

function getProjectsQueryOptions() {
  return {
    queryFn: () => ProjectsService.readProjects({ skip: 0, limit: 100 }),
    queryKey: ["projects"],
  }
}

export const Route = createFileRoute("/_layout/projects")({
  component: Projects,
  head: () => ({
    meta: [
      {
        title: "Projects - FastAPI Template",
      },
    ],
  }),
})

function ProjectsTableContent() {
  const { data: projects } = useSuspenseQuery(getProjectsQueryOptions())

  if (projects.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any projects yet
        </h3>
        <p className="text-muted-foreground">
          Add a new project to get started
        </p>
      </div>
    )
  }

  return <DataTable columns={columns} data={projects.data} />
}

function ProjectsTable() {
  return (
    <Suspense fallback={<PendingProjects />}>
      <ProjectsTableContent />
    </Suspense>
  )
}

function Projects() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Projects</h1>
          <p className="text-muted-foreground">
            Create and manage your projects
          </p>
        </div>
        <AddProject />
      </div>
      <ProjectsTable />
    </div>
  )
}
