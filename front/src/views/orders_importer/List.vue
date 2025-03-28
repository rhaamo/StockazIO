<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        ref="dt"
        :value="orders"
        :lazy="true"
        :paginator="true"
        :rows="perPage"
        data-key="id"
        :total-records="totalRecords"
        :loading="loading"
        responsive-layout="scroll"
        striped-rows
        class="p-datatable-sm"
        removable-sort
        @page="onPage($event)"
        @sort="onSort($event)">
        <template #empty> No orders found. </template>

        <template #header>
          <router-link :to="{ name: 'orders-importer-category-matcher' }"> <PvButton label="Manage category matchers" /></router-link>

          <PvButton class="ml-2" severity="info" label="Import a LCSC .csv order" @click.prevent="showImportLCSCcsv" />
        </template>

        <Column header="Date" :sortable="true" field="date" header-style="width: 12em">
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

        <Column header="Items Qty" :sortable="true" field="items_count" header-style="width: 8em"> </Column>

        <Column header="Status (vendor)" :sortable="false" field="status" header-style="width: 8em"> </Column>

        <Column header="Vendor" :sortable="true" field="vendor_db">
          <template #body="slotProps">
            {{ slotProps.data.vendor_db ? slotProps.data.vendor_db.name : "" }}
          </template>
        </Column>

        <Column header="Import state" :sortable="false" field="import_state" header-style="width: 8em">
          <template #body="slotProps">{{ importStateText(slotProps.data.import_state) }}</template>
        </Column>

        <Column header-style="width: 6em">
          <template #body="slotProps">
            <PvButton
              v-tooltip.left="'Import selected items in the inventory'"
              type="button"
              class="p-button-primary"
              label="import"
              v-if="slotProps.data.import_state !== 2 && slotProps.data.import_state !== 99"
              @click.prevent="importOrder($event, slotProps.data)"></PvButton>
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
import { format as dateFnsFormat } from "date-fns/format";
import { parseISO as dateFnsParseISO } from "date-fns/parseISO";
import { h } from "vue";
import ImportLCSCorderModal from "@/components/orders/LcscCsv.vue";

export default {
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
  }),
  data: () => ({
    orders: [],
    totalRecords: 0,
    loading: true,
    lazyParams: {},
  }),
  computed: {
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.ORDERS_IMPORTER || 20,
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
            label: "Orders importer",
            command: () => {
              this.$router.push({ name: "orders-importer" });
            },
          },
        ],
      };
    },
  },
  mounted() {
    this.lazyParams = {
      first: 0,
      rows: this.$refs.dt.rows,
      sortField: "date",
      sortOrder: -1,
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
        icon: "pi pi-exclamation-triangle",
        rejectProps: {
          label: "Cancel",
          severity: "danger",
          outlined: true,
        },
        acceptProps: {
          label: "Import",
          severity: "primary",
        },
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
    showImportLCSCcsv() {
      this.$dialog.open(ImportLCSCorderModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Import LCSC .csv order")])];
          },
        },
        data: {},
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload orders
            this.loadLazyData();
          }
        },
      });
    },
  },
};
</script>
