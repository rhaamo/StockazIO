<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <div class="mt-4 pt-0 pl-0 pr-0">
      <Tabs value="0" scrollable>
        <TabList>
          <Tab value="0"><i class="pi pi-table mr-2"></i><span>Table</span></Tab>
          <Tab value="1"><i class="pi pi-image mr-2"></i> <span>Thumbnails</span></Tab>
        </TabList>
        <TabPanels>
          <!-- Table -->
          <TabPanel value="0">
            <DataTable
              ref="dt"
              v-model:filters="filters"
              :value="parts"
              :lazy="true"
              :paginator="true"
              :rows="perPage"
              data-key="id"
              :total-records="totalRecords"
              :loading="loading"
              filter-display="row"
              responsive-layout="scroll"
              striped-rows
              class="p-datatable-sm"
              removable-sort
              @page="onPage($event)"
              @sort="onSort($event)"
              @filter="onFilter($event)">
              <template #empty> No parts found. </template>

              <template #header>
                <div class="field-checkbox">
                  <Checkbox v-model="lazyParams.sellable" input-id="only_sellable" :binary="true" />
                  <label for="only_sellable">Only show sellable parts</label>
                </div>
              </template>

              <Column header="Name" :sortable="true" field="name" :filter-match-mode-options="matchModes.name">
                <template #body="slotProps">
                  <div>
                    <template v-if="partGetDefaultAttachment(slotProps.data.part_attachments)">
                      <i
                        :id="`p_a_${slotProps.data.id}`"
                        v-tooltip="'Click to show picture'"
                        class="pi pi-image mr-1"
                        aria-hidden="true"
                        @click="toggleOverlayPanel($event, `p_a_${slotProps.data.id}`)" />
                      <Popover :id="`p_a_${slotProps.data.id}`" :ref="`p_a_${slotProps.data.id}`" append-to="body" :show-close-icon="true">
                        <PvImage preview width="250" :src="partGetDefaultAttachment(slotProps.data.part_attachments).picture_medium"></PvImage>
                      </Popover>
                    </template>
                    <a href="#" class="no-underline" @click.prevent="viewPartModal(slotProps.data)">{{ slotProps.data.name }}</a>
                    <br />
                    <template v-if="slotProps.data.description">
                      {{ slotProps.data.category ? slotProps.data.category.name : "No category" }}: {{ slotProps.data.description }}
                    </template>
                    <template v-else>
                      {{ slotProps.data.category ? slotProps.data.category.name : "No category" }}
                    </template>
                  </div>
                </template>
                <template #filter="{ filterModel, filterCallback }">
                  <InputText
                    v-model="filterModel.value"
                    v-tooltip.top.focus="'Hit enter key to filter'"
                    type="text"
                    class="p-column-filter"
                    placeholder="Search by name"
                    @keydown.enter="filterCallback()" />
                </template>
              </Column>
              <Column header="Storage" :sortable="true" field="storage_id" :filter-match-mode-options="matchModes.storage">
                <template #body="slotProps">{{ slotProps.data.storage && slotProps.data.storage.name ? slotProps.data.storage.name : "-" }}</template>
                <template #filter="{ filterModel, filterCallback }">
                  <TreeSelect
                    v-model="filterModel.value"
                    class="p-column-filter"
                    placeholder="Search by storage"
                    :options="choicesStorageLocationWithNo"
                    selection-mode="single"
                    @change="filterCallback()" />
                </template>
              </Column>
              <Column header="Stock" :sortable="true" field="stock_qty" data-type="numeric" :filter-match-mode-options="matchModes.qty">
                <template #body="slotProps">
                  <template v-if="slotProps.data.stock_qty >= slotProps.data.stock_qty_min"
                    ><span>{{ slotProps.data.stock_qty }}</span></template
                  >
                  <template v-else>
                    <span v-tooltip="'Current stock is below minimum stock quantity or exhausted'" style="color: orange"
                      >{{ slotProps.data.stock_qty }} <i class="pi pi-circle-fill"></i
                    ></span>
                  </template>
                </template>
                <template #filter="{ filterModel, filterCallback }">
                  <InputNumber
                    v-model="filterModel.value"
                    v-tooltip.top.focus="'Hit enter key to filter'"
                    class="p-column-filter"
                    placeholder="qty"
                    @keydown.enter="filterCallback()" />
                </template>
              </Column>
              <Column header="Min" :sortable="true" field="stock_qty_min" data-type="numeric">
                <template #body="slotProps">
                  <span>{{ slotProps.data.stock_qty_min }}</span>
                </template></Column
              >
              <Column header="Unit" :sortable="true" field="part_unit.name">
                <template #body="slotProps">{{
                  slotProps.data.part_unit && slotProps.data.part_unit.name ? slotProps.data.part_unit.name : "-"
                }}</template>
              </Column>
              <Column header="Footprint" :sortable="true" field="footprint_id" :filter-match-mode-options="matchModes.footprint">
                <template #body="slotProps">
                  <span
                    v-tooltip="{
                      value: slotProps.data.footprint ? slotProps.data.footprint.description : '',
                      disabled: false,
                    }">
                    {{ slotProps.data.footprint ? slotProps.data.footprint.name : "-" }}
                  </span>
                </template>
                <template #filter="{ filterModel, filterCallback }">
                  <Dropdown
                    v-model="filterModel.value"
                    class="p-column-filter"
                    placeholder="Search by footprint"
                    :options="choicesFootprintWithNo"
                    option-label="name"
                    option-value="id"
                    option-group-label="category"
                    option-group-children="footprints"
                    :filter="true"
                    @change="filterCallback()" />
                </template>
              </Column>
            </DataTable>
          </TabPanel>
          <!-- Thumbnails -->
          <TabPanel value="1">
            <div class="grid">
              <div v-for="part in parts" :key="part.id" class="col-4">
                <Card class="product-grid-item">
                  <template #content>
                    <div class="product-grid-item-top">
                      <div>
                        <span class="product-category">{{ part.category ? part.category.name : "Uncategorized" }}</span>
                      </div>
                      <span
                        >qty:
                        <template v-if="part.stock_qty >= part.stock_qty_min"
                          ><span>{{ part.stock_qty }}</span></template
                        >
                        <template v-else>
                          <span v-tooltip="'Current stock is below minimum stock quantity or exhausted'" style="color: orange"
                            >{{ part.stock_qty }} <i class="pi pi-circle-fill"></i
                          ></span>
                        </template>
                      </span>
                    </div>
                    <div class="product-grid-item-content mt-3">
                      <template v-if="partGetDefaultAttachment(part.part_attachments)">
                        <PvImage preview :src="partGetDefaultAttachment(part.part_attachments).picture_medium" :alt="part.name" width="250" />
                      </template>
                      <template v-else>
                        <i class="pi pi-microchip mb-5 mt-5" style="font-size: 2.5rem" />
                      </template>

                      <div class="product-name">{{ part.name }}</div>
                      <div class="product-description">
                        {{ part.description }}
                      </div>
                      <div class="product-button">
                        <PvButton label="View details" @click.prevent="viewPartModal(part)"></PvButton>
                      </div>
                    </div>
                  </template>
                </Card>
              </div>
            </div>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { useServerStore } from "@/stores/server";
