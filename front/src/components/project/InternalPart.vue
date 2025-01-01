<template>
  <div>
    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-5">
          <label
            for="qty"
            :class="{
              block: true,
              'p-error': v$.item.qty.$invalid && submitted,
              'w-10': true,
            }"
            >Qty</label
          >
          <InputNumber
            ref="qty"
            v-model="item.qty"
            input-id="qty"
            type="text"
            show-buttons
            :min="0"
            :class="{
              'p-invalid': v$.item.qty.$invalid && submitted,
              'w-10': true,
            }" />
          <small v-if="(v$.item.qty.$invalid && submitted) || v$.item.qty.$pending.$response" class="p-error"
            ><br />
            {{ v$.item.qty.required.$message }}
            <template v-if="v$.item.qty.required && v$.item.qty.minVal"><br /></template>
            {{ v$.item.qty.minVal.$message }}
          </small>
        </div>

        <div class="field w-5">
          <label
            for="notes"
            :class="{
              block: true,
              'p-error': v$.item.notes.$invalid && submitted,
              'w-10': true,
            }"
            >Notes</label
          >
          <InputText
            ref="notes"
            v-model="item.notes"
            input-id="notes"
            type="text"
            :class="{
              'p-invalid': v$.item.notes.$invalid && submitted,
              'w-10': true,
            }" />
          <small v-if="(v$.item.notes.$invalid && submitted) || v$.item.notes.$pending.$response" class="p-error"
            ><br />
            {{ v$.item.notes.maxLength.$message }}
          </small>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field-checkbox w-10">
          <Checkbox
            v-model="item.sourced"
            :class="{
              'p-invalid': v$.item.sourced.$invalid && submitted,
            }"
            input-id="sourced"
            :binary="true" />
          <label
            for="sourced"
            :class="{
              'p-error': v$.item.sourced.$invalid && submitted,
            }"
            >Sourced</label
          >
        </div>
      </div>
    </div>

    <Divider />

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <template v-if="mode === 'edit'">
            <div class="mb-3">When editing, the selected part might be in another page of the table.</div>
          </template>

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
            filter-display="menu"
            responsive-layout="scroll"
            striped-rows
            v-model:selection="item.part"
            class="p-datatable-sm"
            removable-sort
            @page="onPage($event)"
            @sort="onSort($event)"
            @filter="onFilter($event)">
            <template #empty> No parts found. </template>

            <template v-if="(v$.item.part.$invalid && submitted) || v$.item.part.$pending.$response" #footer>
              {{ v$.item.part.required.$message }}
            </template>

            <Column selection-mode="single" header-style="width: 3em"></Column>

            <Column header="Name" :sortable="true" field="name" :filter-match-mode-options="matchModes.name">
              <template #body="slotProps">
                <div>
                  {{ slotProps.data.name }}
                  <br />
                  <template v-if="slotProps.data.description">
                    {{ slotProps.data.category ? slotProps.data.category.name : "No category" }}: {{ slotProps.data.description }}
                  </template>
                  <template v-else>
                    {{ slotProps.data.category ? slotProps.data.category.name : "No category" }}
                  </template>
                </div>
              </template>
              <template #filter="{ filterModel }">
                <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Search by name" />
              </template>
            </Column>
            <Column header="Storage" :sortable="true" field="storage_id" :filter-match-mode-options="matchModes.storage">
              <template #body="slotProps">{{ slotProps.data.storage && slotProps.data.storage.name ? slotProps.data.storage.name : "-" }}</template>
              <template #filter="{ filterModel }">
                <TreeSelect
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="Search by storage"
                  :options="choicesStorageLocationWithNo"
                  selection-mode="single" />
              </template>
            </Column>
            <Column header="Stock" :sortable="true" field="stock_qty" data-type="numeric" :filter-match-mode-options="matchModes.qty">
              <template #body="slotProps">
                <template v-if="slotProps.data.stock_qty >= slotProps.data.stock_qty_min"
                  ><span>{{ slotProps.data.stock_qty }}</span></template
                >
                <template v-else>
                  <span v-tooltip="'Current stock is below minimum stock quantity or exhausted'" class="text-red-500"
                    >{{ slotProps.data.stock_qty }} <i class="pi pi-circle-fill"></i
                  ></span>
                </template>
              </template>
              <template #filter="{ filterModel }">
                <InputNumber v-model="filterModel.value" class="p-column-filter" placeholder="qty" />
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
              <template #filter="{ filterModel }">
                <Dropdown
                  v-model="filterModel.value"
                  class="p-column-filter"
                  placeholder="Search by footprint"
                  :options="choicesFootprintWithNo"
                  option-label="name"
                  option-value="id"
                  option-group-label="category"
                  option-group-children="footprints"
                  :filter="true" />
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </div>

    <div class="flex justify-content-center">
      <div class="flex flex-grow-1 align-items-center justify-content-center">
        <div class="field w-10">
          <PvButton label="Save" @click.prevent="submit(!v$.$invalid)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength, minValue } from "@vuelidate/validators";
