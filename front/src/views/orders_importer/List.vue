<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        :value="orders"
        :lazy="true"
        :paginator="true"
        :rows="perPage"
        ref="dt"
        dataKey="id"
        :totalRecords="totalRecords"
        :loading="loading"
        @page="onPage($event)"
        @sort="onSort($event)"
        responsiveLayout="scroll"
        stripedRows
        class="p-datatable-sm"
        removableSort
      >
        <template #empty> No orders found. </template>

        <template #header>
          <router-link :to="{ name: 'orders-importer-category-matcher' }">
            <PvButton label="Manage category matchers"
          /></router-link>
        </template>

        <Column
          header="Date"
          :sortable="true"
          field="date"
          headerStyle="width: 12em"
        >
          <template #body="slotProps">
            <router-link
              class="no-underline"
              :to="{
                name: 'orders-importer-details',
                params: { id: slotProps.data.id },
              }"
              >{{ formatDate(slotProps.data.date) }}</router-link
            ></template
          >
        </Column>

        <Column header="Order Number" :sortable="true" field="order_number">
          <template #body="slotProps">
            <router-link
              class="no-underline"
              :to="{
                name: 'orders-importer-details',
                params: { id: slotProps.data.id },
              }"
              >{{ slotProps.data.order_number }}</router-link
            >
          </template>
        </Column>

        <Column
          header="Items Qty"
          :sortable="true"
          field="items_count"
          headerStyle="width: 8em"
        >
        </Column>

        <Column
          header="Status (vendor)"
          :sortable="false"
          field="status"
          headerStyle="width: 8em"
        >
        </Column>

        <Column header="Vendor" :sortable="true" field="vendor_db">
          <template #body="slotProps">
            {{ slotProps.data.vendor_db ? slotProps.data.vendor_db.name : "" }}
          </template>
        </Column>

        <Column
          header="Import state"
          :sortable="false"
          field="import_state"
          headerStyle="width: 8em"
        >
          <template #body="slotProps">{{
            importStateText(slotProps.data.import_state)
          }}</template>
        </Column>

        <Column headerStyle="width: 6em">
          <template #body="slotProps">
            <PvButton
              type="button"
              class="p-button-primary"
              v-tooltip="'import'"
              label="import"
              @click.prevent="importOrder($event, slotProps.data)"
              :disabled="
                slotProps.data.import_state === 2 ||
                slotProps.data.import_state === 99
              "
            ></PvButton>
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
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { useConfirm } from "primevue/useconfirm";
import dateFnsFormat from "date-fns/format";
import dateFnsParseISO from "date-fns/parseISO";

export default {
  data: () => ({
    breadcrumb: {
      home: { icon: "pi pi-home", to: "/" },
      items: [{ label: "Orders importer", to: { name: "orders-importer" } }],
    },
    orders: [],
    totalRecords: 0,
    loading: true,
    lazyParams: {},
  }),
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
  }),
  computed: {
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.ORDERS_IMPORTER || 20,
    }),
  },
  mounted() {
    this.lazyParams = {
      first: 0,
      rows: this.$refs.dt.rows,
      sortField: null,
      sortOrder: null,
    };

    this.$nextTick(() => {
      this.loadLazyData();
    });
  },
  methods: {
    loadLazyData() {
      this.loading = true;

      apiService
        .getOrdersImporter(this.lazyParams)
        .then((res) => {
          this.orders = res.data.results;
          this.totalRecords = res.data.count;
          this.loading = false;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Orders",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching orders", err);
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
    formatDate(date) {
      return date ? dateFnsFormat(dateFnsParseISO(date), "E d MMM yyyy") : "";
    },
    importStateText(state) {
      let states = {
        0: "Unknown",
        1: "Fetched",
        2: "Imported",
        99: "Error",
      };
      return states[state];
    },
    reloadCategories() {
      apiService
        .getCategories()
        .then((val) => {
          this.preloadsStore.setCategories(val.data[0]);
          this.preloadsStore.setLastUpdate("categories", new Date());
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Categories",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching categories", err);
        });
    },
    importOrder(event, order) {
      this.confirm.require({
        message: `Don't forget to edit it for categories and other fields.`,
        header: `Importing order '${order.order_number}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .importOrderToInventory(order.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Importing order",
                detail: "Success",
                life: 5000,
              });
              this.loading = true;
              this.loadLazyData();
              // reload for categories count after import
              this.reloadCategories();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Importing order",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with order import", err);
              this.loading = true;
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
