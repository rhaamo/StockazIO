<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <Card v-if="show_parameters_filter" class="ml-5 mt-4 pt-2 mr-5">
      <template #title>Filtering by part parameter</template>
      <template #content>
        <div v-for="(_, i) in parameters_filters" :key="i">
          <ParameterFilter
            v-model:item="parameters_filters[i]"
            v-model:names="parameters_filter_names"
            @deleteItem="deletePartParameterFilter($event, i)" />
        </div>

        <Divider />

        <PvButton class="p-button-help" label="add filter" @click.prevent="addPartParameterFilter($event)" />

        <PvButton
          v-if="parameters_filters && parameters_filters.length"
          class="p-button-success ml-2"
          label="search parts"
          @click.prevent="searchPartsFilter($event)" />
      </template>
    </Card>

    <div class="mt-4 pl-0 pr-0 pt-0 pb-0">
      <TabView>
        <TabPanel>
          <template #header> <i class="pi pi-table mr-2"></i><span>Table</span> </template>
          <DataTable
            ref="dt"
            v-model:filters="filters"
            :value="parts"
            :lazy="true"
            :paginator="true"
            :rows="perPage"
            v-model:selection="selectedParts"
            data-key="id"
            :total-records="totalRecords"
            :loading="loading"
            filter-display="row"
            responsive-layout="scroll"
            :select-all="selectAll"
            striped-rows
            class="p-datatable-sm"
            removable-sort
            :show-filter-operator="false"
            @page="onPage($event)"
            @sort="onSort($event)"
            @filter="onFilter($event)"
            @select-all-change="onSelectAllChange"
            @row-select="onRowSelect"
            @row-unselect="onRowUnselect">
            <template #empty> No parts found. </template>

            <template #header>
              <template v-if="selectedParts && selectedParts.length">
                <PvButton label="Change category" class="p-button-info" @click="toggleOverlayPanel($event, 'btnChangeCat')" />
                <OverlayPanel ref="btnChangeCat">
                  <TreeSelect
                    v-model="bulkEditCategory"
                    input-id="category"
                    placeholder="Film resistors ? MCUs ?"
                    :options="choicesCategory"
                    selection-mode="single" />
                  <PvButton label="Save" class="ml-1" @click="bulkChangeCategory($event)"></PvButton>
                </OverlayPanel>

                <PvButton label="Change location" class="p-button-help ml-2" @click="toggleOverlayPanel($event, 'btnChangeLoc')" />
                <OverlayPanel ref="btnChangeLoc">
                  <TreeSelect
                    v-model="bulkEditStorage"
                    class="p-column-filter"
                    placeholder="Select storage"
                    :options="choicesStorageLocation"
                    selection-mode="single" />
                  <PvButton label="Save" class="ml-1" @click="bulkChangeStorageLocation($event)"></PvButton>
                </OverlayPanel>

                <PvButton label="Generate labels" class="p-button-normal ml-2" @click="showBulkLabelGenerator()" />

                <PvButton label="Delete" class="p-button-danger ml-2" @click="deletePartMultiple($event)" />
              </template>

              <template v-else>
                <div class="flex items-center gap-4">
                  <div>
                    <Checkbox v-model="filter_qty_min" input-id="only_qty_less_min" :binary="true" />
                    <label for="only_qty_less_min"> Only qty &lt; min</label>
                  </div>
                  <div>
                    <Checkbox v-model="filter_qty_zero" input-id="only_qty_zero" :binary="true" />
                    <label for="only_qty_zero"> Qty out of stock</label>
                  </div>
                  <div>
                    <Checkbox v-model="show_parameters_filter" input-id="show_parameters_filter" :binary="true" />
                    <label for="show_parameters_filter"> Parameters Filtering</label>
                  </div>
                </div>
              </template>
            </template>

            <Column selection-mode="multiple" header-style="width: 3em"></Column>
            <Column :sortable="false">
              <template #body="slotProps">
                <div @click="showLabelGenerator(slotProps.data)">
                  <vue-qrcode
                    :id="qrcodeId(slotProps.data.id)"
                    v-tooltip="'show label generator'"
                    :value="qrCodePart(slotProps.data.uuid)"
                    :options="{
                      scale: 1,
                      color: { dark: '#000000', light: '#FFFFFF' },
                    }"
                    :data-uuid="slotProps.data.uuid"
                    :data-name="slotProps.data.name"
                    data-toggle="modal"
                    data-target="#modalQrCode" />
                </div>
              </template>
            </Column>
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
                    <OverlayPanel :id="`p_a_${slotProps.data.id}`" :ref="`p_a_${slotProps.data.id}`" append-to="body" :show-close-icon="true">
                      <PvImage preview width="250" :src="partGetDefaultAttachment(slotProps.data.part_attachments).picture_medium"></PvImage>
                    </OverlayPanel>
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
              <template #body="slotProps">
                <template v-if="slotProps.data.storage && slotProps.data.storage.name">
                  {{ slotProps.data.storage_path.join(" / ") }}
                </template>
                <template v-else>-</template>
              </template>
              <template #filter="{ filterModel, filterCallback }">
                <TreeSelect
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="Search by storage"
                  :options="choicesStorageLocationWithNo"
                  selection-mode="single"
                  fluid
                  @change="filterCallback()" />
              </template>
            </Column>
            <Column
              header="In stock"
              :sortable="true"
              field="stock_qty"
              data-type="numeric"
              :filter-match-mode-options="matchModes.qty"
              header-style="width: 10rem">
              <template #body="slotProps">
                <QuantityPopoverEditor :part="slotProps.data" kind="qty" size="" />
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
            <Column header="Min" :sortable="true" field="stock_qty_min" data-type="numeric" header-style="width: 10rem">
              <template #body="slotProps">
                <QuantityPopoverEditor :part="slotProps.data" kind="qty_min" size="" />
              </template>
            </Column>
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
                  fluid
                  @change="filterCallback()" />
              </template>
            </Column>
            <Column :sortable="false" header-style="min-width: 6.3em">
              <template #body="slotProps">
                <ButtonsEditDelete @edit="editPart($event, slotProps.data)" @delete="deletePart($event, slotProps.data)" />
              </template>
            </Column>
          </DataTable>

          <Popover ref="poQty">
            <label
              for="qty"
              :class="{
                'pb-3': true,
                block: true,
              }"
              >Change quantity from {{ selectedPartMode === "qty" ? selectedPart.oldQty : selectedPart.oldQtyMin }} to:</label
            >
            <div v-if="selectedPartMode === 'qty'" class="flex gap-2">
              <InputNumber v-model="selectedPart.stock_qty" input-id="qty" mode="decimal" show-buttons button-layout="horizontal" :min="0" />
              <PvButton label="save" severity="success" @click.prevent="updateInplaceBothQty($event)" />
            </div>
            <div v-else class="flex gap-2">
              <InputNumber v-model="selectedPart.stock_qty_min" input-id="qty" mode="decimal" show-buttons button-layout="horizontal" :min="0" />
              <PvButton label="save" severity="success" @click.prevent="updateInplaceBothQty($event)" />
            </div>

            <InputGroup class="mt-3">
              <PvButton label="-10" severity="success" size="small" @click.prevent="updateSelectedPartQty(-10)" />
              <PvButton label="-50" severity="info" size="small" @click.prevent="updateSelectedPartQty(-50)" />
              <PvButton label="-100" severity="help" size="small" @click.prevent="updateSelectedPartQty(-100)" />
              <PvButton disabled severity="secondary" size="small" />
              <PvButton label="+100" severity="help" size="small" @click.prevent="updateSelectedPartQty(+100)" />
              <PvButton label="+50" severity="info" size="small" @click.prevent="updateSelectedPartQty(+50)" />
              <PvButton label="+10" severity="success" size="small" @click.prevent="updateSelectedPartQty(+10)" />
            </InputGroup>
          </Popover>
        </TabPanel>

        <TabPanel>
          <template #header> <i class="pi pi-image mr-2"></i> <span>Thumbnails</span> </template>

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
      </TabView>
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
import LabelGeneratorModal from "@/components/label/generator.vue";
import ParameterFilter from "@/components/parts/ParameterFilter.vue";
import { h } from "vue";
import Button from "primevue/button";
import QuantityPopoverEditor from "@/components/parts/QuantityPopoverEditor.vue";
import ButtonsEditDelete from "@/components/btn_edit_delete.vue";

