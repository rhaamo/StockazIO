<template>
  <div class="project_details">
    <ManagePartInventoryModal
      :project="project" :part-to-edit="partToEdit" @manage-part-inventory-saved="onPartSaved"
      @manage-part-inventory-modal-closed="clearPartToEdit"
    />
    <ManagePartExternalModal
      :project="project" :part-to-edit="partToEdit" @manage-part-external-saved="onPartSaved"
      @manage-part-external-modal-closed="clearPartToEdit"
    />
    <ViewModal
      :part="partDetails" :can-delete="false"
      @view-part-modal-closed="onPartModalClosed"
    />

    <div v-if="project" class="row">
      <div class="col-lg-9">
        <h3>
          <i :class="projectPrivate" /> {{ project.name }}
        </h3>
      </div>
      <div class="col-lg-3">
        <b-button variant="link" :to="{ name: 'projects-edit', params: { projectId: project.id } }">
          <i
            class="fa fa-pencil-square-o"
            aria-hidden="true"
          />
        </b-button>
                &nbsp;
        <b-button variant="link" @click.prevent="deleteProject(project)">
          <i
            class="fa fa-trash-o"
            aria-hidden="true"
          />
        </b-button>
      </div>
    </div>

    <div v-if="project" class="row mt-3">
      <div class="col-md-4">
        <div class="row">
          <div v-if="project.ibom_url" class="col-md-6">
            <b>Interactive BOM Url:</b> <a :href="project.ibom_url" target="_blank">here</a>
          </div>
          <div class="col-md-6">
            <b>State:</b> <span class="unit">{{ projectStateText(project.state) }}</span>
            <div v-if="project.state_notes">
              {{ project.state_notes }}
            </div>
          </div>
        </div>

        <div class="row my-4">
          <div class="col-md-12">
            <b>Description:</b>
            <div class="description">
              {{ project.description || 'None' }}
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-md-12">
            <b>Notes:</b>
            <div class="description">
              {{ project.notes || 'None' }}
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <b-tabs content-class="mt-3">
          <b-tab title="Parts">
            <b-button variant="primary" @click.prevent="manageInventoryPart">
              Add part from inventory
            </b-button>
            &nbsp;
            <b-button variant="info" @click.prevent="manageExternalPart">
              Add external part
            </b-button>

            <div>
              <label for="boardsCount">Boards:</label>
              <b-form-spinbutton
                id="boardsCount" v-model="boards" min="1"
                class="w-25 ml-1"
              />
            </div>
            <hr>

            <b-table
              id="tableParts"
              :items="project.project_parts"
              :fields="partsFields"
              responsive="sm"
              striped
              primary-key="uuid"
              small
            >
              <template #cell(part_name)="data">
                <a v-if="data.item.part" href="#" @click.prevent="viewPartModal(data.item.part)">{{ data.item.part.name }}</a>
                <span v-else>{{ data.item.part_name }}</span>
                <template v-if="data.item.part && data.item.part.description">
                  <br>
                  {{ data.item.part.description }}
                </template>
              </template>

              <template #cell(sourced)="data">
                <i
                  v-if="data.item.sourced" style="color: green;" class="fa fa-check"
                  aria-hidden="true"
                />
                <i
                  v-else class="fa fa-close" style="color: red;"
                  aria-hidden="true"
                />
              </template>

              <template #cell(stock_qty)="data">
                <template v-if="data.item.part">
                  <span
                    v-if="(data.item.part.stock_qty < data.item.qty)"
                    class="qtyMinWarning"
                  >{{ data.item.part.stock_qty }}
                    <i
                      v-b-tooltip.hover class="fa fa-circle"
                      aria-hidden="true"
                      :title="currentStockQuantityWarning(data.item.qty)"
                    />
                  </span>
                  <span v-else>{{ data.item.part.stock_qty }}</span>
                </template>
                <span v-else>-</span>
              </template>

              <template #cell(qty)="data">
                <template v-if="data.item.part">
                  <span
                    v-if="(data.item.part.stock_qty < data.item.qty)"
                    class="qtyMinWarning"
                  >{{ data.item.qty }}
                    <i
                      v-b-tooltip.hover class="fa fa-circle"
                      aria-hidden="true"
                      :title="currentStockQuantityWarning(data.item.part.stock_qty)"
                    />
                  </span>
                  <span v-else>{{ data.item.qty }}</span>
                </template>
                <span v-else>{{ data.item.qty }}</span>
              </template>

              <template #cell(qty_total)="data">
                <template v-if="data.item.part">
                  <span
                    v-if="(data.item.part.stock_qty < data.item.qty*boards)"
                    class="qtyMinWarning"
                  >{{ data.item.qty*boards }}
                    <i
                      v-b-tooltip.hover class="fa fa-circle"
                      aria-hidden="true"
                      :title="currentStockQuantityWarning(data.item.part.stock_qty)"
                    />
                  </span>
                  <span v-else>{{ data.item.qty*boards }}</span>
                </template>
                <span v-else>{{ data.item.qty*boards }}</span>
              </template>

              <template #cell(actions)="data">
                <b-button variant="link" @click.prevent="editPart(data.item)">
                  <i
                    class="fa fa-pencil-square-o"
                    aria-hidden="true"
                  />
                </b-button>
                &nbsp;
                <b-button variant="link" @click.prevent="deletePart(data.item)">
                  <i
                    class="fa fa-trash-o"
                    aria-hidden="true"
                  />
                </b-button>
              </template>
            </b-table>
          </b-tab>

          <b-tab title="Files attachments">
            <b-form enctype="multipart/form-data" inline @submit.prevent="addAttachment">
              <label class="sr-only" for="description">Description</label>
              <b-form-group id="input-group-description" label-for="description">
                <b-form-input
                  id="description"
                  v-model="addAttachmentForm.description"
                  required
                  placeholder="File description"
                  class="mb-2 mr-sm-2 mb-sm-0"
                />
                <div v-if="!$v.addAttachmentForm.description.required" class="invalid-feedback d-block">
                  Description is required
                </div>
                <div v-if="!$v.addAttachmentForm.description.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>

              <label class="sr-only" for="file">File</label>
              <b-form-group id="input-group-file" label-for="file" class="mb-2 mr-sm-2 mb-sm-0">
                <b-form-file
                  id="file"
                  ref="file"
                  v-model="addAttachmentForm.file"
                  :accept="allowedUploadTypes"
                  required
                />
                <div v-if="!$v.addAttachmentForm.file.required" class="invalid-feedback d-block">
                  File is required
                </div>
              </b-form-group>

              <b-button
                class="mb-3" type="submit" variant="primary"
                size="sm"
              >
                Add
              </b-button>
            </b-form>
            <hr>

            <table id="table-files-attachments" class="table table-sm table-striped">
              <thead>
                <tr>
                  <th>Link</th>
                  <th>Description</th>
                  <th />
                </tr>
              </thead>
              <tbody v-if="project.project_attachments && project.project_attachments.length">
                <tr v-for="file in project.project_attachments" :key="file.id">
                  <td><a target="_blank" :href="file.file">{{ file.file }}</a></td>
                  <td>{{ file.description }}</td>
                  <td>
                    <b-button variant="link" @click.prevent="deleteAttachment(file)">
                      <i
                        class="fa fa-trash-o"
                        aria-hidden="true"
                      />
                    </b-button>
                  </td>
                </tr>
              </tbody>
            </table>
          </b-tab>

          <b-tab title="Exports">
            <h4>Project infos</h4>
            <b-button variant="info" @click.prevent="exportProject('infos_txt')">
              Text
            </b-button>

            <h4 class="mt-4">
              BOM
            </h4>
            <b-button variant="info" class="mr-2" @click.prevent="exportProject('bom_csv')">
              CSV
            </b-button>
            <b-button variant="info" @click.prevent="exportProject('bom_xlsx')">
              Excel
            </b-button>
          </b-tab>
        </b-tabs>
      </div>
    </div>
    <div v-else class="row">
      <div class="col-md-6">
        Project not yet loaded.
      </div>
    </div>
  </div>
