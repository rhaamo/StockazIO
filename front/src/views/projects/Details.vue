<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2" v-if="project">
      <div class="grid">
        <div class="col-6">
          <h3>
            <i v-if="!project.public" class="fa icon-private fa-lock mr-2" />
            {{ project.name }}
          </h3>
        </div>
        <div class="col-1 col-offset-5">
          <Button
            type="button"
            icon="fa fa-edit"
            class="p-button-primary"
            v-tooltip="'edit'"
            @click.prevent="showEditModal($event)"
          >
          </Button>

          <Button
            type="button"
            icon="fa fa-trash-o"
            class="p-button-danger ml-2"
            v-tooltip="'delete'"
            @click="deleteItem($event)"
          >
          </Button>
        </div>
      </div>

      <div class="grid">
        <div class="col-4">
          <div v-if="project.ibom_url">
            <b>Interactive BOM Url:</b>
            <a :href="project.ibom_url" target="_blank" class="ml-1">here</a>
          </div>

          <div class="mt-2">
            <b>State:</b>
            <span class="ml-1">{{ projectStateText(project.state) }}</span>
            <div v-if="project.state_notes" class="pl-2">
              {{ project.state_notes }}
            </div>
          </div>

          <div class="mt-2">
            <b>Description:</b>
            <div class="pl-2">
              {{ project.description || "None" }}
            </div>
          </div>

          <div class="mt-2">
            <b>Notes:</b>
            <div class="pl-2">
              {{ project.notes || "None" }}
            </div>
          </div>

          <Divider />

          <h4>Exports:</h4>
          <Button
            label="Project infos (text)"
            class="p-button-info"
            @click.prevent="exportProject('infos_txt')"
          />
          <Button
            label="BOM (CSV)"
            class="p-button-info ml-2"
            @click.prevent="exportProject('bom_csv')"
          />
          <Button
            label="BOM (Excel)"
            class="p-button-info ml-2"
            @click.prevent="exportProject('bom_xlsx')"
          />
        </div>

        <div class="col-8">
          <TabView>
            <TabPanel header="Parts"> xxx </TabPanel>
            <TabPanel header="Files attachments"> xxx </TabPanel>
          </TabView>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import logger from "@/logging";
import apiService from "@/services/api/api.service";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";

export default {
  data: () => ({
    project: null,
    projectStates: [
      { value: 1, text: "Planned" },
      { value: 2, text: "Ongoing" },
      { value: 3, text: "Finished" },
      { value: 4, text: "On-Hold" },
      { value: 5, text: "Abandonned" },
      { value: 99, text: "Unknown" },
      { value: null, text: "Filter by state" },
    ],
  }),
  setup: () => ({
    confirm: useConfirm(),
    toast: useToast(),
  }),
  computed: {
    projectId() {
      return this.$route.params.projectId;
    },
    breadcrumb() {
      let bc = {
        home: { icon: "pi pi-home", to: "/" },
        items: [{ label: "Projects", to: { name: "projects-list" } }],
      };
      if (this.project) {
        bc.items.push({
          label: this.project.name,
          to: {
            name: "projects-details",
            params: { projectId: this.project.id },
          },
        });
      }
      return bc;
    },
  },
  mounted() {
    this.fetchProject();
  },
  methods: {
    fetchProject() {
      apiService
        .getProject(this.projectId)
        .then((res) => {
          this.project = res.data;
        })
        .catch((err) => {
          if (err.request.status === 404) {
            this.$router.push({ name: "projects-list" });
            this.toast.add({
              severity: "error",
              summary: "Fetching project details",
              detail: "Project not found",
              life: 5000,
            });
            return;
          }

          this.toast.add({
            severity: "error",
            summary: "Fetching project details",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with project fetch", err.message);
        });
    },
    showEditModal(event) {
      //
    },
    deleteItem(event) {
      this.confirm.require({
        message: `Are you sure you want to delete the project '${this.project.name}' ?`,
        header: `Deleting '${this.project.name}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .deleteProject(this.project.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Project",
                detail: "Deleted",
                life: 5000,
              });
              this.$router.push({ name: "projects-list" });
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Project",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with project deletion", err);
              this.$router.push({ name: "projects-list" });
            });
        },
        reject: () => {
          return;
        },
      });
    },
    projectStateText(value) {
      let a = this.projectStates.filter(function (e) {
        return e.value === value;
      });
      return a && a.length ? a[0].text : "Error";
    },
    exportProject(kind) {
      if (kind === "infos_txt") {
        apiService.projectExportInfosTxt(
          this.project.id,
          `${this.project.name}.txt`
        );
      } else if (kind === "bom_csv") {
        apiService.projectExportBomCSV(
          this.project.id,
          `${this.project.name}__bom.csv`
        );
      } else if (kind === "bom_xlsx") {
        apiService.projectExportBomXLSX(
          this.project.id,
          `${this.project.name}__bom.xlsx`
        );
      }
    },
  },
};
</script>
