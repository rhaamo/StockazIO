<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        v-model:filters="filters"
        :value="part_units"
        class="p-datatable-sm"
        striped-rows
        responsive-layout="scroll"
        :paginator="true"
        :rows="perPage"
        removable-sort
        :global-filter-fields="['name', 'short_name']">
        <template #header>
          <div class="grid">
            <div class="col-2">
              <PvButton label="Add a part unit" @click.prevent="showAddPartUnitModal" />
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
        <Column field="short_name" header="Short name" :sortable="true"></Column>
        <Column field="description" header="Description"></Column>

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
import ManagePartUnitModal from "@/components/part_units/Form.vue";
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
      part_units: (store) => {
        return store.part_units;
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
            label: "Units",
            command: () => {
              this.$router.push({ name: "part-units-list" });
            },
          },
        ],
      };
    },
  },
  methods: {
    fetchPartUnits() {
      apiService
        .getPartUnits()
        .then((val) => {
          this.preloadsStore.setPartUnits(val.data);
          this.preloadsStore.setLastUpdate("part_units", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Part units",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching part units", err);
        });
    },
    showAddPartUnitModal() {
      this.$dialog.open(ManagePartUnitModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a part unit")])];
          },
        },
        data: {
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload Part unit
            this.fetchPartUnits();
          }
        },
      });
    },
    editItem(event, item) {
      this.$dialog.open(ManagePartUnitModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit Part unit")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload Part unit
            this.fetchPartUnits();
          }
        },
      });
    },
    deleteItem(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the part unit '${item.name}' ?`,
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
            .deletePartUnit(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Part unit",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchPartUnits();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Part unit",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part deletion", err);
              this.fetchPartUnits();
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
