<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        v-model:filters="filters"
        :value="part_parameters_presets"
        class="p-datatable-sm"
        striped-rows
        responsive-layout="scroll"
        :paginator="true"
        :rows="perPage"
        removable-sort
        :global-filter-fields="['name']">
        <template #header>
          <div class="grid">
            <div class="col-2">
              <PvButton label="Add a part parameter preset" @click.prevent="showAddParametersUnitsModal" />
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
        <Column header="Parameters">
          <template #body="slotProps">
            <DataTable
              :value="slotProps.data.part_parameters_presets"
              class="p-datatable-sm"
              striped-rows
              responsive-layout="scroll"
              :paginator="false">
              <Column field="name" header="Name" :sortable="true"></Column>
              <Column header="Unit">
                <template #body="slotProps2">
                  <template v-if="slotProps2.data.unit"> {{ slotProps2.data.unit.symbol }} ({{ slotProps2.data.unit.name }}) </template>
                </template>
              </Column>
              <Column field="description" header="Description"></Column>
            </DataTable>
          </template>
        </Column>

        <Column header-style="width: 6.3em">
          <template #body="slotProps">
            <ButtonsEditDelete @edit="editItem($event, slotProps.data)" @delete="deleteItem($event, slotProps.data)" />
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
import ManagePartParametersPresets from "@/components/part_parameters_presets/Form.vue";
import { h } from "vue";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";
import ButtonsEditDelete from "@/components/btn_edit_delete.vue";

export default {
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
  }),
  components: {
    ButtonsEditDelete,
  },
  data: () => ({
    filters: {
      global: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    },
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      part_parameters_presets: (store) => {
        return store.partParametersPresets;
      },
    }),
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.PART_PARAMETERS_PRESETS || 10,
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
            label: "Parameters Presets",
            command: () => {
              this.$router.push({ name: "parameters-presets-list" });
            },
          },
        ],
      };
    },
  },
  methods: {
    fetchPartParameterPresets() {
      apiService
        .getPartParameterPresets()
        .then((val) => {
          this.preloadsStore.setPartParametersPresets(val.data.results);
          this.preloadsStore.setLastUpdate("parameters_presets", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Part Parameters Presets",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching Part Parameters Presets", err);
        });
    },
    showAddParametersUnitsModal() {
      this.$dialog.open(ManagePartParametersPresets, {
        props: {
          modal: true,
          style: {
            width: "35vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a Part Parameters Preset")])];
          },
        },
        data: {
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload Part unit
            this.fetchPartParameterPresets();
          }
        },
      });
    },
    editItem(event, item) {
      this.$dialog.open(ManagePartParametersPresets, {
        props: {
          modal: true,
          style: {
            width: "35vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit Part Parameters Preset")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload Part unit
            this.fetchPartParameterPresets();
          }
        },
      });
    },
    deleteItem(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the part parameters presets '${item.name}' ?`,
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
            .deletePartParameterPresets(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Part Parameters Preset",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchPartParameterPresets();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Part Parameters Preset",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part parameters presets deletion", err);
              this.fetchPartParameterPresets();
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
