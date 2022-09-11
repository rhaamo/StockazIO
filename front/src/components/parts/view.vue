<template>
  <div>
    <div class="grid">
      <div class="col-6">
        <div class="grid">
          <div class="col-3">
            <template v-if="part.stock_qty >= part.stock_qty_min"
              ><b>Qty:</b
              ><span class="ml-1">{{ part.stock_qty }}</span></template
            >
            <template v-else>
              <b>Qty:</b>
              <span
                class="text-red-500 ml-1"
                v-tooltip="
                  'Current stock is below minimum stock quantity or exhausted'
                "
                >{{ part.stock_qty }} <i class="fa fa-circle"></i
              ></span>
            </template>
          </div>
          <div class="col-3"><b>Qty min:</b> {{ part.stock_qty_min }}</div>
          <div class="col-6"><b>Unit: </b> {{ partUnit }}</div>
        </div>

        <div class="mt-2 mb-2 surface-50 p-2">
          {{ part.description || "No description" }}
        </div>

        <div>
          <DataTable
            :value="mainTableItems"
            class="p-datatable-sm"
            stripedRows
            responsiveLayout="scroll"
          >
            <Column field="item" header="Item"></Column>
            <Column field="value" header="Value"></Column>
          </DataTable>
        </div>
      </div>

      <div class="col-6">
        <div class="mb-3">
          <Galleria
            :value="pictureAttachments"
            containerStyle="max-width: 640px"
          >
            <template #item="slotProps">
              <Image
                preview
                height="100"
                :src="slotProps.item.picture"
                :alt="slotProps.item.description"
              />
            </template>
            <template #thumbnail="slotProps">
              <img
                :src="slotProps.item.picture_medium"
                :alt="slotProps.item.description"
                style="height: 60px"
              />
            </template>
          </Galleria>
        </div>

        <TabView :scrollable="true">
          <TabPanel>
            <template #header>
              <span>Parameters</span>
            </template>
            <DataTable
              :value="part.part_parameters_value"
              class="p-datatable-sm"
              stripedRows
              responsiveLayout="scroll"
            >
              <Column field="name" header="Name"></Column>
              <Column field="description" header="Description"></Column>
              <Column header="Value">
                <template #body="slotProps">{{
                  slotProps.data.unit
                    ? `${slotProps.data.unit.name} (${slotProps.data.unit.symbol})`
                    : ""
                }}</template>
              </Column>
            </DataTable>
          </TabPanel>

          <TabPanel>
            <template #header>
              <span>Distributors</span>
            </template>
            <DataTable
              :value="part.distributors_sku"
              class="p-datatable-sm"
              stripedRows
              responsiveLayout="scroll"
            >
              <Column field="sku" header="SKU"></Column>
              <Column header="Distributor">
                <template #body="slotProps">{{
                  slotProps.data.distributor
                    ? slotProps.data.distributor.name
                    : "No name"
                }}</template>
              </Column>
              <Column header="Datasheet">
                <template #body="slotProps">
                  <template v-if="slotProps.data.datasheet_url">
                    <a :href="slotProps.data.datasheet_url" target="_blank"
                      ><i class="fa fa-file-pdf-o"></i>
                      {{ slotProps.data.datasheet_url }}</a
                    ></template
                  ></template
                >
              </Column>
            </DataTable>
          </TabPanel>

          <TabPanel>
            <template #header>
              <span>Manufacturers</span>
            </template>
            <DataTable
              :value="part.manufacturers_sku"
              class="p-datatable-sm"
              stripedRows
              responsiveLayout="scroll"
            >
              <Column field="sku" header="SKU"></Column>
              <Column header="Manufacturer">
                <template #body="slotProps">{{
                  slotProps.data.manufacturer
                    ? slotProps.data.manufacturer.name
                    : "No name"
                }}</template>
              </Column>
              <Column header="Datasheet">
                <template #body="slotProps">
                  <template v-if="slotProps.data.datasheet_url">
                    <a :href="slotProps.data.datasheet_url" target="_blank"
                      ><i class="fa fa-file-pdf-o"></i>
                      {{ slotProps.data.datasheet_url }}</a
                    ></template
                  ></template
                >
              </Column>
            </DataTable>
          </TabPanel>

          <TabPanel>
            <template #header>
              <span>Files</span>
            </template>
            <DataTable
              :value="part.part_attachments"
              class="p-datatable-sm"
              stripedRows
              responsiveLayout="scroll"
            >
              <Column header="Link"
                ><template #body="slotProps">
                  <template
                    v-if="
                      slotProps.data.picture && slotProps.data.picture_medium
                    "
                  >
                    <i class="fa fa-picture-o"></i>
                    <a :href="slotProps.data.picture">{{
                      stripPathFromFileUrl(slotProps.data.picture)
                    }}</a>
                  </template>
                  <template v-else>
                    <i class="fa fa-code-o"></i>
                    <a :href="slotProps.data.file">{{
                      stripPathFromFileUrl(slotProps.data.file)
                    }}</a>
                  </template>
                </template></Column
              >
              <Column field="description" header="Description"> </Column>
            </DataTable>
          </TabPanel>

          <TabPanel>
            <template #header>
              <span>Stock history</span>
            </template>
            <DataTable
              :value="part.part_stock_history"
              class="p-datatable-sm"
              stripedRows
              responsiveLayout="scroll"
            >
              <Column field="created_at" header="Date"
                ><template #body="slotProps">{{
                  formatDate(slotProps.data.created_at)
                }}</template></Column
              >
              <Column field="diff" header="Amount"> </Column>
            </DataTable>
          </TabPanel>
        </TabView>
      </div>
    </div>
  </div>
</template>

<script>
import dateFnsFormat from "date-fns/format";
import dateFnsParseISO from "date-fns/parseISO";
import utils from "@/utils.js";

export default {
  inject: ["dialogRef"],
  data: () => ({
    part: null,
  }),
  created() {
    this.part = this.dialogRef.data.part;
  },
  computed: {
    partUnit() {
      if (this.part && this.part.part_unit) {
        if (this.part.part_unit.short_name) {
          return `${this.part.part_unit.name} (${this.part.part_unit.short_name})`;
        } else {
          return this.part.part_unit.name;
        }
      }
      return "";
    },
    mainTableItems() {
      return [
        {
          item: "Footprint",
          value: this.part.footprint ? this.part.footprint.name : "",
        },
        {
          item: "Storage",
          value: this.part.storage ? this.part.storage.name : "",
        },
        {
          item: "Category",
          value: this.part.category ? this.part.category.name : "",
        },
        {
          item: "Internal part number",
          value: this.part.internal_part_number || "",
        },
        { item: "Comment", value: this.part.comment || "" },
        {
          item: "Production remarks",
          value: this.part.production_remarks || "",
        },
        {
          item: "Sheet Need review",
          value: this.part.needs_review ? "yes" : "no",
        },
        { item: "Part Condition", value: this.part.condition || "" },
        { item: "Can be sold", value: this.part.can_be_sold ? "yes" : "no" },
        { item: "Added", value: this.formatDate(this.part.created_at) },
        { item: "Updated", value: this.formatDate(this.part.updated_at) },
      ];
    },
    pictureAttachments() {
      return (
        this.part.part_attachments.filter((x) => {
          if (x.picture && x.picture_medium) {
            return x;
          }
        }) || []
      );
    },
  },
  methods: {
    formatDate(date) {
      return dateFnsFormat(dateFnsParseISO(date), "E MMM d yyyy HH:mm");
    },
    stripPathFromFileUrl(url) {
      return utils.baseName(url);
    },
  },
};
</script>
