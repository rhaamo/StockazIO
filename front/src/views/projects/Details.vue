<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div v-if="project" class="mt-2">
      <div class="grid">
        <div class="col-6">
          <h3>
            <i v-if="!project.public" class="pi pi-lock mr-2" />
            <router-link v-if="project.public" :to="{ name: 'public-projects-details' }">
              <i v-tooltip.left="'public link'" class="pi pi-globe mr-2" />
            </router-link>
            {{ project.name }}
          </h3>
        </div>
        <div class="col-1 col-offset-5">
          <ButtonsEditDelete @edit="showEditModal($event)" @delete="deleteItem($event)" />
        </div>
      </div>

      <div class="grid">
        <div class="col-4">
          <div v-if="project.ibom_url">
            <b>Interactive BOM Url:</b>
            <a :href="project.ibom_url" target="_blank" class="ml-1">here</a>
          </div>

          <div class="mt-2">
            <b>State:</b>
            <span class="ml-1">{{ projectStateText(project.state) }}</span>
            <div v-if="project.state_notes" class="pl-2">
              {{ project.state_notes }}
            </div>
          </div>

          <div class="mt-2">
            <b>Description:</b>
            <div class="pl-2">
              {{ project.description || "None" }}
            </div>
          </div>

          <div class="mt-2">
            <b>Notes:</b>
            <div class="pl-2">
              {{ project.notes || "None" }}
            </div>
          </div>

          <Divider />

          <h4>Exports:</h4>
          <PvButton label="Project infos (text)" class="p-button-info" @click.prevent="exportProject('infos_txt')" />
          <PvButton label="BOM (CSV)" class="p-button-info ml-2" @click.prevent="exportProject('bom_csv')" />
          <PvButton label="BOM (Excel)" class="p-button-info ml-2" @click.prevent="exportProject('bom_xlsx')" />
        </div>

        <div class="col-8">
          <TabView>
            <TabPanel header="Parts">
              <div>
                <PvButton label="Add part from inventory" @click.prevent="showAddInternalPart($event)" />
                <PvButton class="p-button-info ml-2" label="Add external part" @click.prevent="showAddExternalPart($event)" />
              </div>

              <div class="mt-1">
                <label for="boards_count" class="block">Boards:</label>
                <InputNumber
                  v-model="boards_count"
                  input-id="boards_count"
                  show-buttons
                  button-layout="horizontal"
                  :step="1"
                  :min="1"
                  class="w-4"></InputNumber>
              </div>

              <Divider />

              <DataTable
                :value="project.project_parts"
                class="p-datatable-sm"
                striped-rows
                responsive-layout="scroll"
                :paginator="false"
                removable-sort>
                <Column header="Name" :sortable="false">
                  <template #body="slotProps">
                    <a v-if="slotProps.data.part" href="#" class="no-underline" @click.prevent="viewPartModal(slotProps.data.part)">{{
                      slotProps.data.part.name
                    }}</a>
                    <span v-else>{{ slotProps.data.part_name }}</span>
                    <template v-if="slotProps.data.part && slotProps.data.part.description">
                      <br />
                      {{ slotProps.data.part.description }}
                    </template>
                  </template>
                </Column>

                <Column header="Notes" field="notes" :sortable="false"> </Column>

                <Column header="Stock" :sortable="false" header-style="width: 6em">
                  <template #body="slotProps">
                    <template v-if="slotProps.data.part">
                      <span v-if="slotProps.data.part.stock_qty < slotProps.data.qty" class="qtyMinWarning"
                        >{{ slotProps.data.part.stock_qty }}
                        <i
                          v-tooltip="{
                            value: currentStockQuantityWarning(slotProps.data.qty),
                          }"
                          class="pi pi-circle-fill"
                          aria-hidden="true" />
                      </span>
                      <span v-else>{{ slotProps.data.part.stock_qty }}</span>
                    </template>
                    <span v-else>-</span>
                  </template>
                </Column>

                <Column header="Quantity x1" :sortable="false" header-style="width: 6em">
                  <template #body="slotProps">
                    <template v-if="slotProps.data.part">
                      <span v-if="slotProps.data.part.stock_qty < slotProps.data.qty" class="qtyMinWarning"
                        >{{ slotProps.data.qty }}
                        <i
                          v-tooltip="{
                            value: currentStockQuantityWarning(slotProps.data.part.stock_qty),
                          }"
                          class="pi pi-circle-fill"
                          aria-hidden="true" />
                      </span>
                      <span v-else>{{ slotProps.data.qty }}</span>
                    </template>
                    <span v-else>{{ slotProps.data.qty }}</span>
                  </template>
                </Column>

                <Column header="Quantity total" :sortable="false" header-style="width: 6em">
                  <template #body="slotProps">
                    <template v-if="slotProps.data.part">
                      <span v-if="slotProps.data.part.stock_qty < slotProps.data.qty * boards_count" class="qtyMinWarning"
                        >{{ slotProps.data.qty * boards_count }}
                        <i
                          v-tooltip="{
                            value: currentStockQuantityWarning(slotProps.data.part.stock_qty),
                          }"
                          class="pi pi-circle-fill"
                          aria-hidden="true" />
                      </span>
                      <span v-else>{{ slotProps.data.qty * boards_count }}</span>
                    </template>
                    <span v-else>{{ slotProps.data.qty * boards_count }}</span>
                  </template>
                </Column>

                <Column header="Sourced" field="sourced" :sortable="true" header-style="width: 6em">
                  <template #body="slotProps">
                    <i v-if="slotProps.data.sourced" style="color: green" class="pi pi-check" aria-hidden="true" />
                    <i v-else class="pi pi-times" style="color: red" aria-hidden="true" />
                  </template>
                </Column>

                <Column header-style="width: 6.3em">
                  <template #body="slotProps">
                    <ButtonsEditDelete @edit="showEditPart($event, slotProps.data)" @delete="deletePart($event, slotProps.data)" />
                  </template>
                </Column>
              </DataTable>
            </TabPanel>

            <TabPanel header="Files attachments">
              <form enctype="multipart/form-data" @submit.prevent="addAttachment(!v$.$invalid)">
                <div class="grid">
                  <div class="col-5">
                    <InputText
                      ref="description"
                      v-model="formAddAttachment.description"
                      input-id="description"
                      type="text"
                      placeholder="File description"
                      :invalid="v$.formAddAttachment.description.$invalid && formAddAttachmentSubmitted"
                      fluid />
                    <small
                      v-if="
                        (v$.formAddAttachment.description.$invalid && formAddAttachmentSubmitted) ||
                        v$.formAddAttachment.description.$pending.$response
                      "
                      class="p-error">
                      {{ v$.formAddAttachment.description.required.$message }}
                      <template v-if="v$.formAddAttachment.description.required && v$.formAddAttachment.description.maxLength"><br /></template>
                      {{ v$.formAddAttachment.description.maxLength.$message }}
                    </small>
                  </div>

                  <div class="col-6">
                    <InputText
                      ref="file"
                      v-model="formAddAttachment.file"
                      input-id="file"
                      type="file"
                      :invalid="v$.formAddAttachment.file.$invalid && formAddAttachmentSubmitted"
                      fluid
                      :accept="allowedUploadTypes"
                      @change="attachmentFileChanged($event.target.files)" />
                    <small
                      v-if="(v$.formAddAttachment.file.$invalid && formAddAttachmentSubmitted) || v$.formAddAttachment.file.$pending.$response"
                      class="p-error">
                      {{ v$.formAddAttachment.file.required.$message }}
                    </small>
                  </div>

                  <div class="col-1">
                    <PvButton label="add" type="submit" />
                  </div>
                </div>
              </form>

              <Divider />
              <DataTable :value="project.project_attachments" class="p-datatable-sm" striped-rows responsive-layout="scroll">
                <Column header="Link">
                  <template #body="slotProps">
                    <i class="pi pi-file mr-2"></i>
                    <a class="no-underline" :href="slotProps.data.file">{{ stripPathFromFileUrl(slotProps.data.file) }}</a>
                  </template>
                </Column>
                <Column field="description" header="Description"> </Column>
                <Column>
                  <template #body="slotProps">
                    <PvButton severity="danger" icon="pi pi-trash" @click.prevent="deleteAttachment(slotProps.data)"></PvButton>
                  </template>
                </Column>
              </DataTable>
            </TabPanel>
          </TabView>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import logger from "@/logging";
