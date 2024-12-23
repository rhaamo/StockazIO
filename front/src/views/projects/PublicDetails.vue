<template>
  <div>
    <Breadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />
    <div class="mt-2" v-if="project">
      <div class="grid">
        <div class="col-6">
          <h3>
            <i v-if="!project.public" class="fa icon-private fa-lock mr-2" />
            {{ project.name }}
          </h3>
        </div>
        <div class="col-1 col-offset-5"></div>
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
          <PvButton
            label="Project infos (text)"
            class="p-button-info"
            @click.prevent="exportProject('infos_txt')"
          />
          <PvButton
            label="BOM (CSV)"
            class="p-button-info ml-2"
            @click.prevent="exportProject('bom_csv')"
          />
          <PvButton
            label="BOM (Excel)"
            class="p-button-info ml-2"
            @click.prevent="exportProject('bom_xlsx')"
          />
        </div>

        <div class="col-8">
          <TabView>
            <TabPanel header="Parts">
              <div class="mt-1">
                <label for="boards_count" class="block">Boards:</label>
                <InputNumber
                  inputId="boards_count"
                  v-model="boards_count"
                  showButtons
                  buttonLayout="horizontal"
                  :step="1"
                  :min="1"
                  class="w-4"
                ></InputNumber>
              </div>

              <Divider />

              <DataTable
                :value="project.project_parts"
                class="p-datatable-sm"
                stripedRows
                responsiveLayout="scroll"
                :paginator="false"
                removableSort
              >
                <Column header="Name" :sortable="false">
                  <template #body="slotProps">
                    <span v-if="slotProps.data.part">{{
                      slotProps.data.part.name
                    }}</span>
                    <span v-else>{{ slotProps.data.part_name }}</span>
                    <template
                      v-if="
                        slotProps.data.part && slotProps.data.part.description
                      "
                    >
                      <br />
                      {{ slotProps.data.part.description }}
                    </template>
                  </template>
                </Column>

                <Column header="Notes" field="notes" :sortable="false">
                </Column>

                <Column
                  header="Stock"
                  :sortable="false"
                  headerStyle="width: 6em"
                >
                  <template #body="slotProps">
                    <template v-if="slotProps.data.part">
                      <span
                        v-if="
                          slotProps.data.part.stock_qty < slotProps.data.qty
                        "
                        class="qtyMinWarning"
                        >{{ slotProps.data.part.stock_qty }}
                        <i
                          class="fa fa-circle"
                          aria-hidden="true"
                          v-tooltip="{
                            value: currentStockQuantityWarning(
                              slotProps.data.qty
                            ),
                          }"
                        />
                      </span>
                      <span v-else>{{ slotProps.data.part.stock_qty }}</span>
                    </template>
                    <span v-else>-</span>
                  </template>
                </Column>

                <Column
                  header="Quantity x1"
                  :sortable="false"
                  headerStyle="width: 6em"
                >
                  <template #body="slotProps">
                    <template v-if="slotProps.data.part">
                      <span
                        v-if="
                          slotProps.data.part.stock_qty < slotProps.data.qty
                        "
                        class="qtyMinWarning"
                        >{{ slotProps.data.qty }}
                        <i
                          class="fa fa-circle"
                          aria-hidden="true"
                          v-tooltip="{
                            value: currentStockQuantityWarning(
                              slotProps.data.part.stock_qty
                            ),
                          }"
                        />
                      </span>
                      <span v-else>{{ slotProps.data.qty }}</span>
                    </template>
                    <span v-else>{{ slotProps.data.qty }}</span>
                  </template>
                </Column>

                <Column
                  header="Quantity total"
                  :sortable="false"
                  headerStyle="width: 6em"
                >
                  <template #body="slotProps">
                    <template v-if="slotProps.data.part">
                      <span
                        v-if="
                          slotProps.data.part.stock_qty <
                          slotProps.data.qty * boards_count
                        "
                        class="qtyMinWarning"
                        >{{ slotProps.data.qty * boards_count }}
                        <i
                          class="fa fa-circle"
                          aria-hidden="true"
                          v-tooltip="{
                            value: currentStockQuantityWarning(
                              slotProps.data.part.stock_qty
                            ),
                          }"
                        />
                      </span>
                      <span v-else>{{
                        slotProps.data.qty * boards_count
                      }}</span>
                    </template>
                    <span v-else>{{ slotProps.data.qty * boards_count }}</span>
                  </template>
                </Column>

                <Column
                  header="Sourced"
                  field="sourced"
                  :sortable="true"
                  headerStyle="width: 6em"
                >
                  <template #body="slotProps">
                    <i
                      v-if="slotProps.data.sourced"
                      style="color: green"
                      class="fa fa-check"
                      aria-hidden="true"
                    />
                    <i
                      v-else
                      class="fa fa-close"
                      style="color: red"
                      aria-hidden="true"
                    />
                  </template>
                </Column>
              </DataTable>
            </TabPanel>

            <TabPanel header="Files attachments">
              <DataTable
                :value="project.project_attachments"
                class="p-datatable-sm"
                stripedRows
                responsiveLayout="scroll"
              >
                <Column header="Link"
                  ><template #body="slotProps">
                    <i class="fa fa-code-o"></i>
                    <a class="no-underline" :href="slotProps.data.file">{{
                      stripPathFromFileUrl(slotProps.data.file)
                    }}</a>
                  </template>
                </Column>
                <Column field="description" header="Description"> </Column>
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
import { useToast } from "primevue/usetoast";
import { h } from "vue";
import utils from "@/utils.js";
import Button from "primevue/button";
import PartViewModal from "@/components/parts/view.vue";

export default {
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
    boards_count: 1,
  }),
  setup: () => ({
    toast: useToast(),
  }),
  computed: {
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
          to: {
            name: "projects-details",
            params: { projectId: this.project.id },
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
    projectStateText(value) {
      let a = this.projectStates.filter(function (e) {
        return e.value === value;
      });
      return a && a.length ? a[0].text : "Error";
    },
    exportProject(kind) {
      if (kind === "infos_txt") {
        apiService.projectExportInfosTxt(
          this.project.id,
          `${this.project.name}.txt`
        );
      } else if (kind === "bom_csv") {
        apiService.projectExportBomCSV(
          this.project.id,
          `${this.project.name}__bom.csv`
        );
      } else if (kind === "bom_xlsx") {
        apiService.projectExportBomXLSX(
          this.project.id,
          `${this.project.name}__bom.xlsx`
        );
      }
    },
    stripPathFromFileUrl(url) {
      return utils.baseName(url);
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
