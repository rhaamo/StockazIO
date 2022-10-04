<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2">
      <DataTable
        :value="order.items"
        :lazy="true"
        :paginator="false"
        ref="dt"
        dataKey="id"
        :loading="loading"
        responsiveLayout="scroll"
        stripedRows
        class="p-datatable-sm"
      >
        <template #empty> No orders found. </template>

        <template #header>
          <div class="grid">
            <div class="col-1"><Button label="save" /></div>
            <div class="col-2"><Button label="rematch categories" /></div>
            <div class="col-3">
              <b>Ordered:</b> {{ formatDate(order.date) }}<br />
              <b>Number:</b> {{ order.order_number }}<br />
              <b>Items:</b> {{ rows }}
            </div>
            <div class="4">
              <b>Import state:</b> {{ importStateText(order.import_state)
              }}<br />
              <b>From:</b> {{ order.vendor }}<br />
              <Dropdown
                inputId="distributor"
                v-model="order.vendor_db"
                class="w-full"
                :options="choicesDistributors"
                optionLabel="text"
                :filter="true"
                placeholder="match known one"
              />
            </div>
          </div>
        </template>

        <Column
          header="Manufacturer PN"
          :sortable="false"
          field="mfr_part_number"
          headerStyle="width: 15em"
        >
          <template #body="slotProps">
            <span class="text-sm">{{ slotProps.data.mfr_part_number }}</span>
          </template>
        </Column>

        <Column header="Description" :sortable="false" field="description">
          <template #body="slotProps">
            <span class="text-sm">{{ slotProps.data.description }}</span>
          </template>
        </Column>

        <Column
          header="Manufacturer"
          :sortable="false"
          field="manufacturer_db"
          headerStyle="width: 16em"
        >
          <template #body="slotProps">
            {{ slotProps.data.manufacturer }}<br />
            <Dropdown
              inputId="manufacturer"
              v-model="slotProps.data.manufacturer_db"
              class="w-10"
              :options="choicesManufacturers"
              optionLabel="text"
              :filter="true"
              placeholder="match known one"
            />
          </template>
        </Column>

        <Column
          header="Quantity"
          :sortable="false"
          field="quantity"
          headerStyle="width: 5em"
        >
        </Column>

        <Column
          header="Vendor PN"
          :sortable="false"
          field="vendor_part_number"
          headerStyle="width: 15em"
        >
          <template #body="slotProps">
            <span class="text-sm">{{ slotProps.data.vendor_part_number }}</span>
          </template>
        </Column>

        <Column
          header="Category"
          :sortable="false"
          field="category"
          headerStyle="width: 15em"
        >
          xxx input
        </Column>

        <Column header="do not import" field="ignore" headerStyle="width: 6em">
          xxx checkbox
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
    order: {},
    loading: true,
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
    ...mapState(usePreloadsStore, {
      choicesDistributors: (store) =>
        store.distributors.map((x) => {
          return { value: x.id, text: x.name, datasheet_url: x.datasheet_url };
        }),
      choicesManufacturers: (store) =>
        store.manufacturers.map((x) => {
          return { value: x.id, text: x.name, datasheet_url: x.datasheet_url };
        }),
    }),
    orderId() {
      return this.$route.params.id;
    },
    breadcrumb() {
      let bc = {
        home: { icon: "pi pi-home", to: "/" },
        items: [{ label: "Orders importer", to: { name: "orders-importer" } }],
      };
      if (this.order) {
        bc.items.push({ label: this.order.order_number });
      }
      return bc;
    },
    rows() {
      return this.order && this.order.items ? this.order.items.length : "n/a";
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.loadLazyData();
    });
  },
  methods: {
    loadLazyData() {
      this.loading = true;

      apiService
        .getOrderImporter(this.orderId)
        .then((res) => {
          this.order = res.data;
          this.loading = false;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Order",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching order", err);
        });
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
  },
};
</script>
