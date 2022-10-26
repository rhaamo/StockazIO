<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <div class="card ml-5 mt-4 pt-2" v-if="show_parameters_filter">
      <h4>Filtering by part parameter</h4>

      <div v-for="(_, i) in parameters_filters" :key="i">
        <ParameterFilter
          v-model:item="parameters_filters[i]"
          v-model:names="parameters_filter_names"
          @deleteItem="deletePartParameterFilter($event, i)"
        />
      </div>

      <Divider />

      <PvButton
        @click.prevent="addPartParameterFilter($event)"
        class="p-button-help"
        label="add filter"
      />

      <PvButton
        @click.prevent="searchPartsFilter($event)"
        class="p-button-success ml-2"
        label="search parts"
        v-if="parameters_filters && parameters_filters.length"
      />
    </div>

    <div class="card ml-5 mt-4 pl-0 pr-0 pt-0">
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
            filterDisplay="row"
            responsiveLayout="scroll"
            v-model:selection="selectedParts"
            :selectAll="selectAll"
            @select-all-change="onSelectAllChange"
            @row-select="onRowSelect"
            @row-unselect="onRowUnselect"
            stripedRows
            class="p-datatable-sm"
            removableSort
            :showFilterOperator="false"
          >
            <template #empty> No parts found. </template>

            <template #header>
              <template v-if="selectedParts && selectedParts.length">
                <PvButton
                  label="Change category"
                  class="p-button-info"
                  @click="toggleOverlayPanel($event, 'btnChangeCat')"
                />
                <OverlayPanel ref="btnChangeCat">
                  <TreeSelect
                    inputId="category"
                    placeholder="Film resistors ? MCUs ?"
                    v-model="bulkEditCategory"
                    :options="choicesCategory"
                    selectionMode="single"
                  />
                  <PvButton
                    label="Save"
                    class="ml-1"
                    @click="bulkChangeCategory($event)"
                  ></PvButton>
                </OverlayPanel>

                <PvButton
                  label="Change location"
                  class="p-button-help ml-2"
                  @click="toggleOverlayPanel($event, 'btnChangeLoc')"
                />
                <OverlayPanel ref="btnChangeLoc">
                  <TreeSelect
                    class="p-column-filter"
                    placeholder="Select storage"
                    :options="choicesStorageLocation"
                    selectionMode="single"
                    v-model="bulkEditStorage"
                  />
                  <PvButton
                    label="Save"
                    class="ml-1"
                    @click="bulkChangeStorageLocation($event)"
                  ></PvButton>
                </OverlayPanel>

                <PvButton
                  label="Delete"
                  class="p-button-danger ml-2"
                  @click="deletePartMultiple($event)"
                />
              </template>

              <template v-else>
                <div class="field-checkbox">
                  <Checkbox
                    inputId="only_qty_less_min"
                    v-model="filter_qty_min"
                    :binary="true"
                  />
                  <label for="only_qty_less_min">Only qty &lt; min</label>

                  &nbsp;&nbsp;

                  <Checkbox
                    inputId="show_parameters_filter"
                    v-model="show_parameters_filter"
                    :binary="true"
                  />
                  <label for="show_parameters_filter"
                    >Parameters Filtering</label
                  >
                </div>
              </template>
            </template>

            <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
            <Column :sortable="false">
              <template #body="slotProps">
                <div @click="showLabelGenerator(slotProps.data)">
                  <vue-qrcode
                    :id="qrcodeId(slotProps.data.id)"
                    :value="qrCodePart(slotProps.data.uuid)"
                    :options="{
                      scale: 1,
                      color: { dark: '#000000', light: '#0000' },
                    }"
                    v-tooltip="'show label generator'"
                    :data-uuid="slotProps.data.uuid"
                    :data-name="slotProps.data.name"
                    data-toggle="modal"
                    data-target="#modalQrCode"
                  />
                </div>
              </template>
            </Column>
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
                      <PvImage
                        preview
                        width="250"
                        :src="
                          partGetDefaultAttachment(
                            slotProps.data.part_attachments
                          ).picture_medium
                        "
                      ></PvImage>
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
              <template #filter="{ filterModel, filterCallback }">
                <InputText
                  type="text"
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="Search by name"
                  @keydown.enter="filterCallback()"
                  v-tooltip.top.focus="'Hit enter key to filter'"
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
              <template #filter="{ filterModel, filterCallback }">
                <TreeSelect
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="Search by storage"
                  :options="choicesStorageLocationWithNo"
                  selectionMode="single"
                  @change="filterCallback()"
                />
              </template>
            </Column>
            <Column
              header="Stock"
              :sortable="true"
              field="stock_qty"
              dataType="numeric"
              :filterMatchModeOptions="matchModes.qty"
              headerStyle="width: 15em"
            >
              <template #body="slotProps">
                <Inplace
                  :ref="`inplace_qty_${slotProps.data.id}`"
                  :closable="true"
                >
                  <template
                    #display
                    v-if="
                      slotProps.data.stock_qty >= slotProps.data.stock_qty_min
                    "
                    ><span>{{ slotProps.data.stock_qty }}</span></template
                  >
                  <template #display v-else>
                    <span
                      class="text-red-500"
                      v-tooltip="
                        'Current stock is below minimum stock quantity or exhausted'
                      "
                      >{{ slotProps.data.stock_qty }}
                      <i class="fa fa-circle"></i
                    ></span>
                  </template>
                  <template #content>
                    <InputNumber
                      :inputId="`qty_${slotProps.data.id}`"
                      mode="decimal"
                      showButtons
                      :min="0"
                      v-model="slotProps.data.stock_qty"
                      class="w-3"
                    />
                    <br />
                    <PvButton
                      class="mt-1 mr-1"
                      label="update"
                      @click.prevent="
                        updateInplaceQty(
                          $event,
                          slotProps.data,
                          slotProps.data.stock_qty
                        )
                      "
                    ></PvButton>
                  </template>
                </Inplace>
              </template>
              <template #filter="{ filterModel, filterCallback }">
                <InputNumber
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="qty"
                  @keydown.enter="filterCallback()"
                  v-tooltip.top.focus="'Hit enter key to filter'"
                />
              </template>
            </Column>
            <Column
              header="Min"
              :sortable="true"
              field="stock_qty_min"
              dataType="numeric"
              ><template #body="slotProps">
                <Inplace
                  :ref="`inplace_qty_min_${slotProps.data.id}`"
                  :closable="true"
                >
                  <template #display
                    ><span>{{ slotProps.data.stock_qty_min }}</span></template
                  >
                  <template #content>
                    <InputNumber
                      :inputId="`qty_${slotProps.data.id}`"
                      mode="decimal"
                      showButtons
                      :min="0"
                      v-model="slotProps.data.stock_qty_min"
                      class="w-3"
                    />
                    <br />
                    <PvButton
                      class="mt-1 mr-1"
                      label="update"
                      @click.prevent="
                        updateInplaceQtyMin(
                          $event,
                          slotProps.data,
                          slotProps.data.stock_qty_min
                        )
                      "
                    ></PvButton>
                  </template>
                </Inplace> </template
            ></Column>
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
              <template #filter="{ filterModel, filterCallback }">
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
                  @change="filterCallback()"
                />
              </template>
            </Column>
            <Column :sortable="false" headerStyle="width: 6em"
              ><template #body="slotProps">
                <span class="p-buttonset">
                  <router-link
                    :to="{
                      name: 'parts-edit',
                      params: { partId: slotProps.data.id },
                    }"
                  >
                    <PvButton
                      type="button"
                      icon="fa fa-edit"
                      class="p-button-primary"
                      v-tooltip="'edit'"
                    ></PvButton>
                  </router-link>
                  <PvButton
                    type="button"
                    icon="fa fa-trash-o"
                    class="p-button-danger"
                    v-tooltip="'delete'"
                    @click="deletePart($event, slotProps.data)"
                  ></PvButton>
                </span>
              </template>
            </Column>
          </DataTable>
        </TabPanel>

        <TabPanel>
          <template #header>
            <i class="fa fa-image mr-2"></i> <span>Thumbnails</span>
          </template>

          <div class="grid">
            <div class="col-4" v-for="part in parts" :key="part.id">
              <div class="product-grid-item card">
                <div class="product-grid-item-top">
                  <div>
                    <span class="product-category">{{
                      part.category ? part.category.name : "Uncategorized"
                    }}</span>
                  </div>
                  <span
                    >qty:
                    <template v-if="part.stock_qty >= part.stock_qty_min"
                      ><span>{{ part.stock_qty }}</span></template
                    >
                    <template v-else>
                      <span
                        class="text-red-500"
                        v-tooltip="
                          'Current stock is below minimum stock quantity or exhausted'
                        "
                        >{{ part.stock_qty }} <i class="fa fa-circle"></i
                      ></span>
                    </template>
                  </span>
                </div>
                <div class="product-grid-item-content mt-3">
                  <template
                    v-if="partGetDefaultAttachment(part.part_attachments)"
                  >
                    <PvImage
                      preview
                      :src="
                        partGetDefaultAttachment(part.part_attachments)
                          .picture_medium
                      "
                      :alt="part.name"
                      width="250"
                    />
                  </template>
                  <template v-else>
                    <span class="fa-stack fa-5x">
                      <i class="fa fa-file-picture-o fa-stack-2x" />
                      <i class="fa fa-question fa-stack-1x text-orange-400" />
                    </span>
                  </template>

                  <div class="product-name">{{ part.name }}</div>
                  <div class="product-description">
                    {{ part.description }}
                  </div>
                  <div class="product-button">
                    <PvButton
                      @click.prevent="viewPartModal(part)"
                      label="View details"
                    ></PvButton>
                  </div>
                </div>
              </div>
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
import { FilterMatchMode } from "primevue/api";
import { cloneDeep } from "lodash";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import PartViewModal from "@/components/parts/view.vue";
import LabelGeneratorModal from "@/components/label/generator.vue";
import ParameterFilter from "@/components/parts/ParameterFilter.vue";
import { h } from "vue";
import Button from "primevue/button";

