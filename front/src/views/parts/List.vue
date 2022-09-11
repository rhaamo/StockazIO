<template>
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
          v-model:selection="selectedParts"
          :selectAll="selectAll"
          @select-all-change="onSelectAllChange"
          @row-select="onRowSelect"
          @row-unselect="onRowUnselect"
          stripedRows
          class="p-datatable-sm"
          removableSort
        >
          <template #empty> No parts found. </template>

          <template #header v-if="selectedParts && selectedParts.length">
            <Button label="Change category" class="p-button-secondary" />
            <Button label="Change location" class="p-button-secondary ml-2" />
            <Button
              label="Delete"
              class="p-button-danger ml-2"
              @click="deletePartMultiple($event)"
            />
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
                      showOverlayPanelImage($event, `p_a_${slotProps.data.id}`)
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
              <Inplace :closable="true">
                <template #display
                  ><span>{{ slotProps.data.stock_qty }}</span></template
                ><template #content>TODO</template></Inplace
              >
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
            ><template #body="slotProps">
              <Inplace :closable="true">
                <template #display
                  ><span>{{ slotProps.data.stock_qty_min }}</span></template
                ><template #content>TODO</template></Inplace
              >
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
                  slotProps.data.footprint ? slotProps.data.footprint.name : "-"
                }}
              </span>
            </template>
            <template #filter="{ filterModel }">
              <MultiSelect
                v-model="filterModel.value"
                class="p-column-filter"
                placeholder="Search by footprint"
                :options="choicesFootprintWithNo"
                optionLabel="name"
                optionValue="id"
                optionGroupLabel="category"
                optionGroupChildren="footprints"
                :selectionLimit="1"
                :filter="true"
              />
            </template>
          </Column>
          <Column :sortable="false"
            ><template #body="slotProps">
              <Button
                type="button"
                icon="fa fa-edit"
                class="p-button-primary"
                v-tooltip="'edit'"
                :to="{
                  name: 'parts-edit',
                  params: { partId: slotProps.data.id },
                }"
              ></Button>
              <Button
                type="button"
                icon="fa fa-trash-o"
                class="p-button-danger ml-2"
                v-tooltip="'delete'"
                @click="deletePart($event, slotProps.data)"
              ></Button
            ></template>
          </Column>
        </DataTable>
      </TabPanel>
      <TabPanel>
        <template #header>
          <i class="fa fa-image mr-2"></i> <span>Thumbnails</span>
        </template>
        TODO
      </TabPanel>
    </TabView>
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
import { cloneDeep } from "lodash";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";

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
    filters: {
      name: {
        constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
      },
      storage_id: {
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
      },
      stock_qty: {
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
      },
      footprint_id: {
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
      },
    },
    selectAll: false,
    selectedParts: null,
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
                params: { categoryId: this.actualCurrentCategory.id },
              },
            },
          ],
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
      this.lazyParams = {
        first: 0,
        rows: this.$refs.dt.rows,
        sortField: null,
        sortOrder: null,
        filters: this.filters,
      };
      this.loadLazyData();
      this.categoryChanged();
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
        this.lazyParams.search = this.searchQuery;
        this.loadLazyData();
      } else if (this.storageUuid) {
        this.lazyParams.storageUuid = this.storageUuid;
        this.loadLazyData();
      } else {
        this.loadLazyData();
        this.categoryChanged();
      }
    });
  },
  methods: {
    categoryChanged() {
      if (!this.categoryId || Number(this.categoryId) === 0) {
        this.preloadsStore.setCurrentCategory({
          id: this.categoryId,
          name: "none",
        });
        return;
      }
      let curCat = null;
      const cb = (e) => {
        if (e.id === Number(this.categoryId)) {
          curCat = e;
        }
        e.children.forEach(cb);
      };
      this.categories.forEach(cb);
      this.preloadsStore.setCurrentCategory({
        id: this.categoryId,
        name: curCat.name,
      });
    },
    loadLazyData() {
      this.loading = true;

      // Do a quick cleanup of datas before sending them
      const params = cloneDeep(this.lazyParams);
      if (params.filters["storage_id"]["constraints"][0].value) {
        params.filters["storage_id"]["constraints"][0].value = Object.keys(
          params.filters["storage_id"]["constraints"][0].value
        )[0];
      }
      if (params.filters["footprint_id"]["constraints"][0].value) {
        params.filters["footprint_id"]["constraints"][0].value =
          params.filters["footprint_id"]["constraints"][0].value[0];
      }

      apiService.getParts(params).then((res) => {
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
    viewPartModal(item) {},
    showLabelGenerator(item) {},
    showOverlayPanelImage(event, ref) {
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
              console.log("delete part", part.name);
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
            console.log("reload");
            this.selectedParts = [];
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
