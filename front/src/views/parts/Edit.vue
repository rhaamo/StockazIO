<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <Card v-if="part" class="mt-2">
      <template #title>Basic parts informations</template>
      <template #content>
        <form @submit.prevent="submit(!v$.$invalid)">
          <div class="grid">
            <div class="col-6">
              <div class="mb-3">
                <label
                  for="name"
                  :class="{
                    block: true,
                    'p-error': v$.form.name.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Name*</label
                >
                <InputText
                  ref="name"
                  v-model="form.name"
                  v-focus
                  autofocus
                  input-id="name"
                  type="text"
                  placeholder="PIC42ACHU"
                  :class="{
                    'p-invalid': v$.form.name.$invalid && submitted,
                    'w-10': true,
                  }"
                  @blur="checkIfPartExists" />
                <small v-if="(v$.form.name.$invalid && submitted) || v$.form.name.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.form.name.required.$message }}
                  <template v-if="v$.form.name.required && v$.form.name.maxLength"><br /></template>
                  {{ v$.form.name.maxLength.$message }}
                </small>
                <div v-if="partsExists && partsExists.length">
                  One or more parts exists with this name:
                  <div v-for="p in partsExists" :key="p.uuid">
                    <a href="#" @click.prevent="viewPartModal(p)">{{ p.name }}</a
                    >&nbsp;
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <label
                  for="description"
                  :class="{
                    block: true,
                    'p-error': v$.form.description.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Description</label
                >
                <InputText
                  v-model="form.description"
                  input-id="description"
                  type="text"
                  placeholder="A cute little mcu"
                  :class="{
                    'p-invalid': v$.form.description.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.form.description.$invalid && submitted) || v$.form.description.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.form.description.maxLength.$message }}
                </small>
              </div>

              <div class="mb-3">
                <label
                  for="comment"
                  :class="{
                    block: true,
                    'p-error': v$.form.comment.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Comment</label
                >
                <InputText
                  v-model="form.comment"
                  input-id="comment"
                  type="text"
                  placeholder="Any comment about this part ?"
                  :class="{
                    'p-invalid': v$.form.description.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.form.comment.$invalid && submitted) || v$.form.comment.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.form.comment.maxLength.$message }}
                </small>
              </div>

              <div class="mb-3 grid">
                <div class="col-5">
                  <label
                    for="qty"
                    :class="{
                      block: true,
                      'p-error': v$.form.qty.$invalid && submitted,
                      'w-8': true,
                    }"
                    >Stock Qty*</label
                  >
                  <InputNumber
                    v-model="form.qty"
                    input-id="qty"
                    mode="decimal"
                    show-buttons
                    :min="0"
                    :class="{
                      'p-invalid': v$.form.qty.$invalid && submitted,
                      'w-8': true,
                    }" />
                  <small v-if="(v$.form.qty.$invalid && submitted) || v$.form.qty.$pending.$response" class="p-error"
                    ><br />
                    {{ v$.form.qty.required.$message }}
                    <template v-if="v$.form.qty.required && v$.form.qty.minValue"><br /></template>
                    {{ v$.form.qty.minValue.$message }}
                  </small>
                </div>

                <div class="col-5">
                  <label
                    for="qty_min"
                    :class="{
                      block: true,
                      'p-error': v$.form.qty_min.$invalid && submitted,
                      'w-8': true,
                    }"
                    >Stock Qty Min*</label
                  >
                  <InputNumber
                    v-model="form.qty_min"
                    input-id="qty_min"
                    mode="decimal"
                    show-buttons
                    :min="0"
                    :class="{
                      'p-invalid': v$.form.qty_min.$invalid && submitted,
                      'w-8': true,
                    }" />
                  <small v-if="(v$.form.qty_min.$invalid && submitted) || v$.form.qty_min.$pending.$response" class="p-error"
                    ><br />
                    {{ v$.form.qty_min.required.$message }}
                    <template v-if="v$.form.qty_min.required && v$.form.qty_min.minValue"><br /></template>
                    {{ v$.form.qty_min.minValue.$message }}
                  </small>
                </div>
              </div>

              <div class="mb-3">
                <label
                  for="sheet_status"
                  :class="{
                    block: true,
                    'p-error': v$.form.sheet_status.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Sheet status</label
                >
                <InputText
                  v-model="form.sheet_status"
                  input-id="sheet_status"
                  type="text"
                  :class="{
                    'p-invalid': v$.form.sheet_status.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.form.sheet_status.$invalid && submitted) || v$.form.sheet_status.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.form.sheet_status.maxLength.$message }}
                </small>
              </div>

              <div class="mb-3">
                <label
                  for="condition"
                  :class="{
                    block: true,
                    'p-error': v$.form.condition.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Part Condition</label
                >
                <InputText
                  v-model="form.condition"
                  type="text"
                  input-id="condition"
                  placeholder="Condition of the part"
                  :class="{
                    'p-invalid': v$.form.condition.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.form.condition.$invalid && submitted) || v$.form.condition.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.form.condition.maxLength.$message }}
                </small>
              </div>

              <div class="mb-3">
                <label
                  for="production_remarks"
                  :class="{
                    block: true,
                    'p-error': v$.form.production_remarks.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Production Remarks</label
                >
                <InputText
                  v-model="form.production_remarks"
                  input-id="production_remarks"
                  type="text"
                  :class="{
                    'p-invalid': v$.form.production_remarks.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.form.production_remarks.$invalid && submitted) || v$.form.production_remarks.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.form.production_remarks.maxLength.$message }}
                </small>
              </div>

              <div class="mb-3">
                <label
                  for="internal_pn"
                  :class="{
                    block: true,
                    'p-error': v$.form.internal_pn.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Internal Part Number</label
                >
                <InputText
                  v-model="form.internal_pn"
                  input-id="internal_pn"
                  type="text"
                  :class="{
                    'p-invalid': v$.form.internal_pn.$invalid && submitted,
                    'w-10': true,
                  }" />
                <small v-if="(v$.form.internal_pn.$invalid && submitted) || v$.form.internal_pn.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.form.internal_pn.maxLength.$message }}
                </small>
              </div>

              <div class="grid">
                <div class="field-checkbox col-4">
                  <Checkbox
                    v-model="form.needs_review"
                    :class="{
                      'p-invalid': v$.form.needs_review.$invalid && submitted,
                    }"
                    input-id="needs_review"
                    :binary="true" />
                  <label
                    for="needs_review"
                    :class="{
                      'p-error': v$.form.needs_review.$invalid && submitted,
                    }"
                    >This sheet needs review</label
                  >
                </div>
                <div class="field-checkbox col-4">
                  <Checkbox
                    v-model="form.can_be_sold"
                    :class="{
                      'p-invalid': v$.form.can_be_sold.$invalid && submitted,
                    }"
                    input-id="can_be_sold"
                    :binary="true" />
                  <label
                    :class="{
                      'p-error': v$.form.can_be_sold.$invalid && submitted,
                    }"
                    for="can_be_sold"
                    >That part can be sold</label
                  >
                </div>
                <div class="field-checkbox col-4">
                  <Checkbox
                    v-model="form.private"
                    :class="{
                      'p-invalid': v$.form.private.$invalid && submitted,
                    }"
                    input-id="private"
                    :binary="true" />
                  <label
                    :class="{
                      'p-error': v$.form.private.$invalid && submitted,
                    }"
                    for="private"
                    >That part is private</label
                  >
                </div>
              </div>

              <div class="mb-3">
                <label for="part_unit" class="block">Part unit</label>
                <Dropdown
                  v-model="form.part_unit"
                  placeholder="Centimeters ? Pieces ?"
                  class="w-10"
                  :options="choicesPartUnit"
                  option-label="text"
                  option-value="value" />
              </div>

              <div class="mb-3">
                <label for="category" class="block">Category</label>
                <TreeSelect
                  ref="categoryTree"
                  v-model="form.category"
                  v-model:expandedKeys="expandedCategoryKeys"
                  input-id="category"
                  placeholder="Film resistors ? MCUs ?"
                  :options="choicesCategory"
                  selection-mode="single"
                  class="w-10"
                  :filter="true"
                  :fluid="true"
                  :show-clear="true"
                  auto-filter-focus />
              </div>

              <div class="mb-3">
                <div class="grid">
                  <div class="col-5">
                    <label for="storage_location" class="block">Storage Location</label>
                    <TreeSelect
                      v-model="form.storage_location"
                      v-model:expandedKeys="expandedStorageKeys"
                      input-id="storage_location"
                      placeholder="A box under the bench or some drawer ?"
                      fluid
                      :options="choicesStorageLocation"
                      selection-mode="single"
                      auto-filter-focus
                      filter />
                  </div>
                  <div class="col-4 col-offset-1">
                    <label for="footprint" class="block"
                      >Footprint&nbsp;<template v-if="form.footprint"
                        ><small>(selected: {{ getFootprintNameFromId(form.footprint) }})</small></template
                      ></label
                    >
                    <Listbox
                      v-model="form.footprint"
                      input-id="footprint"
                      placeholder="PDIP, BGA, SOIC, who knows"
                      :options="choicesFootprint"
                      option-label="name"
                      option-value="id"
                      option-group-label="category"
                      option-group-children="footprints"
                      :filter="true"
                      auto-filter-focus
                      checkmark
                      fluid />
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <PvButton type="submit" label="Update" class="p-button-primary" @click.prevent="submit(!v$.$invalid)" />
              </div>
            </div>
            <div class="col-6">
              <Tabs value="0" scrollable>
                <TabList>
                  <Tab value="0">Parameters</Tab>
                  <Tab value="1">Manufacturers</Tab>
                  <Tab value="2">Distributors</Tab>
                </TabList>
                <TabPanels>
                  <!-- Parameters -->
                  <TabPanel value="0">
                    <div v-for="(_, i) in form.part_parameters_value" :key="i">
                      <PartParametersEntry
                        v-model:item="form.part_parameters_value[i]"
                        :submitted="submitted"
                        @deleteItem="deletePartParameter($event, i)" />
                    </div>

                    <Divider />
                    <div class="grid">
                      <div class="col-3">
                        <PvButton class="p-button-help" label="add item" @click.prevent="addPartParameter($event)" />
                      </div>
                      <div class="col-9">
                        <Dropdown
                          v-model="part_parameters_preset"
                          input-id="preset"
                          class="w-7 mr-1"
                          :options="choicesPartParametersPreset"
                          option-label="text"
                          option-value="value"
                          :filter="true"
                          placeholder="Preset to apply" />
                        <ButtonDeleteInline
                          size="p-button-sm"
                          btn-variant-main="p-button-info"
                          btn-variant-ok="p-button-success"
                          btn-variant-cancel="p-button-info"
                          btn-main-text="apply"
                          btn-main-text-disabled="Confirm ?"
                          btn-ok-text="Yes"
                          btn-cancel-text="No"
                          @action-confirmed="applyPartParametersPreset" />
                      </div>
                    </div>
                  </TabPanel>
                  <!-- Manufacturers -->
                  <TabPanel value="1">
                    <div v-for="(_, i) in form.manufacturers_sku" :key="i">
                      <ManufacturersSkuEntry
                        v-model:item="form.manufacturers_sku[i]"
                        :submitted="submitted"
                        @deleteItem="deleteManufacturer($event, i)" />
                    </div>

                    <Divider />
                    <div>
                      <PvButton class="p-button-help" label="add item" @click.prevent="addManufacturer($event)" />
                    </div>
                  </TabPanel>
                  <!-- Distributors -->
                  <TabPanel value="2">
                    <div v-for="(_, i) in form.distributors_sku" :key="i">
                      <DistributorsSkuEntry
                        v-model:item="form.distributors_sku[i]"
                        :submitted="submitted"
                        @deleteItem="deleteDistributor($event, i)" />
                    </div>

                    <Divider />
                    <PvButton class="p-button-help" label="add item" @click.prevent="addDistributor($event)" />
                  </TabPanel>
                </TabPanels>
              </Tabs>
            </div>
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { usePreloadsStore } from "@/stores/preloads";
import { required, maxLength, integer, minValue } from "@vuelidate/validators";
import logger from "@/logging";
import apiService from "@/services/api/api.service";
import { mapState } from "pinia";
import { useToast } from "primevue/usetoast";
import DistributorsSkuEntry from "@/components/parts/DistributorsSkuEntry.vue";
import ManufacturersSkuEntry from "@/components/parts/ManufacturersSkuEntry.vue";
import PartParametersEntry from "@/components/parts/PartParametersEntry.vue";
import PartViewModal from "@/components/parts/view.vue";
import { h } from "vue";
import Button from "primevue/button";

