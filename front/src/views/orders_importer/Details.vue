<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <Message v-if="manufacturers_matched" severity="info"
      >The parts manufacturers have been fuzzy-matched, please check and correct
      if there is any wrong ones.</Message
    >

    <Message severity="warn"
      >Various items has been automatically selected to the best matching
      element, please review and don't forget to save.</Message
    >

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
            <div class="col-1">
              <Button label="save" @click.prevent="submit" />
            </div>
            <div class="col-2">
              <Button
                label="rematch categories"
                @click.prevent="rematchCategories"
              />
            </div>
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
          headerStyle="width: 17em"
        >
          <template #body="slotProps">
            {{ slotProps.data.manufacturer }}<br />
            <Dropdown
              inputId="manufacturer"
              v-model="slotProps.data.manufacturer_db"
              class="w-full"
              :options="choicesManufacturers"
              optionLabel="text"
              :filter="true"
              placeholder="match known one"
              :showClear="true"
            />
          </template>
        </Column>

        <Column
          header="Quantity"
          :sortable="false"
          field="quantity"
          headerStyle="width: 5em"
          bodyClass="text-center"
          headerClass="text-center"
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
          <template #body="slotProps">
            <TreeSelect
              inputId="category"
              placeholder="category to import in"
              v-model="slotProps.data.category"
              :options="choicesCategory"
              selectionMode="single"
              class="w-full"
            />
          </template>
        </Column>

        <Column
          header="do not import"
          field="ignore"
          headerStyle="width: 6em"
          bodyClass="text-center"
          headerClass="text-center"
        >
          <template #body="slotProps">
            <Checkbox v-model="slotProps.data.ignore" :binary="true" />
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
import Fuse from "fuse.js";

export default {
  data: () => ({
    order: {},
    loading: true,
    fuse_options: {
      includeScore: true,
      keys: ["text", "aliases"],
    },
    manufacturers_matched: false,
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
          return {
            value: x.id,
            text: x.name,
            datasheet_url: x.datasheet_url,
            aliases: x.aliases.split(",").map((x) => x.trim()),
          };
        }),
      choicesCategory: (store) => {
        const cb = (e) => {
          // base object
          let obj = {
            key: e.id,
            label: e.name,
            icon: `fa fa-folder-o`,
          };
          obj["selectable"] = true;
          obj["children"] = e.children.map(cb);
          return obj;
        };
        return [store.categories].map(cb);
      },
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

          // fix category & manufacturer objects for the dropdown thingy
          for (const [i] of this.order.items.entries()) {
            if (this.order.items[i].category) {
              this.order.items[i].category = {
                [this.order.items[i].category.id]: true,
              };
            }

            if (this.order.items[i].manufacturer_db) {
              this.order.items[i].manufacturer_db = {
                value: this.order.items[i].manufacturer_db.id,
                text: this.order.items[i].manufacturer_db.name,
                datasheet_url:
                  this.order.items[i].manufacturer_db.datasheet_url,
                aliases: this.order.items[i].manufacturer_db.aliases
                  .split(",")
                  .map((x) => x.trim()),
              };
            }
          }

          this.fuseMatchManufacturers();
          if (!this.order.vendor_db) {
            this.fuseMatchDistributor();
          } else {
            this.order.vendor_db = {
              value: this.order.vendor_db.id,
              text: this.order.vendor_db.name,
              datasheet_url: this.order.vendor_db.datasheet_url,
            };
          }
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
    fuseMatchManufacturers() {
      let fuse = new Fuse(this.choicesManufacturers, this.fuse_options);

      for (const [i] of this.order.items.entries()) {
        if (!this.order.items[i].manufacturer_db) {
          let results = fuse.search(this.order.items[i].manufacturer);

          if (results && results.length) {
            this.order.items[i].manufacturer_db = results[0].item;
          }
        }
      }

      this.manufacturers_matched = true;
    },
    fuseMatchDistributor() {
      let fuse = new Fuse(this.choicesDistributors, this.fuse_options);

      let results = fuse.search(this.order.vendor);

      if (results && results.length) {
        this.order.vendor_db = results[0].item;
      }
    },
    rematchCategories() {
      apiService
        .rematchOrderItems()
        .then((res) => {
          this.loadLazyData();
          this.fuseMatchManufacturers();
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Categories update",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error rematching categories", err);
        });
    },
    submit() {
      let datas = this.order;
      datas.vendor_db = datas.vendor_db ? datas.vendor_db.value : null;
      datas.items = datas.items.map((x) => {
        return {
          ...x,
          category: x.category ? parseInt(Object.keys(x.category)[0]) : null,
          manufacturer_db: x.manufacturer_db ? x.manufacturer_db.value : null,
        };
      });
      apiService
        .updateOrderImporter(this.order.id, datas)
        .then((res) => {
          this.toast.add({
            severity: "success",
            summary: "Order",
            detail: "Saved with success",
            life: 5000,
          });
          this.loadLazyData();
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Order",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error fetching order", err);
          this.loadLazyData();
        });
    },
  },
};
</script>
