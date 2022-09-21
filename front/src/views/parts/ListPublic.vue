<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <div class="card ml-5 mt-4">
      <TabView>
        <TabPanel>
          <template #header>
            <i class="fa fa-table mr-2"></i><span>Table</span>
          </template>
          <DataTable
            :value="parts"
            :lazy="true"
            :paginator="true"
            :rows="perPage"
            v-model:filters="filters"
            ref="dt"
            dataKey="id"
            :totalRecords="totalRecords"
            :loading="loading"
            @page="onPage($event)"
            @sort="onSort($event)"
            @filter="onFilter($event)"
            filterDisplay="menu"
            responsiveLayout="scroll"
            stripedRows
            class="p-datatable-sm"
            removableSort
          >
            <template #empty> No parts found. </template>

            <template #header>
              <div class="field-checkbox">
                <Checkbox
                  inputId="only_sellable"
                  v-model="lazyParams.sellable"
                  :binary="true"
                />
                <label for="only_sellable">Only show sellable parts</label>
              </div>
            </template>

            <Column
              header="Name"
              :sortable="true"
              field="name"
              :filterMatchModeOptions="matchModes.name"
            >
              <template #body="slotProps">
                <div>
                  <template
                    v-if="
                      partGetDefaultAttachment(slotProps.data.part_attachments)
                    "
                  >
                    <i
                      :id="`p_a_${slotProps.data.id}`"
                      v-tooltip="'Click to show picture'"
                      class="fa fa-picture-o mr-1"
                      aria-hidden="true"
                      @click="
                        toggleOverlayPanel($event, `p_a_${slotProps.data.id}`)
                      "
                    />
                    <OverlayPanel
                      :ref="`p_a_${slotProps.data.id}`"
                      appendTo="body"
                      :showCloseIcon="true"
                      :id="`p_a_${slotProps.data.id}`"
                    >
                      <Image
                        preview
                        width="250"
                        :src="
                          partGetDefaultAttachment(
                            slotProps.data.part_attachments
                          ).picture_medium
                        "
                      ></Image>
                    </OverlayPanel>
                  </template>
                  <a
                    href="#"
                    class="no-underline"
                    @click.prevent="viewPartModal(slotProps.data)"
                    >{{ slotProps.data.name }}</a
                  >
                  <br />
                  <template v-if="slotProps.data.description">
                    {{
                      slotProps.data.category
                        ? slotProps.data.category.name
                        : "No category"
                    }}: {{ slotProps.data.description }}
                  </template>
                  <template v-else>
                    {{
                      slotProps.data.category
                        ? slotProps.data.category.name
                        : "No category"
                    }}
                  </template>
                </div>
              </template>
              <template #filter="{ filterModel }">
                <InputText
                  type="text"
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="Search by name"
                />
              </template>
            </Column>
            <Column
              header="Storage"
              :sortable="true"
              field="storage_id"
              :filterMatchModeOptions="matchModes.storage"
            >
              <template #body="slotProps">{{
                slotProps.data.storage && slotProps.data.storage.name
                  ? slotProps.data.storage.name
                  : "-"
              }}</template>
              <template #filter="{ filterModel }">
                <TreeSelect
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="Search by storage"
                  :options="choicesStorageLocationWithNo"
                  selectionMode="single"
                />
              </template>
            </Column>
            <Column
              header="Stock"
              :sortable="true"
              field="stock_qty"
              dataType="numeric"
              :filterMatchModeOptions="matchModes.qty"
            >
              <template #body="slotProps">
                <template
                  v-if="
                    slotProps.data.stock_qty >= slotProps.data.stock_qty_min
                  "
                  ><span>{{ slotProps.data.stock_qty }}</span></template
                >
                <template v-else>
                  <span
                    class="text-red-500"
                    v-tooltip="
                      'Current stock is below minimum stock quantity or exhausted'
                    "
                    >{{ slotProps.data.stock_qty }} <i class="fa fa-circle"></i
                  ></span>
                </template>
              </template>
              <template #filter="{ filterModel }">
                <InputNumber
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="qty"
                />
              </template>
            </Column>
            <Column
              header="Min"
              :sortable="true"
              field="stock_qty_min"
              dataType="numeric"
            >
              <template #body="slotProps">
                <span>{{ slotProps.data.stock_qty_min }}</span>
              </template></Column
            >
            <Column header="Unit" :sortable="true" field="part_unit.name">
              <template #body="slotProps">{{
                slotProps.data.part_unit && slotProps.data.part_unit.name
                  ? slotProps.data.part_unit.name
                  : "-"
              }}</template>
            </Column>
            <Column
              header="Footprint"
              :sortable="true"
              field="footprint_id"
              :filterMatchModeOptions="matchModes.footprint"
            >
              <template #body="slotProps">
                <span
                  v-tooltip="{
                    value: slotProps.data.footprint
                      ? slotProps.data.footprint.description
                      : '',
                    disabled: false,
                  }"
                >
                  {{
                    slotProps.data.footprint
                      ? slotProps.data.footprint.name
                      : "-"
                  }}
                </span>
              </template>
              <template #filter="{ filterModel }">
                <Dropdown
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="Search by footprint"
                  :options="choicesFootprintWithNo"
                  optionLabel="name"
                  optionValue="id"
                  optionGroupLabel="category"
                  optionGroupChildren="footprints"
                  :filter="true"
                />
              </template>
            </Column>
          </DataTable>
        </TabPanel>
        <TabPanel>
          <template #header>
            <i class="fa fa-image mr-2"></i> <span>Thumbnails</span>
          </template>
          <div class="grid">
            <div class="col-2" v-for="part in parts" :key="part.id">
              <Card :title="part.name">
                <template #title>
                  {{ part.name }}
                </template>
                <template #content>
                  <div class="mb-1 text-sm">
                    {{ part.description || "No description." }}
                  </div>

                  <div class="flex justify-content-center">
                    <div
                      class="flex flex-grow-1 align-items-center justify-content-center"
                    >
                      <div class="field w-6">
                        <template
                          v-if="partGetDefaultAttachment(part.part_attachments)"
                        >
                          <Image
                            preview
                            width="150"
                            :src="
                              partGetDefaultAttachment(part.part_attachments)
                                .picture_medium
                            "
                          ></Image>
                        </template>

                        <template v-else>
                          <span class="fa-stack fa-5x">
                            <i class="fa fa-file-picture-o fa-stack-2x" />
                            <i
                              class="fa fa-question fa-stack-1x text-orange-400"
                            />
                          </span>
                        </template>
                      </div>
                    </div>
                  </div>
                </template>
                <template #footer>
                  <div class="text-center">
                    <div class="text-sm">qty: {{ part.stock_qty }}</div>
                    <Button
                      class="p-button-outlined mt-1"
                      label="View details"
                      @click.prevent="viewPartModal(slotProps.data)"
                    ></Button>
                  </div>
                </template>
              </Card>
            </div>
          </div>
        </TabPanel>
      </TabView>
    </div>
  </div>
