<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        :value="manufacturers"
        class="p-datatable-sm"
        stripedRows
        responsiveLayout="scroll"
        :paginator="true"
        :rows="perPage"
        removableSort
        :globalFilterFields="['name']"
        v-model:filters="filters"
      >
        <template #header>
          <div class="grid">
            <div class="col-2">
              <Button
                label="Add a manufacturer"
                @click.prevent="showAddManufacturerModal"
              />
            </div>

            <div class="col-2 col-offset-7">
              <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText
                  v-model="filters['global'].value"
                  placeholder="Keyword Search"
                />
              </span>
            </div>
          </div>
        </template>

        <Column field="name" header="Name" :sortable="true"></Column>
        <Column field="logo" header="Logo">
          <template #body="slotProps">
            <img
              :src="slotProps.data.logo_mini"
              style="max-width: 100px"
              :alt="slotProps.data.name"
              lazy
              v-if="slotProps.data.logo"
            />
          </template>
        </Column>
        <Column field="address" header="Address"></Column>
        <Column field="url" header="URL">
          <template #body="slotProps">
            <template v-if="slotProps.data.url">
              Website:
              <a :href="slotProps.data.url" target="_blank">{{
                slotProps.data.url
              }}</a>
            </template>
            <template v-if="slotProps.data.url && slotProps.data.email"
              ><br
            /></template>
            <template v-if="slotProps.data.email">
              Email: {{ slotProps.data.email }}
            </template>

            <template
              v-if="
                slotProps.data.datasheet_url &&
                (slotProps.data.email || slotProps.data.url)
              "
              ><br
            /></template>
            <template v-if="slotProps.data.datasheet_url">
              Datasheet template: {{ slotProps.data.datasheet_url }}
            </template>
          </template>
        </Column>
        <Column field="comment" header="Comment"></Column>
        <Column field="phones" header="Phones">
          <template #body="slotProps">
            <template v-if="slotProps.data.phone">
              Tel: {{ slotProps.data.phone }}
            </template>
            <template v-if="slotProps.data.phone && slotProps.data.fax">
              <br />
            </template>
            <template v-if="slotProps.data.fax">
              Fax: {{ slotProps.data.fax }}
            </template>
          </template>
        </Column>

        <Column>
          <template #body="slotProps">
            <span class="p-buttonset">
              <Button
                type="button"
                icon="fa fa-edit"
                class="p-button-primary"
                v-tooltip="'edit'"
                @click.prevent="editItem($event, slotProps.data)"
              ></Button>
              <Button
                type="button"
                icon="fa fa-trash-o"
                class="p-button-danger"
                v-tooltip="'delete'"
                @click="deleteItem($event, slotProps.data)"
              ></Button>
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
import { FilterMatchMode } from "primevue/api";
import ManageManufacturerModal from "@/components/manufacturers/Form.vue";
import { h } from "vue";
import apiService from "../../services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";

export default {
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Manufacturers" }],
    },
    filters: {
      global: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    },
  }),
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      manufacturers: (store) => {
        return store.manufacturers;
      },
    }),
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.MANUFACTURERS || 10,
    }),
  },
  methods: {
    fetchManufacturers() {
      apiService
        .getManufacturers()
        .then((val) => {
          this.preloadsStore.setManufacturers(val.data);
          this.preloadsStore.setLastUpdate("manufacturers", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Manufacturers",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching manufacturers", err);
        });
    },
    showAddManufacturerModal() {
      const addManufacturerRef = this.$dialog.open(ManageManufacturerModal, {
        props: {
          modal: true,
          style: {
            width: "50vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a manufacturer")])];
          },
        },
        data: {
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload manufacturers
            this.fetchManufacturers();
          }
        },
      });
    },
    editItem(event, item) {
      const editManufacturerRef = this.$dialog.open(ManageManufacturerModal, {
        props: {
          modal: true,
          style: {
            width: "50vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit manufacturer")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload manufacturers
            this.fetchManufacturers();
          }
        },
      });
    },
    deleteItem(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the manufacturer '${item.name}' ?`,
        header: `Deleting '${item.name}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .deleteManufacturer(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Manufacturer",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchManufacturers();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Manufacturer",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part deletion", err);
              this.fetchManufacturers();
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
