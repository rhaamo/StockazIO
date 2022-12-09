<template>
  <div v-if="part">
    <div class="grid">
      <div class="col-6">
        <span
          style="float: left"
          class="pt-2"
          @click="showLabelGenerator(part)"
        >
          <vue-qrcode
            :id="qrcodeId(part.id)"
            v-tooltip="'click to show label generator'"
            :value="qrCodePart(part.uuid)"
            :options="{ scale: 1 }"
            :data-uuid="part.uuid"
            :data-name="part.name"
          />
        </span>

        <h3>
          <i v-if="part.private" class="fa icon-private fa-lock mr-2" />
          {{ part.name }}
        </h3>
      </div>
      <div class="col-1 col-offset-5">
        <router-link
          :to="{
            name: 'parts-edit',
            params: { partId: part.id },
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
          class="p-button-danger ml-2"
          v-tooltip="'delete'"
          @click="deletePart($event, part)"
        ></PvButton>
      </div>
    </div>

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
          <div class="col-6">
            <b>Unit: </b> {{ partUnit || "None defined" }}
          </div>
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
              <PvImage
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
                <template #body="slotProps"
                  >{{ slotProps.data.value }}
                  {{
                    slotProps.data.unit
                      ? `${slotProps.data.unit.name} (${slotProps.data.unit.symbol})`
                      : ""
                  }}</template
                >
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

            <form
              enctype="multipart/form-data"
              @submit.prevent="addAttachment(!v$.$invalid)"
            >
              <div class="grid">
                <div class="col-5">
                  <InputText
                    ref="description"
                    inputId="description"
                    type="text"
                    v-model="formAddAttachment.description"
                    placeholder="File description"
                    :class="{
                      'p-invalid':
                        v$.formAddAttachment.description.$invalid &&
                        formAddAttachmentSubmitted,
                      'w-12': true,
                    }"
                  />
                  <small
                    v-if="
                      (v$.formAddAttachment.description.$invalid &&
                        formAddAttachmentSubmitted) ||
                      v$.formAddAttachment.description.$pending.$response
                    "
                    class="p-error"
                  >
                    {{ v$.formAddAttachment.description.required.$message }}
                    <template
                      v-if="
                        v$.formAddAttachment.description.required &&
                        v$.formAddAttachment.description.maxLength
                      "
                      ><br
                    /></template>
                    {{ v$.formAddAttachment.description.maxLength.$message }}
                  </small>
                </div>

                <div class="col-6">
                  <InputText
                    ref="file"
                    inputId="file"
                    type="file"
                    v-model="formAddAttachment.file"
                    @change="attachmentFileChanged($event.target.files)"
                    :class="{
                      'p-invalid':
                        v$.formAddAttachment.file.$invalid &&
                        formAddAttachmentSubmitted,
                      'w-12': true,
                    }"
                    :accept="allowedUploadTypes"
                  />
                  <small
                    v-if="
                      (v$.formAddAttachment.file.$invalid &&
                        formAddAttachmentSubmitted) ||
                      v$.formAddAttachment.file.$pending.$response
                    "
                    class="p-error"
                  >
                    {{ v$.formAddAttachment.file.required.$message }}
                  </small>
                </div>

                <div class="col-1">
                  <PvButton label="add" type="submit" />
                </div>
              </div>
            </form>

            <Divider />
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
                    <i class="fa fa-picture-o mr-1"></i>
                    <a :href="slotProps.data.picture">{{
                      stripPathFromFileUrl(slotProps.data.picture)
                    }}</a>
                  </template>
                  <template v-else>
                    <i class="fa fa-code-o"></i>
                    <a class="no-underline" :href="slotProps.data.file">{{
                      stripPathFromFileUrl(slotProps.data.file)
                    }}</a>
                  </template>
                </template></Column
              >
              <Column field="description" header="Description"> </Column>
              <Column>
                <template #body="slotProps">
                  <template
                    v-if="
                      slotProps.data.picture && slotProps.data.picture_medium
                    "
                  >
                    <i
                      v-if="slotProps.data.picture_default"
                      class="fa fa-check-square-o"
                      title="Default picture"
                      aria-hidden="true"
                    />
                    <i
                      v-else
                      class="fa fa-square-o"
                      aria-hidden="true"
                      title="Set as default picture"
                      @click.prevent="
                        setAttachmentAsDefault(part.id, slotProps.data.id)
                      "
                    />
                    &nbsp;&nbsp;
                  </template>
                  <router-link
                    to="#"
                    @click.prevent="deleteAttachment(slotProps.data)"
                  >
                    <i class="fa fa-trash-o" aria-hidden="true" />
                  </router-link>
                </template>
              </Column>
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
import apiService from "@/services/api/api.service";
import logger from "@/logging";
import { useToast } from "primevue/usetoast";
import LabelGeneratorModal from "@/components/label/generator.vue";
import { h } from "vue";
import { useConfirm } from "primevue/useconfirm";
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";
import { mapState } from "pinia";
import { usePreloadsStore } from "@/stores/preloads";
import { useServerStore } from "@/stores/server";

