<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        v-model:filters="filters"
        :value="manufacturers"
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
              <PvButton label="Add a manufacturer" @click.prevent="showAddManufacturerModal" />
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

        <Column field="name" header="Name" :sortable="true">
          <template #body="slotProps">
            {{ slotProps.data.name }}
            <template v-if="slotProps.data.aliases">
              <br />
              <small>aliases: {{ slotProps.data.aliases }}</small>
            </template>
          </template>
        </Column>
        <Column field="logo" header="Logo">
          <template #body="slotProps">
            <img v-if="slotProps.data.logo" :src="slotProps.data.logo_mini" style="max-width: 100px" :alt="slotProps.data.name" lazy />
          </template>
        </Column>
        <Column field="address" header="Address"></Column>
        <Column field="url" header="URL">
          <template #body="slotProps">
            <template v-if="slotProps.data.url">
              Website:
              <a :href="slotProps.data.url" target="_blank">{{ slotProps.data.url }}</a>
            </template>
            <template v-if="slotProps.data.url && slotProps.data.email"><br /></template>
            <template v-if="slotProps.data.email"> Email: {{ slotProps.data.email }} </template>

            <template v-if="slotProps.data.datasheet_url && (slotProps.data.email || slotProps.data.url)"><br /></template>
            <template v-if="slotProps.data.datasheet_url"> Datasheet template: {{ slotProps.data.datasheet_url }} </template>
          </template>
        </Column>
        <Column field="comment" header="Comment"></Column>
        <Column field="phones" header="Phones">
          <template #body="slotProps">
            <template v-if="slotProps.data.phone"> Tel: {{ slotProps.data.phone }} </template>
            <template v-if="slotProps.data.phone && slotProps.data.fax">
              <br />
            </template>
            <template v-if="slotProps.data.fax"> Fax: {{ slotProps.data.fax }} </template>
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
import ManageManufacturerModal from "@/components/manufacturers/Form.vue";
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
      manufacturers: (store) => {
        return store.manufacturers;
      },
    }),
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.MANUFACTURERS || 10,
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
            label: "Manufacturers",
            command: () => {
              this.$router.push({ name: "manufacturers-list" });
            },
          },
        ],
      };
    },
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
      this.$dialog.open(ManageManufacturerModal, {
        props: {
          modal: true,
          style: {
            width: "50vw",
          },
          dismissableMask: true,
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
      this.$dialog.open(ManageManufacturerModal, {
        props: {
          modal: true,
          style: {
            width: "50vw",
          },
          dismissableMask: true,
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
