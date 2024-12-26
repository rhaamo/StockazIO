<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <Card class="mt-2">
      <template #title>Basic parts informations</template>
      <template #content>
        <form @submit.prevent="submit(!v$.$invalid, 'add_new')">
          <div class="grid">
            <div class="col-6">
              <div class="field">
                <label
                  for="name"
                  :class="{
                    block: true,
                    'p-error': v$.form.name.$invalid && submitted,
                    'w-10': true,
                  }"
                  >Name*</label
                >
                <IconField>
                  <InputIcon :class="partNameAutofinder"></InputIcon>
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
                </IconField>
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

              <div class="field">
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
                  }"
                  @blur="autoDetectFootprint" />
                <small v-if="(v$.form.description.$invalid && submitted) || v$.form.description.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.form.description.maxLength.$message }}
                </small>
              </div>

              <div class="field">
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

              <div class="grid">
                <div class="field col-5">
                  <label
                    for="qty"
                    :class="{
                      'p-error': v$.form.qty.$invalid && submitted,
                      'pr-3': true,
                      block: true,
                    }"
                    >Stock Qty*</label
                  >
                  <InputNumber
                    v-model="form.qty"
                    input-id="qty"
                    mode="decimal"
                    show-buttons
                    button-layout="horizontal"
                    :min="0"
                    :invalid="v$.form.qty.$invalid && submitted" />
                  <small v-if="(v$.form.qty.$invalid && submitted) || v$.form.qty.$pending.$response" class="p-error"
                    ><br />
                    {{ v$.form.qty.required.$message }}
                    <template v-if="v$.form.qty.required && v$.form.qty.minValue"><br /></template>
                    {{ v$.form.qty.minValue.$message }}
                  </small>

                  <InputGroup class="mt-3">
                    <PvButton label="-10" severity="success" size="small" @click.prevent="updateQty(-10)" />
                    <PvButton label="-50" severity="info" size="small" @click.prevent="updateQty(-50)" />
                    <PvButton label="-100" severity="help" size="small" @click.prevent="updateQty(-100)" />
                    <PvButton disabled severity="secondary" size="small" />
                    <PvButton label="+100" severity="help" size="small" @click.prevent="updateQty(+100)" />
                    <PvButton label="+50" severity="info" size="small" @click.prevent="updateQty(+50)" />
                    <PvButton label="+10" severity="success" size="small" @click.prevent="updateQty(+10)" />
                  </InputGroup>
                </div>

                <div class="field col-5">
                  <label
                    for="qty_min"
                    :class="{
                      'p-error': v$.form.qty_min.$invalid && submitted,
                      'pr-3': true,
                      block: true,
                    }"
                    >Stock Qty Min*</label
                  >
                  <InputNumber
                    v-model="form.qty_min"
                    input-id="qty_min"
                    mode="decimal"
                    show-buttons
                    :min="0"
                    :invalid="v$.form.qty_min.$invalid && submitted"
                    button-layout="horizontal" />
                  <small v-if="(v$.form.qty_min.$invalid && submitted) || v$.form.qty_min.$pending.$response" class="p-error"
                    ><br />
                    {{ v$.form.qty_min.required.$message }}
                    <template v-if="v$.form.qty_min.required && v$.form.qty_min.minValue"><br /></template>
                    {{ v$.form.qty_min.minValue.$message }}
                  </small>
                </div>
              </div>

              <div class="field">
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

              <div class="field">
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

              <div class="field">
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

              <div class="field">
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

              <div class="field-checkbox">
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
              <div class="field-checkbox">
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
              <div class="field-checkbox">
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

            <div class="col-6">
              <div class="field">
                <label for="part_unit" class="block">Part unit</label>
                <Listbox
                  v-model="form.part_unit"
                  placeholder="Centimeters ? Pieces ?"
                  class="w-7"
                  :options="choicesPartUnit"
                  option-label="text"
                  option-value="value"
                  checkmark
                  striped />
              </div>

              <div class="field">
                <label for="category" class="block">Category</label>
                <TreeSelect
                  ref="categoryTree"
                  v-model="form.category"
                  v-model:expandedKeys="expandedCategoryKeys"
                  input-id="category"
                  placeholder="Film resistors ? MCUs ?"
                  :options="choicesCategory"
                  selection-mode="single"
                  class="w-7"
                  :filter="true"
                  :fluid="true"
                  :show-clear="true"
                  auto-filter-focus />
              </div>

              <div class="field">
                <label for="storage_location" class="block">Storage Location</label>
                <TreeSelect
                  v-model="form.storage_location"
                  v-model:expandedKeys="expandedStorageKeys"
                  input-id="storage_location"
                  placeholder="A box under the bench or some drawer ?"
                  class="w-7"
                  :options="choicesStorageLocation"
                  selection-mode="single"
                  auto-filter-focus
                  filter />
              </div>

              <div class="field">
                <label for="footprint" class="block"
                  ><PvButton
                    v-tooltip.top="`Try auto-match from description`"
                    raised
                    rounded
                    size="small"
                    severity="info"
                    variant="text"
                    icon="pi pi-refresh"
                    @click.prevent="autoDetectFootprint()" />
                  Footprint&nbsp;
                  <template v-if="form.footprint"
                    ><small>(selected: {{ getFootprintNameFromId(form.footprint) }})</small></template
                  >
                </label>

                <Listbox
                  v-model="form.footprint"
                  input-id="footprint"
                  placeholder="PDIP, BGA, SOIC, who knows"
                  class="w-7"
                  :options="choicesFootprint"
                  option-label="name"
                  option-value="id"
                  option-group-label="category"
                  option-group-children="footprints"
                  :filter="true"
                  auto-filter-focus
                  checkmark />
              </div>

              <div class="field">
                <!-- save and save add another-->
                <PvButton label="Save and view" class="p-button-primary" @click.prevent="submit(!v$.$invalid, 'continue')" />
                <PvButton
                  type="submit"
                  label="Save and add another"
                  class="ml-2 p-button-secondary"
                  @click.prevent="submit(!v$.$invalid, 'add_new')" />
              </div>
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
import PartViewModal from "@/components/parts/view.vue";
import { h } from "vue";
import Button from "primevue/button";
import { fuzzyMatch } from "fuzzbunny";