</template>

<script>
import ManagePartInventoryModal from '@/components/parts/project_manage_inventory_modal'
import ManagePartExternalModal from '@/components/parts/project_manage_external_modal'
import ViewModal from '@/components/parts/view_modal'
import apiService from '../../services/api/api.service'
import logger from '@/logging'
import { mapState } from 'vuex'
import { validationMixin } from 'vuelidate'
import { required, maxLength } from 'vuelidate/lib/validators'
import { useToast } from 'vue-toastification'
import ToastyToast from '@/components/toasty-toast'

export default {
  name: 'ProjectsDetails',
  components: {
    ManagePartInventoryModal,
    ManagePartExternalModal,
    ViewModal
  },
  mixins: [ validationMixin ],
  props: {
  },
  validations: {
    addAttachmentForm: {
      description: {
        required, maxLength: maxLength(255)
      },
      file: {
        required
      }
    }
  },
  data: () => ({
    project: null,
    addAttachmentForm: {
      description: '',
      file: null
    },
    projectStates: [
      { value: 1, text: 'Planned' },
      { value: 2, text: 'Ongoing' },
      { value: 3, text: 'Finished' },
      { value: 4, text: 'On-Hold' },
      { value: 5, text: 'Abandonned' },
      { value: 99, text: 'Unknown' },
      { value: null, text: 'Filter by state' }
    ],
    partsFields: [
      { key: 'part_name', label: 'Part name', tdClass: 'part_name' },
      { key: 'notes', label: 'Notes', tdClass: 'notes' },
      { key: 'stock_qty', label: 'Stock', tdClass: 'stock_qty' },
      { key: 'qty', label: 'Quantity x1', tdClass: 'qty' },
      { key: 'qty_total', label: 'Quantity total', tdClass: 'qty_total' },
      { key: 'sourced', label: 'Sourced', tdClass: 'sourced' },
      { key: 'actions', label: 'Actions', tdClass: 'actions' }

    ],
    partDetails: null,
    boards: 1,
    partToEdit: null
  }),
  setup () {
    const toast = useToast()
    return { toast }
  },
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings
    }),
    projectId () {
      return this.$route.params.projectId
    },
    projectPrivate () { return this.project.public ? 'fa icon-private fa-unlock' : 'fa icon-private fa-lock' },
    allowedUploadTypes () {
      let types = this.serverSettings.partAttachmentAllowedTypes || ['application/pdf', 'image/jpeg']
      return types.join(', ')
    }
  },
  watch: {
  },
  created () {
    this.fetchProject()
  },
  methods: {
    currentStockQuantityWarning (qty) {
      return `Current stock is below needed project quantity (${qty})`
    },
    projectStateText (value) {
      let a = this.projectStates.filter(function (e) { return e.value === value })
      return a && a.length ? a[0].text : 'Error'
    },
    fetchProject () {
      apiService.getProject(this.projectId)
        .then((res) => {
          this.project = res.data
        })
        .catch((err) => {
          this.toast.error({
            component: ToastyToast,
            props: {
              title: this.$pgettext('Project/Details/Toast/Error/Title', 'Fetching project details'),
              message: this.$pgettext('Project/Details/Toast/Error/Message', 'An error occured, please try again later')
            }
          })
          logger.default.error('Error with project fetch', err.message)
        })
    },
    deleteProject (project) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the project '${project.name}' ?`, {
        title: 'Please Confirm',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'YES',
        cancelTitle: 'NO',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true
      })
        .then((value) => {
          if (value === false) { return }

          apiService.deleteProject(project.id)
            .then((val) => {
              this.toast.success({
                component: ToastyToast,
                props: {
                  title: this.$pgettext('Project/Delete/Toast/Success/Title', 'Deleting project'),
                  message: this.$pgettext('Project/Delete/Toast/Success/Message', 'Success')
                }
              })
              this.$router.push({ name: 'projects-list' })
            })
            .catch((err) => {
              this.toast.error({
                component: ToastyToast,
                props: {
                  title: this.$pgettext('Project/Delete/Toast/Error/Title', 'Deleting project'),
                  message: this.$pgettext('Project/Delete/Toast/Error/Message', 'An error occured, please try again later')
                }
              })
              logger.default.error('Error with project deletion', err)
              this.fetchProject()
            })
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    },
    addAttachment () {
      this.$v.addAttachmentForm.$touch()
      if (this.$v.addAttachmentForm.$invalid) { return }

      apiService.projectAttachmentCreate(this.project.id, this.addAttachmentForm)
        .then((val) => {
          this.toast.success({
            component: ToastyToast,
            props: {
              title: this.$pgettext('ProjectAttachment/Create/Toast/Success/Title', 'Saving project attachment'),
              message: this.$pgettext('ProjectAttachment/Create/Toast/Success/Message', 'Success')
            }
          })
          this.fetchProject()
          this.addAttachmentForm = { description: '', file: null }
        })
        .catch((err) => {
          this.toast.error({
            component: ToastyToast,
            props: {
              title: this.$pgettext('ProjectAttachment/Create/Toast/Error/Title', 'Saving project attachment'),
              message: this.$pgettext('ProjectAttachment/Create/Toast/Error/Message', 'Error occured or file type not allowed.')
            }
          })
          logger.default.error('Error with project attachment deletion', err)
        })
    },
    deleteAttachment (attachment) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the attachment '${attachment.description}' ?`, {
        title: 'Please Confirm',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'YES',
        cancelTitle: 'NO',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true
      })
        .then((value) => {
          if (value === false) { return }

          apiService.projectAttachmentDelete(this.project.id, attachment.id)
            .then((val) => {
              this.toast.success({
                component: ToastyToast,
                props: {
                  title: this.$pgettext('ProjectAttachment/Delete/Toast/Success/Title', 'Deleting project attachment'),
                  message: this.$pgettext('ProjectAttachment/Delete/Toast/Success/Message', 'Success')
                }
              })
              this.fetchProject()
            })
            .catch((err) => {
              this.toast.error({
                component: ToastyToast,
                props: {
                  title: this.$pgettext('ProjectAttachment/Delete/Toast/Error/Title', 'Deleting project attachment'),
                  message: this.$pgettext('ProjectAttachment/Delete/Toast/Error/Message', 'An error occured, please try again later')
                }
              })
              logger.default.error('Error with project attachment deletion', err)
              this.fetchProject()
            })
        })
        .catch((err) => {
          logger.default.error('Error with the delete attachment modal', err)
        })
    },
    manageInventoryPart () {
      this.$bvModal.show('modalManageInventoryPart')
    },
    manageExternalPart () {
      this.$bvModal.show('modalManageExternalPart')
    },
    onPartSaved () {
      logger.default.info('Part saved, reloading project.')
      this.partToEdit = null
      this.fetchProject()
    },
    onPartModalClosed () {
      this.partDetails = null
    },
    viewPartModal (part) {
      this.partDetails = part
      this.$bvModal.show('modalManage')
    },
    editPart (part) {
      this.partToEdit = part
      if (part.part) {
        this.$bvModal.show('modalManageInventoryPart')
      } else {
        this.$bvModal.show('modalManageExternalPart')
      }
    },
    deletePart (part) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the part '${part.part ? part.part.name : part.part_name}' from the project ?`, {
        title: 'Please Confirm',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: 'YES',
        cancelTitle: 'NO',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true
      })
        .then((value) => {
          if (value === false) { return }

          if (value === true) {
            apiService.projectDeletePart(this.project.id, part.id)
              .then((val) => {
                this.toast.success({
                  component: ToastyToast,
                  props: {
                    title: this.$pgettext('ProjectPart/Delete/Toast/Success/Title', 'Deleting project part'),
                    message: this.$pgettext('ProjectPart/Delete/Toast/Success/Message', 'Success')
                  }
                })
                this.fetchProject()
              })
              .catch((err) => {
                this.toast.error({
                  component: ToastyToast,
                  props: {
                    title: this.$pgettext('ProjectPart/Delete/Toast/Error/Title', 'Deleting project part'),
                    message: this.$pgettext('ProjectPart/Delete/Toast/Error/Message', 'An error occured, please try again later')
                  }
                })
                logger.default.error('Error with project part deletion', err)
                this.fetchProject()
              })
          }
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    },
    clearPartToEdit () {
      this.partToEdit = null
    },
    exportProject (kind) {
      if (kind === 'infos_txt') {
        apiService.projectExportInfosTxt(this.project.id, `${this.project.name}.txt`)
      } else if (kind === 'bom_csv') {
        apiService.projectExportBomCSV(this.project.id, `${this.project.name}__bom.csv`)
      } else if (kind === 'bom_xlsx') {
        apiService.projectExportBomXLSX(this.project.id, `${this.project.name}__bom.xlsx`)
      }
    }
  }
}
</script>

<style>
table#tableParts td.notes {
  width: 30em;
  overflow: hidden;
}

table#tableParts td.stock_qty {
  width: 6em;
}

table#tableParts td.qty {
  width: 8em;
}

table#tableParts td.qty_total {
  width: 8em;
}

table#tableParts td.sourced {
  width: 6em;
}

table#tableParts td.actions {
  width: 8em;
}
</style>
