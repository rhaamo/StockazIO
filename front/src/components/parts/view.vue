<template>
  <div>
    <div class="grid">
      <div class="col-6">
        <div class="grid quantities">
          <div class="col-3"><b class="mr-1">Qty:</b><QuantityPopoverEditor :part="part" kind="qty" size="large" /></div>
          <div class="col-3"><b class="mr-1">Qty min:</b><QuantityPopoverEditor :part="part" kind="qty_min" size="large" /></div>
          <div class="col-6"><b>Unit: </b> {{ partUnit || "None defined" }}</div>
        </div>

        <div class="mt-2 mb-2 surface-50 p-2 description">
          {{ part.description || "No description" }}
        </div>

        <div>
          <DataTable :value="mainTableItems" class="p-datatable-sm" striped-rows responsive-layout="scroll">
            <Column field="item" header="Item" header-style="width: 20rem"></Column>
            <Column field="value" header="Value"></Column>
          </DataTable>
        </div>

        <div>
          <h3>Used in projects:</h3>
          <PvButton v-if="!readonly" label="Add to project" size="small" severity="primary" @click.prevent="showAddToProject"></PvButton>

          <DataTable v-if="part && partProjects.length" :value="partProjects" class="p-datatable-sm mt-3" striped-rows responsive-layout="scroll">
            <Column field="name" header="Name" header-style="width: 20rem">
              <template #body="slotProps">
                <router-link
                  v-if="!readonly"
                  v-tooltip.left="'View project'"
                  :to="{
                    name: 'projects-details',
                    params: { projectId: slotProps.data.project_id },
                  }">
                  {{ slotProps.data.name }}
                </router-link>
                <template v-else>{{ slotProps.data.name }}</template>
              </template>
            </Column>
            <Column field="qty" header="Quantity (one board)" header-style="width: 11rem"></Column>
            <Column field="sourced" header="Sourced" header-style="width: 1rem">
              <template #body="slotProps">
                <div v-if="slotProps.data.sourced"><i class="pi pi-check"></i></div>
                <div v-else><i class="pi pi-times"></i></div>
              </template>
            </Column>
            <Column field="notes" header="Notes" header-style="width: 25rem">
              <template #body="slotProps">
                {{ slotProps.data.notes }}
              </template></Column
            >
            <Column v-if="!readonly" :sortable="false" header-style="min-width: 2em">
              <template #body="slotProps">
                <span class="p-buttonset">
                  <PvButton
                    v-tooltip.right="'Remove from project'"
                    severity="danger"
                    @click.prevent="deletePartFromProject($event, slotProps.data)"
                    icon="pi pi-trash"
                    class="ml-1" />
                </span>
              </template>
            </Column>
          </DataTable>
          <div v-else class="mt-3">None.</div>
        </div>
      </div>

      <div class="col-6">
        <div class="mb-3">
          <Galleria :value="pictureAttachments" container-style="max-width: 640px">
            <template #item="slotProps">
              <PvImage preview height="100" :src="slotProps.item.picture" :alt="slotProps.item.description" />
            </template>
            <template #thumbnail="slotProps">
              <img :src="slotProps.item.picture_medium" :alt="slotProps.item.description" style="height: 60px" />
            </template>
          </Galleria>
        </div>

        <Tabs value="0" scrollable>
          <TabList>
            <Tab value="0">Parameters</Tab>
            <Tab value="1">Distributors</Tab>
            <Tab value="2">Manufacturers</Tab>
            <Tab value="3">Files</Tab>
            <Tab value="4">Stock History</Tab>
          </TabList>
          <TabPanels>
            <!-- Parameters -->
            <TabPanel value="0">
              <DataTable :value="part.part_parameters_value" class="p-datatable-sm" striped-rows responsive-layout="scroll">
                <Column field="name" header="Name"></Column>
                <Column field="description" header="Description"></Column>
                <Column header="Value">
                  <template #body="slotProps"
                    >{{ slotProps.data.value }}
                    {{ slotProps.data.unit ? `${slotProps.data.unit.name} (${slotProps.data.unit.symbol})` : "" }}</template
                  >
                </Column>
              </DataTable>
            </TabPanel>
            <TabPanel value="1">
              <DataTable :value="part.distributors_sku" class="p-datatable-sm" striped-rows responsive-layout="scroll">
                <Column field="sku" header="SKU"></Column>
                <Column header="Distributor">
                  <template #body="slotProps">{{ slotProps.data.distributor ? slotProps.data.distributor.name : "No name" }}</template>
                </Column>
                <Column header="Datasheet">
                  <template #body="slotProps">
                    <template v-if="slotProps.data.datasheet_url">
                      <a :href="slotProps.data.datasheet_url" target="_blank"
                        ><i class="pi pi-file-pdf"></i> {{ slotProps.data.datasheet_url }}</a
                      ></template
                    ></template
                  >
                </Column>
              </DataTable>
            </TabPanel>
            <TabPanel value="2">
              <DataTable :value="part.manufacturers_sku" class="p-datatable-sm" striped-rows responsive-layout="scroll">
                <Column field="sku" header="SKU"></Column>
                <Column header="Manufacturer">
                  <template #body="slotProps">{{ slotProps.data.manufacturer ? slotProps.data.manufacturer.name : "No name" }}</template>
                </Column>
                <Column header="Datasheet">
                  <template #body="slotProps">
                    <template v-if="slotProps.data.datasheet_url">
                      <a :href="slotProps.data.datasheet_url" target="_blank"
                        ><i class="pi pi-file-pdf"></i> {{ slotProps.data.datasheet_url }}</a
                      ></template
                    ></template
                  >
                </Column>
              </DataTable>
            </TabPanel>
            <TabPanel value="3">
              <DataTable :value="part.part_attachments" class="p-datatable-sm" striped-rows responsive-layout="scroll">
                <Column header="Link"
                  ><template #body="slotProps">
                    <template v-if="slotProps.data.picture && slotProps.data.picture_medium">
                      <i class="pi pi-image"></i>
                      <a class="no-underline ml-2" :href="slotProps.data.picture">{{ stripPathFromFileUrl(slotProps.data.picture) }}</a>
                    </template>
                    <template v-else>
                      <i class="pi pi-file"></i>
                      <a class="no-underline" :href="slotProps.data.file">{{ stripPathFromFileUrl(slotProps.data.file) }}</a>
                    </template>
                  </template></Column
                >
                <Column field="description" header="Description"> </Column>
              </DataTable>
            </TabPanel>
            <TabPanel value="4">
              <DataTable :value="part.part_stock_history" class="p-datatable-sm" striped-rows responsive-layout="scroll">
                <Column field="created_at" header="Date"
                  ><template #body="slotProps">{{ formatDate(slotProps.data.created_at) }}</template></Column
                >
                <Column field="diff" header="Amount"> </Column>
              </DataTable>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </div>
    </div>
  </div>