import apiService from "@/services/api/api.service";
import { useToast } from "primevue/usetoast";
import logger from "@/logging";
import { FilterMatchMode } from "@primevue/core/api";
import { cloneDeep } from "lodash";
import { useServerStore } from "@/stores/server";
import { mapState } from "pinia";

export default {
  inject: ["dialogRef"],
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
    serverStore: useServerStore(),
  }),
  data: () => ({
    mode: null,
    item: {
      qty: 1,
      sourced: false,
      notes: "",
      part: null,
    },
    project: null,
    submitted: false,
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
    selectedPart: null,
  }),
  mounted() {
    this.mode = this.dialogRef.data.mode; // add / edit
    this.project = this.dialogRef.data.project;

    if (this.dialogRef.data.item) {
      this.item = {
        id: this.dialogRef.data.item.id,
        qty: this.dialogRef.data.item.qty,
        sourced: this.dialogRef.data.item.sourced,
        part: {
          id: this.dialogRef.data.item.part ? this.dialogRef.data.item.part.id : null,
        },
      };
    }

    this.lazyParams = {
      first: 0,
      rows: this.$refs.dt.rows,
      sortField: null,
      sortOrder: null,
      filters: this.filters,
    };

    this.loadLazyData();
  },
  validations: {
    item: {
      part: { required },
      qty: {
        required,
        minValue: minValue(0),
      },
      sourced: {},
      notes: { maxLength: maxLength(255) },
    },
  },
  computed: {
    ...mapState(useServerStore, {
      perPage: (store) => 5, // store.settings.pagination.PARTS || 10,
    }),
  },
  methods: {
    loadLazyData() {
      this.loading = true;

      // Do a quick cleanup of datas before sending them
      const params = cloneDeep(this.lazyParams);
      if (params.filters["storage_id"].value) {
        params.filters["storage_id"].value = Object.keys(params.filters["storage_id"].value)[0];
      }

      apiService.getParts(params).then((res) => {
        this.parts = res.data.results;
        this.totalRecords = res.data.count;
        this.loading = false;
      });
    },
    submit(isFormValid) {
      this.submitted = true;
      if (!isFormValid) {
        return;
      }

      if (this.mode === "add") {
        this.save();
      } else {
        this.edit();
      }
    },
    save() {
      let internal_part = {
        part: this.item.part.id,
        qty: this.item.qty,
        sourced: this.item.sourced,
        notes: this.item.notes,
        project: this.project.id,
      };

      apiService
        .projectAddPart(this.project.id, internal_part)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "External part",
            detail: "Saved with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "External part",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with external part saving", err);
          this.dialogRef.close({ finished: true });
        });
    },
    edit() {
      let internal_part = {
        part: this.item.part.id,
        qty: this.item.qty,
        sourced: this.item.sourced,
        notes: this.item.notes,
        project: this.project.id,
      };

      apiService
        .projectUpdatePart(this.project.id, this.item.id, internal_part)
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "External part",
            detail: "Updated with success",
            life: 5000,
          });
          this.dialogRef.close({ finished: true });
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "External part",
            detail: "Save failed",
            life: 5000,
          });
          logger.default.error("Error with external part update", err);
          this.dialogRef.close({ finished: true });
        });
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
