<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" class="mb-2" />

    <Message v-if="manufacturers_matched" severity="info" class="mb-2"
      >The parts manufacturers have been fuzzy-matched, please check and correct if there is any wrong ones.</Message
    >

    <Message severity="warn" class="mb-2"
      >Various items has been automatically selected to the best matching element, <b>please review and <u>don't forget to save</u></b
      >.</Message
    >

    <div class="mt-2">
      <DataTable
        ref="dt"
        :value="order.items"
        :lazy="true"
        :paginator="false"
        data-key="id"
        :loading="loading"
        responsive-layout="scroll"
        striped-rows
        class="p-datatable-sm">
        <template #empty> No orders found. </template>

        <template #header>
          <div class="grid">
            <div class="col-1">
              <PvButton label="save" @click.prevent="submit" />
            </div>
            <div class="col-2">
              <PvButton label="automatch manufacturers" severity="info" @click.prevent="fuseMatchManufacturers" />
            </div>
            <div class="col-2">
              <PvButton label="automatch categories" severity="info" @click.prevent="rematchCategories" />
            </div>
            <div class="col-2">
              <router-link v-tooltip.top="'Bulk-generate labels'" to="#" class="no-underline" @click.prevent="showBulkLabelGenerator()">
                <PvButton label="bulk label generator" severity="help" />
              </router-link>
            </div>
            <div class="col-3">
              <b>Ordered:</b> {{ formatDate(order.date) }}<br />
              <b>Number:</b> {{ order.order_number }}<br />
              <b>Items:</b> {{ rows }}
            </div>
            <div class="4">
              <b>Import state:</b> {{ importStateText(order.import_state) }}<br />
              <b>From:</b> {{ order.vendor }}<br />
              <Dropdown
                v-model="order.vendor_db"
                input-id="distributor"
                class="w-full"
                :options="choicesDistributors"
                option-label="text"
                :filter="true"
                placeholder="match known one" />
            </div>
          </div>
        </template>

        <Column header="Manufacturer PN" :sortable="false" field="mfr_part_number" header-style="width: 15em">
          <template #body="slotProps">
            <template v-if="slotProps.data.new_in_stock && slotProps.data.part_db">
              <div class="flex items-center gap-2">
                <div @click="showLabelGenerator(slotProps.data.part_db)">
                  <vue-qrcode
                    :id="qrcodeId(slotProps.data.part_db.id)"
                    v-tooltip="'show label generator'"
                    :value="qrCodePart(slotProps.data.part_db.uuid)"
                    :options="{
                      scale: 1,
                      color: { dark: '#000000', light: '#FFFFFF' },
                    }"
                    :data-uuid="slotProps.data.part_db.uuid"
                    :data-name="slotProps.data.part_db.name"
                    data-toggle="modal"
                    data-target="#modalQrCode" />
                </div>

                <div>
                  <a href="#" class="no-underline" @click.prevent="viewPartModal(slotProps.data)">{{ slotProps.data.mfr_part_number }}</a>
                  <br />
                  <small><i>This is a new part in stock, you can print a label now</i></small>
                </div>
              </div>
            </template>
            <template v-else>
              {{ slotProps.data.mfr_part_number }}
              <br />
              <small><i>This part was already in stock, qty was incremented</i></small>
            </template>
          </template>
        </Column>

        <Column header="Description" :sortable="false" field="description">
          <template #body="slotProps">
            <span class="text-sm">{{ slotProps.data.description }}</span>
          </template>
        </Column>

        <Column header="Footprint" :sortable="false" field="footprint_db" header-style="width: 20em">
          <template #body="slotProps">
            <Dropdown
              v-model="slotProps.data.footprint_db"
              input-id="footprint"
              placeholder="match known one"
              :options="choicesFootprints"
              option-label="name"
              option-value="id"
              option-group-label="category"
              option-group-children="footprints"
              :filter="true"
              auto-filter-focus
              show-clear />
          </template>
        </Column>

        <Column header="Manufacturer" :sortable="false" field="manufacturer_db" header-style="width: 20em">
          <template #body="slotProps">
            {{ slotProps.data.manufacturer }}<br />
            <Dropdown
              v-model="slotProps.data.manufacturer_db"
              input-id="manufacturer"
              class="w-full"
              :options="choicesManufacturers"
              option-label="text"
              :filter="true"
              placeholder="match known one"
              :show-clear="true" />
          </template>
        </Column>

        <Column header="Quantity" :sortable="false" field="quantity" header-style="width: 5em" body-class="text-center" header-class="text-center">
        </Column>

        <Column header="Vendor PN" :sortable="false" field="vendor_part_number">
          <template #body="slotProps">
            <span class="text-sm">{{ slotProps.data.vendor_part_number }}</span>
          </template>
        </Column>

        <Column header="Category" :sortable="false" field="category" header-style="width: 25em">
          <template #body="slotProps">
            <TreeSelect
              v-model="slotProps.data.category"
              input-id="category"
              placeholder="category to import in"
              :options="choicesCategory"
              selection-mode="single"
              class="w-full"
              :filter="true"
              :fluid="true"
              :show-clear="true" />
          </template>
        </Column>

        <Column header="do not import" field="ignore" header-style="width: 6em" body-class="text-center" header-class="text-center">
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
import { format as dateFnsFormat } from "date-fns/format";
import { parseISO as dateFnsParseISO } from "date-fns/parseISO";
import Fuse from "fuse.js";
import { fuzzyMatch } from "fuzzbunny";
import PartViewModal from "@/components/parts/view.vue";
import { h } from "vue";
import Button from "primevue/button";
import LabelGeneratorModal from "@/components/label/generator.vue";

