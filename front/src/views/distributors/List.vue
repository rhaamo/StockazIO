<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        :value="distributors"
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
                label="Add a distributor"
                @click.prevent="showAddDistributorModal"
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

        <Column headerStyle="width: 6em">
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
import ManageDistributorModal from "@/components/distributors/Form.vue";
import { h } from "vue";
import apiService from "../../services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";

export default {
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Distributors", to: { name: "distributors-list" } }],
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
      distributors: (store) => {
        return store.distributors;
      },
    }),
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.DISTRIBUTORS || 10,
    }),
  },
  methods: {
    fetchDistributors() {
      apiService
        .getDistributors()
        .then((val) => {
          this.preloadsStore.setDistributors(val.data);
          this.preloadsStore.setLastUpdate("distributors", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Distributors",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching distributors", err);
        });
    },
    showAddDistributorModal() {
      const addDistributorRef = this.$dialog.open(ManageDistributorModal, {
        props: {
          modal: true,
          style: {
            width: "50vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add a distributor")])];
          },
        },
        data: {
          mode: "add",
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload distributors
            this.fetchDistributors();
          }
        },
      });
    },
    editItem(event, item) {
      const editDistributorRef = this.$dialog.open(ManageDistributorModal, {
        props: {
          modal: true,
          style: {
            width: "50vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit distributor")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload distributors
            this.fetchDistributors();
          }
        },
      });
    },
    deleteItem(event, item) {
      this.confirm.require({
        message: `Are you sure you want to delete the distributor '${item.name}' ?`,
        header: `Deleting '${item.name}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .deleteDistributor(item.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Distributor",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchDistributors();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Distributor",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part deletion", err);
              this.fetchDistributors();
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
