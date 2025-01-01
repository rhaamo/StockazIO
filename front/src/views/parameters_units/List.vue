<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        v-model:filters="filters"
        :value="parameters_units"
        class="p-datatable-sm"
        striped-rows
        responsive-layout="scroll"
        :paginator="true"
        :rows="perPage"
        removable-sort
        :global-filter-fields="['name', 'symbol']">
        <template #header>
          <div class="grid">
            <div class="col-2">
              <PvButton label="Add a parameter unit" @click.prevent="showAddParametersUnitsModal" />
            </div>

            <div class="col-2 col-offset-7">
              <div class="p-inputgroup">
                <IconField>
                  <InputIcon class="pi pi-search"></InputIcon>
                  <InputText v-model="filters['global'].value" placeholder="Keyword Search" />
                </IconField>
              </div>
            </div>
          </div>
        </template>

        <Column field="name" header="Name" :sortable="true"></Column>
        <Column field="symbol" header="Symbol" :sortable="true"></Column>
        <Column field="description" header="Description"></Column>

        <Column header-style="width: 6.3em">
          <template #body="slotProps">
            <span class="p-buttonset">
              <PvButton
                v-tooltip="'edit'"
                type="button"
                icon="fa fa-edit"
                class="p-button-primary"
                @click.prevent="editItem($event, slotProps.data)"></PvButton>
              <PvButton
                v-tooltip="'delete'"
                type="button"
                icon="fa fa-trash-o"
                class="p-button-danger ml-1"
                @click="deleteItem($event, slotProps.data)"></PvButton>
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
import ManageParametersUnitModal from "@/components/parameters_units/Form.vue";
import { h } from "vue";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";

export default {
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
  }),
  data: () => ({
    filters: {
      global: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    },
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      parameters_units: (store) => {
        return store.parameters_unit;
      },
    }),
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.PART_UNITS || 10,
    }),
    breadcrumb() {
      return {
        home: {
          icon: "pi pi-home",
          command: () => {
            this.$router.push({ name: "home" });
          },
        },
        items: [
          {
            label: "Parts",
            command: () => {
              this.$router.push({ name: "parts-list" });
            },
          },
          {
            label: "Parameters Units",
            command: () => {
              this.$router.push({ name: "parameters-units-list" });
            },
          },
        ],
      };
    },
  },
  methods: {
    fetchParametersUnits() {
      apiService
        .getParametersUnits()
        .then((val) => {
          this.preloadsStore.setParametersUnits(val.data);
          this.preloadsStore.setLastUpdate("parameters_unit", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Parameters units",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching parameters units", err);
        });
    },
    showAddParametersUnitsModal() {
      this.$dialog.open(ManageParametersUnitModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a parameter unit")])];
          },
        },
        data: {
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload Part unit
            this.fetchParametersUnits();
          }
        },
      });
    },
    editItem(event, item) {
      this.$dialog.open(ManageParametersUnitModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit Parameter unit")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload Part unit
            this.fetchParametersUnits();
          }
        },
      });
    },
    deleteItem(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the parameter unit '${item.name}' ?`,
        icon: "pi pi-exclamation-triangle",
        rejectProps: {
          label: "Cancel",
          severity: "secondary",
          outlined: true,
        },
        acceptProps: {
          label: "Delete",
          severity: "danger",
        },
        accept: () => {
          apiService
            .deleteParametersUnits(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Parameter unit",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchParametersUnits();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Parameter unit",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with parameter unit deletion", err);
              this.fetchParametersUnits();
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
