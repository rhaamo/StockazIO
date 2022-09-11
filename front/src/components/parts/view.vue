<template>
  <div>
    <div class="grid">
      <div class="col-6">
        <div class="grid">
          <div class="col-3"><b>Qty:</b> {{ part.stock_qty }}</div>
          <div class="col-3"><b>Qty min:</b> {{ part.stock_qty_min }}</div>
          <div class="col-6"><b>Unit: </b> {{ partUnit }}</div>
        </div>

        <div class="mt-2 mb-2 surface-50 p-2">{{ part.description }}</div>

        <div>
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

        <div>
          <DataTable
            :value="mainTableItems"
            class="p-datatable-sm"
            stripedRows
            responsiveLayout="scroll"
          >
            <Column field="item"></Column>
            <Column field="value"></Column>
          </DataTable>
        </div>
      </div>

      <div class="col-6">
        <TabView :scrollable="true">
          <TabPanel>
            <template #header>
              <span>Parameters</span>
            </template>
            coin
          </TabPanel>

          <TabPanel>
            <template #header>
              <span>Distributors</span>
            </template>
            yyy
          </TabPanel>

          <TabPanel>
            <template #header>
              <span>Manufacturers</span>
            </template>
            zzz
          </TabPanel>

          <TabPanel>
            <template #header>
              <span>Files</span>
            </template>
            111
          </TabPanel>

          <TabPanel>
            <template #header>
              <span>Stock history</span>
            </template>
            222
          </TabPanel>
        </TabView>
      </div>
    </div>
  </div>
</template>

<script>
import dateFnsFormat from "date-fns/format";
import dateFnsParseISO from "date-fns/parseISO";

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
          item: "Footprint:",
          value: this.part.footprint ? this.part.footprint.name : "",
        },
        {
          item: "Storage:",
          value: this.part.storage ? this.part.storage.name : "",
        },
        {
          item: "Category:",
          value: this.part.category ? this.part.category.name : "",
        },
        {
          item: "Internal part number:",
          value: this.part.internal_part_number || "",
        },
        { item: "Comment:", value: this.part.comment || "" },
        {
          item: "Production remarks:",
          value: this.part.production_remarks || "",
        },
        {
          item: "Sheet Need review:",
          value: this.part.needs_review ? "yes" : "no",
        },
        { item: "Part Condition:", value: this.part.condition || "" },
        { item: "Can be sold:", value: this.part.can_be_sold ? "yes" : "no" },
        { item: "Added:", value: this.formatDate(this.part.created_at) },
        { item: "Updated:", value: this.formatDate(this.part.updated_at) },
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
  },
};
</script>