export default {
  components: {
    ParameterFilter,
    QuantityPopoverEditor,
    ButtonsEditDelete,
  },
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
      name: {
        value: null,
        matchMode: FilterMatchMode.STARTS_WITH,
      },
      storage_id: {
        value: null,
        matchMode: FilterMatchMode.EQUALS,
      },
      stock_qty: {
        value: null,
        matchMode: FilterMatchMode.EQUALS,
      },
      footprint_id: {
        value: null,
        matchMode: FilterMatchMode.EQUALS,
      },
    },
    selectAll: false,
    selectedParts: null,
    bulkEditStorage: null,
    bulkEditCategory: null,
    filter_qty_min: false,
    filter_qty_zero: false,
    show_parameters_filter: false,
    parameters_filter_names: [],
    parameters_filters: [],
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
            label: "Parts by category",
          },
          items: [
            {
              label: this.actualCurrentCategory.name,
              command: () => {
                this.$router.push({
                  name: "parts-category-list",
                  params: {
                    categoryId: this.actualCurrentCategory.id || this.categoryId,
                  },
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
                name: "parts-category-list",
                params: {
                  categoryId: this.actualCurrentCategory.id || this.categoryId,
                },
              });
            },
            label: "Uncategorized parts",
          },
        };
      } else {
        return {
          home: {
            icon: "pi pi-folder mr-1",
            command: () => {
              this.$router.push({ name: "parts-list" });
            },
            label: "All parts",
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
    filter_qty_min: function () {
      if (this.filter_qty_min) {
        this.lazyParams.qtyType = "qtyMin";
      } else {
        delete this.lazyParams.qtyType;
      }
      this.loadLazyData();
    },
    filter_qty_zero: function () {
      if (this.filter_qty_zero) {
        // AAA
        this.lazyParams.qtyType = "qtyZero";
      } else {
        // AAA
        delete this.lazyParams.qtyType;
      }
      this.loadLazyData();
    },
    show_parameters_filter: function () {
      if (this.show_parameters_filter) {
        this.loadPartParametersNames();
      } else {
        this.parameters_filters = [];
        delete this.lazyParams.parameter_filters;
        this.loadLazyData();
      }
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
      let params = cloneDeep(this.lazyParams);
      if (params.filters["storage_id"].value) {
        params.filters["storage_id"].value = Object.keys(params.filters["storage_id"].value)[0];
      }

      apiService
        .getParts(params)
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
    loadPartParametersNames() {
      apiService
        .getPartParametersAllNames()
        .then((res) => {
          this.parameters_filter_names = res.data;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Parts parameters names",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with parts parameters names", err);
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
                  return [h("h1", [h("i", { class: "pi pi-lock mr-1" }), h("span", part.name)])];
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
              readonly: false,
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
            return [h("h3", [h("i", { class: "pi pi-qrcode mr-1" }), h("span", "Label Generator")])];
          },
        },
        data: {
          items: [item],
          kind: "part",
        },
      });
    },
    toggleOverlayPanel(event, ref) {
      this.$refs[ref].toggle(event);
    },
    onPage(event) {
      this.lazyParams = event;
      this.loadLazyData();
    },
    onPageDV(event) {
      this.lazyParams.first = event.first;
      this.lazyParams.rows = event.rows;
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
    onSelectAllChange(event) {
      const selectAll = event.checked;

      if (selectAll) {
        this.selectAll = true;
        this.selectedParts = cloneDeep(this.parts);
      } else {
        this.selectAll = false;
        this.selectedParts = [];
      }
    },
    onRowSelect() {
      this.selectAll = this.selectedParts.length === this.totalRecords;
    },
    onRowUnselect() {
      this.selectAll = false;
    },
    editPart(event, part) {
      this.$router.push({
        name: "parts-edit",
        params: { partId: part.id },
      });
    },
    deletePart(event, part) {
      this.confirm.require({
        message: `Are you sure you want to delete the part '${part.name}' ?`,
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
            .deletePart(part.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Deleting part",
                detail: "Success",
                life: 5000,
              });
              this.loadLazyData();
              this.preloadsStore.decrementCategoryPartsCount(this.categoryId);
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Deleting part",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part deletion", err);
              this.loadLazyData();
            });
        },
        reject: () => {
          return;
        },
      });
    },
    deletePartMultiple(event) {
      this.confirm.require({
        message: `Are you sure you want to delete all the selected parts ?`,
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
          const _bulkDelete = async (parts) => {
            for (let part of parts) {
              logger.default.info("delete part", part.name);
              await apiService
                .deletePart(part.id)
                .then((val) => {
                  this.toast.add({
                    severity: "success",
                    summary: `Deleting ${part.name}`,
                    detail: "Success",
                    life: 5000,
                  });
                  this.preloadsStore.decrementCategoryPartsCount(this.categoryId);
                })
                .catch((err) => {
                  this.toast.add({
                    severity: "error",
                    summary: `Deleting ${part.name}`,
                    detail: "An error occured, please try again later",
                    life: 5000,
                  });
                  logger.default.error("Error with part deletion", err);
                });
            }
          };

          _bulkDelete(this.selectedParts).then(() => {
            logger.default.info("reload");
            this.selectedParts = [];
            this.loadLazyData();
          });
        },
        reject: () => {
          return;
        },
      });
    },
    bulkChangeStorageLocation(event) {
      let ids = this.selectedParts.map((x) => {
        return x.id;
      });
      let storageId = Object.keys(this.bulkEditStorage)[0];

      apiService
        .changePartsStorageLocation(ids, storageId)
        .then((val) => {
          this.toast.add({
            severity: "success",
            summary: `Updating parts`,
            detail: "Success",
            life: 5000,
          });
          this.$nextTick(() => {
            this.bulkEditStorage = null;
            this.toggleOverlayPanel(event, "btnChangeLoc");
            this.loadLazyData();
          });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: `Updating parts`,
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with storage part update", err);
          this.bulkEditStorage = null;
          this.toggleOverlayPanel(event, "btnChangeLoc");
          this.selectedParts = null;
          this.loadLazyData();
        });
    },
    bulkChangeCategory(event) {
      let ids = this.selectedParts.map((x) => {
        return x.id;
      });
      let categoryId = Object.keys(this.bulkEditCategory)[0];

      apiService
        .changePartsCategory(ids, categoryId)
        .then((val) => {
          this.toast.add({
            severity: "success",
            summary: `Updating parts`,
            detail: "Success",
            life: 5000,
          });
          this.$nextTick(() => {
            this.bulkEditCategory = null;
            this.toggleOverlayPanel(event, "btnChangeCat");
            for (let part of this.selectedParts) {
              this.preloadsStore.decrementCategoryPartsCount(part.category.id, ids.length);
              this.preloadsStore.incrementCategoryPartsCount(categoryId, ids.length);
            }
            this.selectedParts = null;
            this.loadLazyData();
          });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: `Updating parts`,
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with category part update", err);
          this.bulkEditCategory = null;
          this.toggleOverlayPanel(event, "btnChangeCat");
          this.loadLazyData();
        });
    },
    addPartParameterFilter(event) {
      this.parameters_filters.push({
        name: "",
        mode: "",
        value: "",
      });
    },
    deletePartParameterFilter(event, idx) {
      this.parameters_filters.splice(idx, 1);
    },
    searchPartsFilter(event) {
      this.loading = true;
      this.lazyParams.parameter_filters = this.parameters_filters.map((x) => {
        return { name: x.name.value, matchMode: x.mode.value, value: x.value };
      });
      this.loadLazyData();
    },
    showBulkLabelGenerator() {
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
            return [h("h3", [h("i", { class: "pi pi-qrcode mr-1" }), h("span", "Label Generator")])];
          },
        },
        data: {
          items: this.selectedParts,
          kind: "part",
        },
      });
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
  border: 1px solid black;

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