export default {
  components: {
    ParameterFilter,
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
            icon: e.uuid ? `fa fa-folder-open` : `fa fa-home`,
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
            label: "Parts by category",
          },
          items: [
            {
              label: this.actualCurrentCategory.name,
              to: {
                name: "parts-category-list",
                params: {
                  categoryId: this.actualCurrentCategory.id || this.categoryId,
                },
              },
            },
          ],
        };
      } else if (this.categoryId && this.categoryId == 0) {
        return {
          home: {
            icon: "fa fa-folder-o mr-1",
            to: {
              name: "parts-category-list",
              params: {
                categoryId: this.actualCurrentCategory.id || this.categoryId,
              },
            },
            label: "Uncategorized parts",
          },
        };
      } else {
        return {
          home: {
            icon: "fa fa-folder-o mr-1",
            to: { name: "parts-list" },
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
        params.filters["storage_id"].value = Object.keys(
          params.filters["storage_id"].value
        )[0];
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
        },
        templates: {
          header: () => {
            return [
              h("h3", [
                h("i", { class: "fa fa-qrcode mr-1" }),
                h("span", "Label Generator"),
              ]),
            ];
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
    deletePart(event, part) {
      this.confirm.require({
        message: `Are you sure you want to delete the part '${part.name}' ?`,
        header: `Deleting '${part.name}' ?`,
        icon: "fa fa-exclamation-triangle",
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
        header: `Deleting ${this.selectedParts.length} parts.`,
        icon: "fa fa-exclamation-triangle",
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
                  this.preloadsStore.decrementCategoryPartsCount(
                    this.categoryId
                  );
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
              this.preloadsStore.decrementCategoryPartsCount(
                part.category.id,
                ids.length
              );
              this.preloadsStore.incrementCategoryPartsCount(
                categoryId,
                ids.length
              );
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
    updateInplaceQty(event, part, qty) {
      logger.default.info("update inplace qty", part.id, qty);
      apiService
        .updatePartialPart(part.id, { stock_qty: qty })
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: `Updating part quantity`,
            detail: "Success",
            life: 5000,
          });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: `Updating part quantity`,
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with quantity part update", err);
        });
      this.$refs[`inplace_qty_${part.id}`].close();
    },
    updateInplaceQtyMin(event, part, qty) {
      logger.default.info("update inplace qty min", part.id, qty);
      apiService
        .updatePartialPart(part.id, { stock_qty_min: qty })
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: `Updating min part quantity`,
            detail: "Success",
            life: 5000,
          });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: `Updating min part quantity`,
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with min quantity part update", err);
        });
      this.$refs[`inplace_qty_min_${part.id}`].close();
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
  },
};
</script>

<style lang="scss" scoped>
.card {
  background: #ffffff;
  padding: 2rem;
  box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14),
    0 1px 3px 0 rgba(0, 0, 0, 0.12);
  border-radius: 4px;
  margin-bottom: 2rem;
}

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