export default {
  props: {
    node: Number,
  },
  data: () => ({
    part: null,
    formAddAttachmentSubmitted: false,
    formAddAttachment: {
      description: null,
      file: null,
    },
  }),
  setup: () => ({
    v$: useVuelidate(),
    toast: useToast(),
    confirm: useConfirm(),
    preloadsStore: usePreloadsStore(),
    serverStore: useServerStore(),
  }),
  created() {
    this.fetchPart();
  },
  validations: {
    formAddAttachment: {
      description: {
        required,
        maxLength: maxLength(255),
      },
      file: {
        required,
      },
    },
  },
  computed: {
    ...mapState(useServerStore, {
      allowedUploadTypes: (store) => {
        let types = store.settings.partAttachmentAllowedTypes || [
          "application/pdf",
          "image/jpeg",
        ];
        return types.join(", ");
      },
    }),
    partId() {
      return this.$route.params.partId;
    },
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
    fetchPart() {
      apiService
        .getPart(this.partId)
        .then((res) => {
          this.part = res.data;
        })
        .catch((err) => {
          if (err.request.status === 404) {
            this.$router.push({ name: "parts-list" });
            this.toast.add({
              severity: "error",
              summary: "Fetching part details",
              detail: "Part not found",
              life: 5000,
            });
            return;
          }

          this.toast.add({
            severity: "error",
            summary: "Fetching part details",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with part fetch", err.message);
        });
    },
    formatDate(date) {
      return dateFnsFormat(dateFnsParseISO(date), "E MMM d yyyy HH:mm");
    },
    stripPathFromFileUrl(url) {
      return utils.baseName(url);
    },
    qrcodeId(id, size) {
      return size ? `qrcode-${id}-${size}` : `qrcode-${id}`;
    },
    qrCodePart(uuid) {
      return `web+stockazio:part,${uuid}`;
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
        },
      });
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
              this.preloadsStore.decrementCategoryPartsCount(this.categoryId);
              this.$router.push({ name: "parts-list" });
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Deleting part",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part deletion", err);
              this.$router.push({ name: "parts-list" });
            });
        },
        reject: () => {
          return;
        },
      });
    },
    attachmentFileChanged(files) {
      this.formAddAttachment.realFile = files[0];
    },
    addAttachment(isFormValid) {
      this.formAddAttachmentSubmitted = true;
      if (!isFormValid) {
        return;
      }

      apiService
        .partAttachmentCreate(this.part.id, {
          description: this.formAddAttachment.description,
          file: this.formAddAttachment.realFile,
        })
        .then((val) => {
          this.toast.add({
            severity: "success",
            summary: "Part attachment",
            detail: "Upload successfull",
            life: 5000,
          });
          this.fetchPart();
          this.formAddAttachment = { description: null, file: null };
          this.formAddAttachmentSubmitted = false;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Part attachment",
            detail: "Error occured or file type not allowed.",
            life: 5000,
          });
          logger.default.error("Error with part attachment deletion", err);
        });
    },
    setAttachmentAsDefault(partId, fileId) {
      apiService
        .partAttachmentSetDefault(partId, fileId)
        .then((val) => {
          this.toast.add({
            severity: "success",
            summary: "Part attachment",
            detail: "Set as default with success",
            life: 5000,
          });
          this.fetchPart();
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Part attachment",
            detail: "Set as default failed",
            life: 5000,
          });
          logger.default.error("Error with part attachment default set", err);
          this.fetchPart();
        });
    },
    deleteAttachment(attachment) {
      this.confirm.require({
        message: `Are you sure you want to delete the attachment '${attachment.description}' ?`,
        header: `Deleting '${attachment.description}' ?`,
        icon: "fa fa-exclamation-triangle",
        accept: () => {
          apiService
            .partAttachmentDelete(this.part.id, attachment.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Part attachment",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchPart();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Part attachment",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part attachment deletion", err);
              this.fetchPart();
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