import apiService from "@/services/api/api.service";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import ManageProjectModal from "@/components/project/Form.vue";
import ExternalPart from "@/components/project/ExternalPart.vue";
import InternalPart from "@/components/project/InternalPart.vue";
import { h } from "vue";
import utils from "@/utils.js";
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength } from "@vuelidate/validators";
import { mapState } from "pinia";
import { useServerStore } from "@/stores/server";
import Button from "primevue/button";
import PartViewModal from "@/components/parts/view.vue";
import ButtonsEditDelete from "@/components/btn_edit_delete.vue";

export default {
  setup: () => ({
    confirm: useConfirm(),
    toast: useToast(),
    serverStore: useServerStore(),
    v$: useVuelidate(),
  }),
  components: {
    ButtonsEditDelete,
  },
  data: () => ({
    project: null,
    projectStates: [
      { value: 1, text: "Planned" },
      { value: 2, text: "Ongoing" },
      { value: 3, text: "Finished" },
      { value: 4, text: "On-Hold" },
      { value: 5, text: "Abandonned" },
      { value: 99, text: "Unknown" },
      { value: null, text: "Filter by state" },
    ],
    formAddAttachmentSubmitted: false,
    formAddAttachment: {
      description: null,
      file: null,
    },
    boards_count: 1,
  }),
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
        let types = store.settings.partAttachmentAllowedTypes || ["application/pdf", "image/jpeg"];
        return types.join(", ");
      },
    }),
    projectId() {
      return this.$route.params.projectId;
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
            label: "Projects",
            command: () => {
              this.$router.push({ name: "projects-list" });
            },
          },
        ],
      };
      if (this.project) {
        bc.items.push({
          label: this.project.name,
          command: () => {
            this.$router.push({
              name: "projects-details",
              params: { projectId: this.project.id },
            });
          },
        });
      }
      return bc;
    },
  },
  mounted() {
    this.fetchProject();
  },
  methods: {
    fetchProject() {
      apiService
        .getProject(this.projectId)
        .then((res) => {
          this.project = res.data;
        })
        .catch((err) => {
          if (err.request.status === 404) {
            this.$router.push({ name: "projects-list" });
            this.toast.add({
              severity: "error",
              summary: "Fetching project details",
              detail: "Project not found",
              life: 5000,
            });
            return;
          }

          this.toast.add({
            severity: "error",
            summary: "Fetching project details",
            detail: "An error occured, please try again later",
            life: 5000,
          });
          logger.default.error("Error with project fetch", err.message);
        });
    },
    showEditModal(event) {
      this.$dialog.open(ManageProjectModal, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Edit project")])];
          },
        },
        data: {
          mode: "edit",
          item: this.project,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload project
            this.fetchProject();
          }
        },
      });
    },
    deleteItem(event) {
      this.confirm.require({
        message: `Are you sure you want to delete the project '${this.project.name}' ?`,
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
            .deleteProject(this.project.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Project",
                detail: "Deleted",
                life: 5000,
              });
              this.$router.push({ name: "projects-list" });
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Project",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with project deletion", err);
              this.$router.push({ name: "projects-list" });
            });
        },
        reject: () => {
          return;
        },
      });
    },
    deletePart(event, part) {
      let part_name = part.part ? part.part.name : part.part_name;

      this.confirm.require({
        message: `Are you sure you want to delete the part '${part_name}' ?`,
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
            .projectDeletePart(this.project.id, part.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Part",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchProject();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Part",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with part deletion", err);
              this.fetchProject();
            });
        },
        reject: () => {
          return;
        },
      });
    },
    projectStateText(value) {
      let a = this.projectStates.filter(function (e) {
        return e.value === value;
      });
      return a && a.length ? a[0].text : "Error";
    },
    exportProject(kind) {
      if (kind === "infos_txt") {
        apiService.projectExportInfosTxt(this.project.id, `${this.project.name}.txt`);
      } else if (kind === "bom_csv") {
        apiService.projectExportBomCSV(this.project.id, `${this.project.name}__bom.csv`);
      } else if (kind === "bom_xlsx") {
        apiService.projectExportBomXLSX(this.project.id, `${this.project.name}__bom.xlsx`);
      }
    },
    stripPathFromFileUrl(url) {
      return utils.baseName(url);
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
        .projectAttachmentCreate(this.project.id, {
          description: this.formAddAttachment.description,
          file: this.formAddAttachment.realFile,
        })
        .then((val) => {
          this.toast.add({
            severity: "success",
            summary: "Project attachment",
            detail: "Upload successfull",
            life: 5000,
          });
          this.fetchProject();
          this.formAddAttachment = { description: null, file: null };
          this.formAddAttachmentSubmitted = false;
        })
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Project attachment",
            detail: "Error occured or file type not allowed.",
            life: 5000,
          });
          this.fetchProject();
          logger.default.error("Error with project attachment deletion", err);
        });
    },
    deleteAttachment(attachment) {
      this.confirm.require({
        message: `Are you sure you want to delete the attachment '${attachment.description}' ?`,
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
            .projectAttachmentDelete(this.project.id, attachment.id)
            .then((val) => {
              this.toast.add({
                severity: "success",
                summary: "Project attachment",
                detail: "Deleted",
                life: 5000,
              });
              this.fetchProject();
            })
            .catch((err) => {
              this.toast.add({
                severity: "error",
                summary: "Project attachment",
                detail: "An error occured, please try again later",
                life: 5000,
              });
              logger.default.error("Error with project attachment deletion", err);
              this.fetchProject();
            });
        },
        reject: () => {
          return;
        },
      });
    },
    showAddExternalPart(event) {
      this.$dialog.open(ExternalPart, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Describe the part")])];
          },
        },
        data: {
          mode: "add",
          project: this.project,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload project
            this.fetchProject();
          }
        },
      });
    },
    showEditPart(event, item) {
      if (item.part) {
        this.showEditInternalPart(event, item);
      } else {
        this.showEditExternalPart(event, item);
      }
    },
    showEditExternalPart(event, item) {
      this.$dialog.open(ExternalPart, {
        props: {
          modal: true,
          style: {
            width: "25vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Describe the part")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
          project: this.project,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload project
            this.fetchProject();
          }
        },
      });
    },
    showAddInternalPart(event) {
      this.$dialog.open(InternalPart, {
        props: {
          modal: true,
          style: {
            width: "60vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Select part from inventory")])];
          },
        },
        data: {
          mode: "add",
          project: this.project,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload project
            this.fetchProject();
          }
        },
      });
    },
    showEditInternalPart(event, item) {
      this.$dialog.open(InternalPart, {
        props: {
          modal: true,
          style: {
            width: "60vw",
          },
          dismissableMask: true,
        },
        templates: {
          header: () => {
            return [h("h3", [h("span", "Select part from inventory")])];
          },
        },
        data: {
          mode: "edit",
          item: item,
          project: this.project,
        },
        onClose: (options) => {
          if (options.data && options.data.finished) {
            // reload project
            this.fetchProject();
          }
        },
      });
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
                      this.$router.replace({
                        name: "parts-details",
                        params: { partId: part.id },
                      });
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
    currentStockQuantityWarning(qty) {
      return `Current stock is below needed project quantity (${qty})`;
    },
  },
};
</script>