export default {
  components: {
    DistributorsSkuEntry,
    ManufacturersSkuEntry,
    PartParametersEntry,
  },
  props: {
    node: Number,
  },
  setup: () => ({
    v$: useVuelidate(),
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
  }),
  data: () => ({
    submitted: false,
    part: null,
    form: {
      name: "",
      description: "",
      comment: "",
      qty: 1,
      qty_min: 0,
      sheet_status: "",
      condition: "",
      needs_review: false,
      can_be_sold: false,
      private: false,
      production_remarks: "",
      internal_pn: "",
      part_unit: null,
      category: null,
      storage_location: null,
      footprint: null,
      distributors_sku: [],
      manufacturers_sku: [],
      part_parameters_value: [],
    },
    partsExists: [],
    partDetails: null,
    part_parameters_preset: null,
    origCategory: null,
    expandedStorageKeys: {},
    expandedCategoryKeys: {},
  }),
  created() {
    this.fetchPart();
  },
  mounted() {
    this.expandAllStorageChoices();
    this.expandAllCategoryChoices();
  },
  computed: {
    ...mapState(usePreloadsStore, {
      choicesPartUnit: (store) =>
        store.part_units.map((x) => {
          return { value: x.id, text: `${x.name} (${x.short_name})` };
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
      choicesStorageLocation: (store) => {
        const cb = (e) => {
          // base object
          let obj = {
            key: e.uuid ? e.id : `cat-${e.id}`,
            label: e.description ? `${e.name} (${e.description})` : e.name,
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
            category: x.description ? `${x.name} (${x.description})` : x.name,
            footprints: x.footprint_set.map((y) => {
              return { id: y.id, name: y.name };
            }),
          };
        }),
      choicesPartParametersPreset: (store) => {
        return store.partParametersPresets.map((x) => {
          return { value: x, text: x.name };
        });
      },
      flattenedChoicesFootprints: (store) =>
        store.footprints
          .map((x) => {
            return x.footprint_set.map((y) => {
              return { id: y.id, name: y.name };
            });
          })
          .flat(),
    }),
    partId() {
      return this.$route.params.partId;
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
            label: "Edit part",
            command: () => {
              this.$router.push({
                name: "parts-edit",
                params: { partId: this.partId },
              });
            },
          },
        ],
      };
      if (this.part) {
        bc.items.push({
          label: this.part.name,
          command: () => {
            this.$router.push({
              name: "parts-details",
              params: { partId: this.partId },
            });
          },
        });
      }
      return bc;
    },
  },
  validations: {
    form: {
      name: {
        required,
        maxLength: maxLength(255),
      },
      description: {
        maxLength: maxLength(255),
      },
      comment: {
        maxLength: maxLength(255),
      },
      qty: {
        required,
        integer,
        minValue: minValue(0),
      },
      qty_min: {
        required,
        integer,
        minValue: minValue(0),
      },
      sheet_status: {
        maxLength: maxLength(255),
      },
      needs_review: {},
      condition: {
        maxLength: maxLength(255),
      },
      can_be_sold: {},
      private: {},
      production_remarks: {
        maxLength: maxLength(255),
      },
      internal_pn: {
        maxLength: maxLength(255),
      },
      part_unit: {},
      category: {},
      storage_location: {},
      footprint: {},
    },
  },
  methods: {
    submit(isFormValid) {
      this.submitted = true;

      if (!isFormValid) {
        return;
      }

      let newCategoryId = this.form.category;

      let datas = {
        name: this.form.name,
        description: this.form.description,
        comment: this.form.comment,
        stock_qty: this.form.qty,
        stock_qty_min: this.form.qty_min,
        status: this.form.sheet_status,
        needs_review: this.form.needs_review,
        condition: this.form.condition,
        can_be_sold: this.form.can_be_sold,
        private: this.form.private,
        production_remarks: this.form.production_remarks,
        internal_part_number: this.form.internal_pn,

        part_unit: this.form.part_unit,
        category: this.form.category ? Object.keys(this.form.category)[0] : null,
        storage: this.form.storage_location ? Object.keys(this.form.storage_location)[0] : null,
        footprint: this.form.footprint,

        distributors_sku: this.form.distributors_sku.map((x) => {
          return {
            datasheet_url: x.datasheet_url,
            distributor: x.distributor ? x.distributor.value : null,
            sku: x.sku,
          };
        }),
        manufacturers_sku: this.form.manufacturers_sku.map((x) => {
          return {
            datasheet_url: x.datasheet_url,
            manufacturer: x.manufacturer ? x.manufacturer.value : null,
            sku: x.sku,
          };
        }),
        part_parameters_value: this.form.part_parameters_value,
      };
      if (datas.category === 0 || datas.category === "0" || datas.category === "null") {
        datas.category = null;
      }
      if (datas.category && datas.category.undefined && !datas.category.undefined) {
        datas.category = null;
      }

      logger.default.info("submitting part", datas);

      apiService
        .updatePart(this.part.id, datas)
        .then((resp) => {
          this.toast.add({
            severity: "success",
            summary: "Updating part",
            detail: "Success",
            life: 5000,
          });

          if (this.origCategory && newCategoryId) {
            if (Object.keys(this.origCategory)[0] != Object.keys(newCategoryId)[0]) {
              logger.default.info("old category: ", Object.keys(this.origCategory)[0], " new: ", Object.keys(newCategoryId)[0]);
              this.preloadsStore.decrementCategoryPartsCount(Object.keys(this.origCategory)[0]);
              this.preloadsStore.incrementCategoryPartsCount(Object.keys(newCategoryId)[0]);
              this.origCategory = { [Object.keys(newCategoryId)[0]]: true };
            }
          }
        })
        .catch((error) => {
          this.toast.add({
            severity: "error",
            summary: "Updating part",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Cannot update part", error.message);
        });
    },
    checkIfPartExists(event) {
      if (this.form.name === "") {
        return;
      }
      // ignore self
      if (this.part.name == this.form.name) {
        return;
      }

      apiService
        .partsAutocompleteQuick(this.form.name)
        .then((res) => {
          this.partsExists = res.data;
        })
        .catch((err) => {
          if (err.response.status === 404) {
            logger.default.info("Autocompleter said part not found");
          } else {
            logger.default.error("Got an error from the autocompleter", err.message);
          }
          this.partsExists = [];
        });
    },
    clearForm: function () {
      this.form.name = "";
      this.form.description = "";
      this.form.comment = "";
      this.form.qty = 1;
      this.form.qty_min = 0;
      this.form.sheet_status = "";
      this.form.condition = "";
      this.form.internal_pn = "";
      this.form.needs_review = false;
      this.form.footprint = null;
      this.form.production_remarks = "";
      this.form.distributors_sku = [];
      this.form.manufacturers_sku = [];
      this.form.part_parameters_value = [];
      this.v$.$reset();
      this.$refs.name.$el.focus();
      this.partsExists = [];
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
                  return [h("h3", [h("i", { class: "pi pi-lock mr-1" }), h("span", part.name)])];
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
                      let route = this.$router.resolve({
                        name: "parts-details",
                        params: { partId: part.id },
                      });
                      window.open(route.href, "_blank");
                    },
                    class: "p-button-outlined",
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
              canDelete: false,
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
    addDistributor(event) {
      this.form.distributors_sku.push({
        sku: "",
        distributor: null,
        datasheet_url: "",
      });
    },
    deleteDistributor(event, idx) {
      this.form.distributors_sku.splice(idx, 1);
    },
    addManufacturer(event) {
      this.form.manufacturers_sku.push({
        sku: "",
        manufacturer: null,
        datasheet_url: "",
      });
    },
    deleteManufacturer(event, idx) {
      this.form.manufacturers_sku.splice(idx, 1);
    },
    addPartParameter(event) {
      this.form.part_parameters_value.push({
        name: "",
        description: "",
        value: "",
        unit: null,
      });
    },
    deletePartParameter(event, idx) {
      this.form.part_parameters_value.splice(idx, 1);
    },
    applyPartParametersPreset() {
      if (this.part_parameters_preset) {
        this.part_parameters_preset.part_parameters_presets.forEach((item) => {
          this.form.part_parameters_value.push({
            name: item.name,
            description: item.description,
            value: "",
            unit: item.unit ? item.unit.id : null,
          });
        });
      }
    },
    fetchPart() {
      apiService
        .getPart(this.partId)
        .then((res) => {
          this.part = res.data;
          this.form.name = this.part.name;
          this.form.description = this.part.description;
          this.form.comment = this.part.comment;
          this.form.qty = this.part.stock_qty;
          this.form.qty_min = this.part.stock_qty_min;
          this.form.sheet_status = this.part.status;
          this.form.needs_review = this.part.needs_review;
          this.form.condition = this.part.condition;
          this.form.can_be_sold = this.part.can_be_sold;
          this.form.private = this.part.private;
          this.form.production_remarks = this.part.production_remarks;
          this.form.internal_pn = this.part.internal_part_number;
          this.form.part_parameters_value = this.part.part_parameters_value.map((x) => {
            return {
              id: x.id,
              name: x.name,
              description: x.description,
              value: x.value,
              unit: x.unit ? x.unit.id : null,
            };
          });
          this.form.manufacturers_sku = this.part.manufacturers_sku.map((x) => {
            return {
              id: x.id,
              sku: x.sku,
              manufacturer: {
                text: x.manufacturer ? x.manufacturer.name : null,
                value: x.manufacturer ? x.manufacturer.id : null,
                datasheet_url: x.manufacturer ? x.manufacturer.datasheet_url : null,
              },
              datasheet_url: x.datasheet_url,
            };
          });
          this.form.distributors_sku = this.part.distributors_sku.map((x) => {
            return {
              id: x.id,
              sku: x.sku,
              distributor: {
                text: x.distributor.name,
                value: x.distributor.id,
                datasheet_url: x.distributor ? x.distributor.datasheet_url : null,
              },
              datasheet_url: x.datasheet_url,
            };
          });
          this.form.part_unit = this.part.part_unit ? this.part.part_unit.id : null;
          this.form.category = this.part.category ? { [this.part.category.id]: true } : null;
          this.form.storage_location = this.part.storage ? { [this.part.storage.id]: true } : null;
          this.form.footprint = this.part.footprint ? this.part.footprint.id : null;
          this.origCategory = this.form.category;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Fetching part details",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with fetching part", err.message);
        });
    },
    expandAllStorageChoices() {
      for (let node of this.choicesStorageLocation) {
        this.expandStorageNode(node);
      }
      this.expandedStorageKeys = { ...this.expandedStorageKeys };
    },
    expandStorageNode(node) {
      if (node.children && node.children.length) {
        this.expandedStorageKeys[node.key] = true;
        for (let child of node.children) {
          this.expandStorageNode(child);
        }
      }
    },
    expandAllCategoryChoices() {
      for (let node of this.choicesCategory) {
        this.expandCategoryNode(node);
      }
      this.expandedCategoryKeys = { ...this.expandedCategoryKeys };
    },
    expandCategoryNode(node) {
      if (node.children && node.children.length) {
        this.expandedCategoryKeys[node.key] = true;
        for (let child of node.children) {
          this.expandCategoryNode(child);
        }
      }
    },
    getFootprintNameFromId(id) {
      for (let fp of this.flattenedChoicesFootprints) {
        if (fp.id === id) {
          return fp.name;
        }
      }
      return "none";
    },
  },
};
</script>