</template>

<script>
import { usePreloadsStore } from "@/stores/preloads";
import { useServerStore } from "../../stores/server";
import { mapState } from "pinia";
import apiService from "@/services/api/api.service";
import logger from "@/logging";
import { FilterMatchMode } from "primevue/api";
import utils from "@/utils.js";
import { cloneDeep, chunk } from "lodash";
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
            icon: e.uuid ? `fa fa-folder-open` : `fa fa-home`,
          };
          // Selectable only if no locations
          obj["selectable"] = e.storage_locations ? false : true;
          // Merge children with storage_locations
          if (e.storage_locations && e.children) {
            obj["children"] = e.children.concat(e.storage_locations).map(cb);
          }
          // return obj
          return obj;
        };
        return store.storages.filter(utils.removeStorageCatWithoutLocs).map(cb);
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
            icon: `fa fa-folder-o`,
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
      return [
        { key: "0", label: "No Storage Location", icon: "fa fa-close" },
      ].concat(this.choicesStorageLocation);
    },
    searchQuery() {
      return this.$route.query.q;
    },
    breadcrumb() {
      if (
        this.actualCurrentCategory &&
        this.categoryId &&
        this.categoryId !== "0"
      ) {
        return {
          home: {
            icon: "fa fa-folder-o mr-1",
            to: "/",
            label: "Public parts by category",
          },
          items: [
            {
              label: this.actualCurrentCategory.name,
              to: {
                name: "public-parts-category-list",
                params: { categoryId: this.actualCurrentCategory.id },
              },
            },
          ],
        };
      } else if (this.categoryId && this.categoryId == 0) {
        return {
          home: {
            icon: "fa fa-folder-o mr-1",
            to: {
              name: "public-parts-category-list",
              params: { categoryId: this.actualCurrentCategory.id },
            },
            label: "Uncategorized public parts",
          },
        };
      } else {
        return {
          home: {
            icon: "fa fa-folder-o mr-1",
            to: { name: "public-parts" },
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
    thumbnailsChunked() {
      return chunk(this.parts, 6);
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
        params.filters["storage_id"].value = Object.keys(
          params.filters["storage_id"].value
        )[0];
      }

      apiService.getPublicParts(params).then((res) => {
        this.parts = res.data.results;
        this.totalRecords = res.data.count;
        this.loading = false;
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
            },
            templates: {
              header: () => {
                if (part.private) {
                  return [
                    h("h3", [
                      h("i", { class: "fa fa-lock mr-1" }),
                      h("span", part.name),
                    ]),
                  ];
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