export default {
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
    confirm: useConfirm(),
  }),
  data: () => ({
    order: {},
    loading: true,
    fuse_options: {
      includeScore: true,
      keys: ["text", "aliases", "name"],
    },
    manufacturers_matched: false,
    footprints_matched: false,
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
      choicesFootprints: (store) =>
        store.footprints.map((x) => {
          return {
            category: x.name,
            footprints: x.footprint_set.map((y) => {
              return { id: y.id, name: y.name };
            }),
          };
        }),
      flattenedChoicesFootprints: (store) =>
        store.footprints
          .map((x) => {
            return x.footprint_set.map((y) => {
              return { id: y.id, name: y.name };
            });
          })
          .flat(),
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

          // fix category, manufacturer and footprint objects for the dropdown thingy
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
                datasheet_url: this.order.items[i].manufacturer_db.datasheet_url,
                aliases: this.order.items[i].manufacturer_db.aliases.split(",").map((x) => x.trim()),
              };
            }

            if (this.order.items[i].footprint_db) {
              this.order.items[i].footprint_db = this.order.items[i].footprint_db.id;
            }
          }

          this.fuseMatchFootprints();
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
      // using Fuse.io here because we have a list of manufacturers to match a manufacturer string against it
      let fuse = new Fuse(this.choicesManufacturers, this.fuse_options);

      for (const [i] of this.order.items.entries()) {
        // if there is no associated manufacturer, match it
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
    fuseMatchFootprints() {
      // using fuzzbunny here because we can't fuzzy search "12gigawatt SOT-23 super-component" against a list of [sot-23, tssop, bga...]
      // so instead we try to match every items in the footprints against the description, and accepts the first match found
      for (const [i] of this.order.items.entries()) {
        // if there is no associated footprint, match it
        if (this.order.items[i].footprint_db === null) {
          for (const j of this.flattenedChoicesFootprints) {
            const match = fuzzyMatch(this.order.items[i].description, j.name);
            if (match) {
              // Match found, break the loop for this item
              this.order.items[i].footprint_db = j.id;
              break;
            }
          }
        }
      }

      this.footprints_matched = true;
    },
    rematchCategories() {
      apiService
        .rematchOrderItems()
        .then((res) => {
          this.loadLazyData();
          this.fuseMatchManufacturers();
          this.fuseMatchFootprints();
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
    viewPartModal(item) {
      let part = item.part_db;
      // Get full part object infos
      apiService
        .getPart(part.id)
        .then((val) => {
          const viewPartRef = this.$dialog.open(PartViewModal, {
            props: {
              modal: true,
              style: {
                width: "70vw",
              },
              dismissableMask: true,
              draggable: false,
            },
            templates: {
              header: () => {
                if (part.private) {
                  return [h("h1", [h("i", { class: "fa fa-lock mr-1" }), h("span", part.name)])];
                } else {
                  return [h("h1", part.name)];
                }
              },
              footer: () => {
                return [
                  h(Button, {
                    label: "Show full details",
                    onClick: () => {
                      viewPartRef.close();
                      this.$router.replace({
                        name: "parts-details",
                        params: { partId: part.id },
                      });
                    },
                    class: "p-button-outlined",
                  }),
                  h(Button, {
                    label: "Delete",
                    onClick: () => {
                      this.deletePart(null, part);
                      viewPartRef.close();
                    },
                    class: "p-button-danger",
                  }),
                  h(Button, {
                    label: "Close",
                    onClick: () => viewPartRef.close(),
                    class: "p-button-success",
                  }),
                ];
              },
            },
            data: {
              part: val.data,
            },
          });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Part details",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with getting part details", err);
        });
    },
    showLabelGenerator(item) {
      this.$dialog.open(LabelGeneratorModal, {
        props: {
          modal: true,
          style: {
            width: "70vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("i", { class: "fa fa-qrcode mr-1" }), h("span", "Label Generator")])];
          },
        },
        data: {
          items: [item],
          kind: "part",
        },
      });
    },
    qrcodeId(id, size) {
      return size ? `qrcode-${id}-${size}` : `qrcode-${id}`;
    },
    qrCodePart(uuid) {
      return `web+stockazio:part,${uuid}`;
    },
    showBulkLabelGenerator() {
      // Duplicate the orders list but filtered for new parts with part db associated, then map it to only get the part_db objects
      let slocs = [...this.order.items.filter((x) => x.part_db && x.new_in_stock)].map((x) => {
        return x.part_db;
      });
      console.log(slocs);

      this.$dialog.open(LabelGeneratorModal, {
        props: {
          modal: true,
          style: {
            width: "70vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("i", { class: "fa fa-qrcode mr-1" }), h("span", "Label Generator")])];
          },
        },
        data: {
          items: slocs,
          kind: "part",
        },
      });
    },
  },
};
</script>
