<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        v-model:filters="filters"
        :value="distributors"
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
              <PvButton label="Add a distributor" @click.prevent="showAddDistributorModal" />
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
import ManageDistributorModal from "@/components/distributors/Form.vue";
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
      distributors: (store) => {
        return store.distributors;
      },
    }),
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.DISTRIBUTORS || 10,
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
            label: "Distributors",
            command: () => {
              this.$router.push({ name: "distributors-list" });
            },
          },
        ],
      };
    },
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
      this.$dialog.open(ManageDistributorModal, {
        props: {
          modal: true,
          style: {
            width: "50vw",
          },
          dismissableMask: true,
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
      this.$dialog.open(ManageDistributorModal, {
        props: {
          modal: true,
          style: {
            width: "50vw",
          },
          dismissableMask: true,
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