</template>

<script>
import { format as dateFnsFormat } from "date-fns/format";
import { parseISO as dateFnsParseISO } from "date-fns/parseISO";
import utils from "@/utils.js";
import QuantityPopoverEditor from "@/components/parts/QuantityPopoverEditor.vue";
import apiService from "@/services/api/api.service";
import logger from "@/logging";
import AddToProjectModal from "@/components/parts/AddToProjectModal.vue";
import { h } from "vue";

export default {
  inject: ["dialogRef"],
  components: {
    QuantityPopoverEditor,
  },
  data: () => ({
    part: null,
    readonly: true,
  }),
  computed: {
    partUnit() {
      if (this.part && this.part.part_unit) {
        if (this.part.part_unit.short_name) {
          return `${this.part.part_unit.name} (${this.part.part_unit.short_name})`;
        } else {
          return this.part.part_unit.name;
        }
      }
      return "No unit defined";
    },
    mainTableItems() {
      return [
        {
          item: "Footprint",
          value: this.part.footprint ? this.part.footprint.name : "",
        },
        {
          item: "Storage",
          value: this.part.storage ? this.part.storage_path.join(" / ") : "-",
        },
        {
          item: "Category",
          value: this.part.category ? this.part.category_path.join(" / ") : "Uncategorized",
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
    partProjects() {
      return this.part.projectpart_set.map((x) => {
        return { id: x.id, name: x.project.name, notes: x.notes, qty: x.qty, project_id: x.project.id, sourced: x.sourced };
      });
    },
  },
  created() {
    this.part = this.dialogRef.data.part;
    if (typeof this.dialogRef.data.readonly !== "undefined") {
      this.readonly = this.dialogRef.data.readonly;
    }
  },
  methods: {
    reloadPart() {
      apiService
        .getPart(this.part.id)
        .then((val) => {
          this.part = val.data;
        })
        .catch((err) => {
          this.$toast.add({
            severity: "error",
            summary: "Part details",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with getting part details", err);
        });
    },
    formatDate(date) {
      return dateFnsFormat(dateFnsParseISO(date), "E MMM d yyyy HH:mm");
    },
    stripPathFromFileUrl(url) {
      return utils.baseName(url);
    },
    showAddToProject() {
      this.$dialog.open(AddToProjectModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Add to project")])];
          },
        },
        data: {
          part: this.part,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            this.reloadPart();
          }
        },
      });
    },
    deletePartFromProject(event, item) {
      this.$confirm.require({
        message: `Are you sure you want to delete the part '${this.part.name}' from project '${item.name}' ?`,
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
            .projectDeletePart(item.project_id, item.id)
            .then((val) => {
              this.$toast.add({
                severity: "success",
                summary: "Part",
                detail: "Deleted",
                life: 5000,
              });
              this.reloadPart();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Part",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part deletion from project", err);
              this.reloadPart();
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

<style lang="scss" scoped>
.quantities {
  font-size: 1.5rem;
}

.description {
  font-size: 1.2rem;
}
</style>