import { mapState } from "pinia";
import apiService from "@/services/api/api.service";
import logger from "@/logging";
import { FilterMatchMode } from "@primevue/core/api";
import { cloneDeep } from "lodash";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import PartViewModal from "@/components/parts/view.vue";
import { h } from "vue";
import Button from "primevue/button";

export default {
  data: () => ({
    loading: true,
    lazyParams: {},
    parts: [],
    totalRecords: 0,
    matchModes: {
      name: [
        { label: "Starts with", value: FilterMatchMode.STARTS_WITH },
        { label: "Contains", value: FilterMatchMode.CONTAINS },
        { label: "Not contains", value: FilterMatchMode.NOT_CONTAINS },
        { label: "Ends with", value: FilterMatchMode.ENDS_WITH },
        { label: "Equals", value: FilterMatchMode.EQUALS },
        { label: "Not equals", value: FilterMatchMode.NOT_EQUALS },
      ],
      storage: [
        { label: "Equals", value: FilterMatchMode.EQUALS },
        { label: "Not equals", value: FilterMatchMode.NOT_EQUALS },
      ],
      qty: [
        { label: "Equals", value: FilterMatchMode.EQUALS },
        { label: "Less than", value: FilterMatchMode.LESS_THAN },
        {
          label: "Less than or equal to",
          value: FilterMatchMode.LESS_THAN_OR_EQUAL_TO,
        },
        { label: "Greater than", value: FilterMatchMode.GREATER_THAN },
        {
          label: "Greater than or equal to",
          value: FilterMatchMode.GREATER_THAN_OR_EQUAL_TO,
        },
      ],
      footprint: [
        { label: "Equals", value: FilterMatchMode.EQUALS },
        { label: "Not equals", value: FilterMatchMode.NOT_EQUALS },
      ],
    },
    // Note: this is duplicated in watch: categoryId()
    filters: {
      name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
      storage_id: { value: null, matchMode: FilterMatchMode.EQUALS },
      stock_qty: { value: null, matchMode: FilterMatchMode.EQUALS },
      footprint_id: { value: null, matchMode: FilterMatchMode.EQUALS },
    },
  }),
  computed: {
    ...mapState(usePreloadsStore, {
      categories: (store) => [store.categories],
      currentCategory: (store) => store.currentCategory,
      choicesStorageLocation: (store) => {
        const cb = (e) => {
          // base object
          let obj = {
            key: e.uuid ? e.id : `cat-${e.id}`,
            label: e.name,
            icon: e.uuid ? `pi pi-folder-open` : `pi pi-home`,
          };
          if (e.children) {
            obj["children"] = e.children.map(cb);
          }
          // return obj
          return obj;
        };
        return store.storages.map(cb);
      },
      choicesFootprint: (store) =>
        store.footprints.map((x) => {
          return {
            category: x.name,
            footprints: x.footprint_set.map((y) => {
              return { id: y.id, name: y.name };
            }),
          };
        }),
      choicesCategory: (store) => {
        const cb = (e) => {
          // base object
          let obj = {
            key: e.id,
            label: e.name,
            icon: `pi pi-folder`,
          };
          obj["selectable"] = true;
          obj["children"] = e.children.map(cb);
          return obj;
        };
        return [store.categories].map(cb);
      },
    }),
    ...mapState(useServerStore, {
      perPage: (store) => store.settings.pagination.PARTS || 10,
    }),
    choicesFootprintWithNo() {
      return [
        {
          category: "No footprint",
          footprints: [{ id: 0, name: "No footprint" }],
        },
      ].concat(this.choicesFootprint);
    },
    choicesStorageLocationWithNo() {
      return [{ key: "0", label: "No Storage Location", icon: "pi pi-times" }].concat(this.choicesStorageLocation);
    },
    searchQuery() {
      return this.$route.query.q;
    },
    breadcrumb() {
      if (this.actualCurrentCategory && this.categoryId && this.categoryId !== "0") {
        return {
          home: {
            icon: "pi pi-folder mr-1",
            command: () => {
              this.$router.push({ name: "home" });
            },
            label: "Public parts by category",
          },
          items: [
            {
              label: this.actualCurrentCategory.name,
              command: () => {
                this.$router.push({
                  name: "public-parts-category-list",
                  params: { categoryId: this.actualCurrentCategory.id },
                });
              },
            },
          ],
        };
      } else if (this.categoryId && this.categoryId == 0) {
        return {
          home: {
            icon: "pi pi-folder mr-1",
            command: () => {
              this.$router.push({
                name: "public-parts-category-list",
                params: { categoryId: this.actualCurrentCategory.id },
              });
            },
            label: "Uncategorized public parts",
          },
        };
      } else {
        return {
          home: {
            icon: "pi pi-folder mr-1",
            command: () => {
              this.$router.push({ name: "public-parts" });
            },
            label: "All public parts",
          },
        };
      }
    },
    categoryId() {
      return this.$route.params.categoryId;
    },
    actualCurrentCategory() {
      return this.currentCategory;
    },
    storageId() {
      return this.$route.query.storage;
    },
    storageUuid() {
      return this.$route.query.storage_uuid;
    },
  },
  watch: {
    categoryId: function () {
      // Reset filters
      this.filters.name.value = null;
      this.filters.storage_id.value = null;
      this.filters.stock_qty.value = null;
      this.filters.footprint_id.value = null;
      // Also delete search term from lazyParams object
      delete this.lazyParams.search;

      this.categoryChanged();
      this.loadLazyData();
    },
    searchQuery: function () {
      // define search param
      this.lazyParams.search = this.searchQuery;
      // delete category_id
      delete this.lazyParams.category_id;

      // reload
      this.loadLazyData();
    },
    "lazyParams.sellable": function () {
      if (!this.lazyParams.sellable) {
        delete this.lazyParams.sellable;
      }
      // reload after toggle
      this.loadLazyData();
    },
  },
  setup: () => ({
    preloadsStore: usePreloadsStore(),
    serverStore: useServerStore(),
    confirm: useConfirm(),
    toast: useToast(),
  }),
  created() {},
  mounted() {
    this.lazyParams = {
      first: 0,
      rows: this.$refs.dt.rows,
      sortField: null,
      sortOrder: null,
      filters: this.filters,
    };

    this.$nextTick(() => {
      if (this.searchQuery) {
        logger.default.info("mounted(): search query");
        this.lazyParams.search = this.searchQuery;
        this.loadLazyData();
      } else if (this.storageUuid) {
        logger.default.info("mounted(): storage UUID");
        this.lazyParams.storageUuid = this.storageUuid;
        this.loadLazyData();
      } else {
        logger.default.info("mounted(): default");
        this.categoryChanged();
        this.loadLazyData();
      }
    });
  },
  methods: {
    categoryChanged() {
      // on mount() we set the current category in the store
      // instead of setting from the tree/node, so that way we get the
      // category name even on direct access (otherwise we would only have the ID)
      // if we have a 0 category (uncategorized)
      if (!this.categoryId || Number(this.categoryId) === 0) {
        this.preloadsStore.setCurrentCategory({
          id: this.categoryId,
          name: "none",
        });
        // set the lazy params field
        this.lazyParams.category_id = this.categoryId;
        return;
      }

      // Else it is an existing category
      let curCat = null;
      const cb = (e) => {
        if (e.id === Number(this.categoryId)) {
          curCat = e;
        }
        e.children.forEach(cb);
      };
      // we cycle over all categories to find the name too
      this.categories.forEach(cb);
      this.preloadsStore.setCurrentCategory({
        id: this.categoryId,
        name: curCat.name,
      });

      // set the lazy params field
      this.lazyParams.category_id = this.categoryId;
    },
    loadLazyData() {
      this.loading = true;

      // Do a quick cleanup of datas before sending them
      const params = cloneDeep(this.lazyParams);
      if (params.filters["storage_id"].value) {
        params.filters["storage_id"].value = Object.keys(params.filters["storage_id"].value)[0];
      }

      apiService
        .getPublicParts(params)
        .then((res) => {
          this.parts = res.data.results;
          this.totalRecords = res.data.count;
          this.loading = false;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Parts loading",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with parts loading", err);
        });
    },
    qrcodeId(id, size) {
      return size ? `qrcode-${id}-${size}` : `qrcode-${id}`;
    },
    qrCodePart(uuid) {
      return `web+stockazio:part,${uuid}`;
    },
    partGetDefaultAttachment(attachments) {
      // If only one attachment, and it is a picture, elect as default
      if (attachments.length === 1 && attachments[0].picture) {
        return attachments[0];
      }

      // Else return the one marked as default
      let att = attachments.filter((x) => {
        if (x.picture_default) {
          return x;
        }
      })[0]; // return first item
      if (att) {
        return att;
      }

      // Else return first attachment being an image
      return attachments.filter((x) => {
        if (x.picture) {
          return x;
        }
      })[0]; // return first item
    },
    viewPartModal(part) {
      // Get full part object infos
      apiService
        .getPublicPart(part.id)
        .then((val) => {
          const viewPartRef = this.$dialog.open(PartViewModal, {
            props: {
              modal: true,
              style: {
                width: "70vw",
              },
              dismissableMask: true,
            },
            templates: {
              header: () => {
                if (part.private) {
                  return [h("h3", [h("i", { class: "pi pi-lock mr-1" }), h("span", part.name)])];
                } else {
                  return [h("h3", part.name)];
                }
              },
              footer: () => {
                return [
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
    toggleOverlayPanel(event, ref) {
      this.$refs[ref].toggle(event);
    },
    onPage(event) {
      this.lazyParams = event;
      this.loadLazyData();
    },
    onSort(event) {
      this.lazyParams = event;
      this.loadLazyData();
    },
    onFilter(event) {
      this.lazyParams.filters = this.filters;
      this.loadLazyData();
    },
  },
};
</script>

<style lang="scss" scoped>
.product-name {
  font-size: 1.5rem;
  font-weight: 700;
}

.product-description {
  margin: 0 0 1rem 0;
}

.product-category {
  font-weight: 600;
  vertical-align: middle;
}

::v-deep(.product-grid-item) {
  margin: 0.5rem;
  border: 1px solid var(--surface-border);

  .product-grid-item-top,
  .product-grid-item-bottom {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .product-grid-item-content {
    text-align: center;
  }
}
</style>
