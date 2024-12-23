<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        :value="projects"
        :lazy="true"
        :paginator="true"
        :rows="perPage"
        v-model:filters="filters"
        ref="dt"
        dataKey="id"
        :totalRecords="totalRecords"
        :loading="loading"
        @page="onPage($event)"
        @sort="onSort($event)"
        @filter="onFilter($event)"
        filterDisplay="row"
        responsiveLayout="scroll"
        stripedRows
        class="p-datatable-sm"
        removableSort
      >
        <template #empty> No projects found. </template>

        <template #header>
          <PvButton
            label="Add a project"
            @click.prevent="showAddProjectModal"
          />
        </template>

        <Column
          header="Visibility"
          :sortable="false"
          field="visibility"
          headerStyle="width: 2em"
        >
          <template #body="slotProps">
            <div>
              <i
                v-if="slotProps.data.public"
                class="fa fa-globe"
                aria-hidden="true"
              />
              <i v-else class="fa fa-lock" aria-hidden="true" />
            </div>
          </template>
        </Column>

        <Column
          header="Name"
          :sortable="true"
          field="name"
          :filterMatchModeOptions="matchModes.name"
        >
          <template #body="slotProps">
            <div>
              <router-link
                class="no-underline"
                :to="{
                  name: 'projects-details',
                  params: { projectId: slotProps.data.id },
                }"
              >
                {{ slotProps.data.name }}
              </router-link>
            </div>
          </template>
          <template #filter="{ filterModel }">
            <InputText
              type="text"
              v-model="filterModel.value"
              class="p-column-filter"
              placeholder="Search by name"
            />
          </template>
        </Column>

        <Column header="Description" :sortable="false" field="description">
          <template #body="slotProps">
            <div>
              {{ slotProps.data.description || "-" }}
            </div>
          </template>
        </Column>

        <Column
          header="State"
          :sortable="true"
          field="state"
          :filterMatchModeOptions="matchModes.state"
        >
          <template #body="slotProps">
            <div>
              <span>{{ projectStateText(slotProps.data.state) }}</span>
              <div v-if="slotProps.data.state_notes">
                {{ slotProps.data.state_notes }}
              </div>
            </div>
          </template>
          <template #filter="{ filterModel }">
            <Dropdown
              v-model="filterModel.value"
              class="w-full"
              :options="projectStates"
              optionLabel="text"
              optionValue="value"
              :filter="false"
            />
          </template>
        </Column>

        <Column headerStyle="width: 6em">
          <template #body="slotProps">
            <span class="p-buttonset">
              <PvButton
                type="button"
                icon="fa fa-edit"
                class="p-button-primary"
                v-tooltip="'edit'"
                @click.prevent="editItem($event, slotProps.data)"
              ></PvButton>
              <PvButton
                type="button"
                icon="fa fa-trash-o"
                class="p-button-danger"
                v-tooltip="'delete'"
                @click="deleteItem($event, slotProps.data)"
              ></PvButton>
            </span>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { useServerStore } from "@/stores/server";
import { mapState } from "pinia";
import { FilterMatchMode } from "@primevue/core/api";
import ManageProjectModal from "@/components/project/Form.vue";
import { h } from "vue";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";

export default {
  data: () => ({
    breadcrumb: {
      home: {
        icon: "pi pi-home",
        command: () => {
          this.$router.push({ name: "home" });
        },
      },
      items: [
        {
          label: "Projects",
          command: () => {
            this.$router.push({ name: "projects-list" });
          },
        },
      ],
    },
    matchModes: {
      name: [
        { label: "Starts with", value: FilterMatchMode.STARTS_WITH },
        { label: "Contains", value: FilterMatchMode.CONTAINS },
        { label: "Not contains", value: FilterMatchMode.NOT_CONTAINS },
        { label: "Ends with", value: FilterMatchMode.ENDS_WITH },
        { label: "Equals", value: FilterMatchMode.EQUALS },
        { label: "Not equals", value: FilterMatchMode.NOT_EQUALS },
      ],
      state: [
        { label: "Equals", value: FilterMatchMode.EQUALS },
        { label: "Not equals", value: FilterMatchMode.NOT_EQUALS },
      ],
    },
    filters: {
      name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
      state: { value: null, matchMode: FilterMatchMode.EQUALS },
    },
    projects: [],
    totalRecords: 0,
    loading: true,
    lazyParams: {},
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
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
  }),
  computed: {
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.PROJECTS || 20,
    }),
  },
  mounted() {
    this.lazyParams = {
      first: 0,
      rows: this.$refs.dt.rows,
      sortField: null,
      sortOrder: null,
      filters: this.filters,
    };

    this.$nextTick(() => {
      this.loadLazyData();
    });
  },
  methods: {
    loadLazyData() {
      this.loading = true;

      apiService
        .getProjects(this.lazyParams)
        .then((res) => {
          this.projects = res.data.results;
          this.totalRecords = res.data.count;
          this.loading = false;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Projects",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching projects", err);
        });
    },
    onPage(event) {
      this.lazyParams = event;
      this.loadLazyData();
    },
    onSort(event) {
      this.lazyParams = event;
      this.loadLazyData();
    },
    onFilter(event) {
      this.lazyParams.filters = this.filters;
      this.loadLazyData();
    },
    projectStateText(value) {
      let a = this.projectStates.filter(function (e) {
        return e.value === value;
      });
      return a && a.length ? a[0].text : "Error";
    },
    showAddProjectModal() {
      this.$dialog.open(ManageProjectModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a project")])];
          },
        },
        data: {
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload projects
            this.loadLazyData();
          }
        },
      });
    },
    editItem(event, item) {
      this.$dialog.open(ManageProjectModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit project")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload Part unit
            this.loadLazyData();
          }
        },
      });
    },
    deleteItem(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the project '${item.name}' ?`,
        header: `Deleting '${item.name}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .deleteProject(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Project",
                detail: "Deleted",
                life: 5000,
              });
              this.loadLazyData();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Project",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with project deletion", err);
              this.loadLazyData();
            });
        },
        reject: () => {
          return;
        },
      });
    },
  },
};
</script>