export default {
  setup: () => ({
    v$: useVuelidate(),
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
  }),
  data: () => ({
    submitted: false,
    form: {
      name: "",
      description: "",
      comment: "",
      qty: 0,
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
    },
    partsExists: [],
    partDetails: null,
    expandedStorageKeys: {},
    expandedCategoryKeys: {},
    partNameAutofinder: "pi pi-ellipsis-h",
  }),
  mounted() {
    if (this.currentCategory) {
      this.form.category = { [this.currentCategory.id]: true };
    }
    this.expandAllStorageChoices();
    this.expandAllCategoryChoices();
  },
  computed: {
    ...mapState(usePreloadsStore, {
      currentCategory: (store) => store.currentCategory,
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
            icon: `fa fa-folder-o`,
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
      flattenedChoicesFootprints: (store) =>
        store.footprints
          .map((x) => {
            return x.footprint_set.map((y) => {
              return { id: y.id, name: y.name };
            });
          })
          .flat(),
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
            label: "Quick add new part",
          },
        ],
      };
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
    submit(isFormValid, mode) {
      this.submitted = true;

      if (!isFormValid) {
        return;
      }

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
      };
      if (datas.category === 0 || datas.category === "0" || datas.category === "null") {
        datas.category = null;
      }

      logger.default.info("submitting part", datas);

      apiService
        .createPart(datas)
        .then((resp) => {
          this.toast.add({
            severity: "success",
            summary: "Adding part",
            detail: "Success",
            life: 5000,
          });
          this.preloadsStore.incrementCategoryPartsCount(datas.category);
          if (mode === "add_new") {
            this.clearForm();
          } else {
            // mode === continue
            this.$router.push({
              name: "parts-details",
              params: { partId: resp.data.id },
            });
          }
        })
        .catch((error) => {
          this.toast.add({
            severity: "error",
            summary: "Adding part",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Cannot save part", error.message);
        });
    },
    checkIfPartExists(event) {
      if (this.form.name === "") {
        return;
      }
      apiService
        .partsAutocompleteQuick(this.form.name)
        .then((res) => {
          this.partsExists = res.data;
          this.partNameAutofinder = "pi pi-times";
        })
        .catch((err) => {
          if (err.response.status === 404) {
            logger.default.info("Autocompleter said part not found");
            this.partNameAutofinder = "pi pi-check";
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
      this.form.qty = 0;
      this.form.qty_min = 0;
      this.form.sheet_status = "";
      this.form.condition = "";
      this.form.internal_pn = "";
      this.form.needs_review = false;
      this.form.footprint = null;
      this.form.production_remarks = "";
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
              dismissableMask: true,
            },
            templates: {
              header: () => {
                if (part.private) {
                  return [h("h3", [h("i", { class: "fa fa-lock mr-1" }), h("span", part.name)])];
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
    autoDetectFootprint() {
      if (!this.form.description) {
        return;
      }
      for (const i of this.flattenedChoicesFootprints) {
        const match = fuzzyMatch(this.form.description, i.name);
        if (match) {
          console.log("Matched description", this.form.description, "with footprint", i.name);
          this.form.footprint = i.id;
          return;
        }
      }
      console.log("Could not match description", this.form.description, "with any footprint");
    },
    getFootprintNameFromId(id) {
      for (let fp of this.flattenedChoicesFootprints) {
        if (fp.id === id) {
          return fp.name;
        }
      }
      return "none";
    },
    updateQty(quantity) {
      if (this.form.qty + quantity < 0) {
        this.form.qty = 0;
        return;
      }
      this.form.qty += quantity;
    },
  },
};
</script>
