<template>
  <div class="project_details">
    <AddPartInventoryModal />
    <AddPartExternalModal @add-part-external-saved="onPartExternalSaved" />

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
          </div>
        </div>

        <div class="row my-4">
          <div class="col-md-12">
            Description:
            <div class="description">
              {{ project.description || 'None' }}
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-md-12">
            Notes:
            <div class="description">
              {{ project.notes || 'None' }}
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <b-tabs content-class="mt-3">
          <b-tab title="Parts">
            <b-button variant="primary" @click.prevent="addInventoryPart">
              Add part from inventory
            </b-button>&nbsp;
            <b-button variant="info" @click.prevent="addExternalPart">
              Add external part
            </b-button>
            <hr>
          </b-tab>

          <b-tab title="Files attachments">
            <b-form enctype="multipart/form-data" inline @submit.prevent="addAttachment">
              <label class="sr-only" for="description">Description</label>
              <b-form-input
                id="description"
                v-model="addAttachmentForm.description"
                required
                placeholder="File description"
                class="mb-2 mr-sm-2 mb-sm-0"
              />

              <label class="sr-only" for="file">File</label>
              <b-form-group id="input-group-file" label-for="file" class="mb-2 mr-sm-2 mb-sm-0">
                <b-form-file
                  id="file"
                  ref="file"
                  v-model="addAttachmentForm.file"
                  :accept="allowedUploadTypes"
                  required
                />
              </b-form-group>

              <b-button type="submit" variant="primary">
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
import AddPartInventoryModal from '@/components/parts/project_add_inventory_modal'
import AddPartExternalModal from '@/components/parts/project_add_external_modal'
import apiService from '../../services/api/api.service'
import logger from '@/logging'
import { mapState } from 'vuex'

export default {
  components: {
    AddPartInventoryModal,
    AddPartExternalModal
  },
  props: {
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
      { value: 4, text: 'Waiting' },
      { value: 5, text: 'Abandonned' },
      { value: 99, text: 'Unknown' },
      { value: null, text: 'Filter by state' }
    ]
  }),
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
          this.$bvToast.toast(this.$pgettext('Project/Details/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Project/Details/Toast/Error/Title', 'Fetching project details'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error with project fetch', err.message)
        })
    },
    deleteProject (project) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the project '${project.name}' ?`, {
        title: 'Plase Confirm',
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
              this.$bvToast.toast(this.$pgettext('Project/Delete/Toast/Success/Message', 'Success'), {
                title: this.$pgettext('Project/Delete/Toast/Success/Title', 'Deleting project'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'primary',
                toaster: 'b-toaster-top-center'
              })
              this.$router.push({ name: 'projects-list' })
            })
            .catch((err) => {
              this.$bvToast.toast(this.$pgettext('Project/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                title: this.$pgettext('Project/Delete/Toast/Error/Title', 'Deleting project'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'danger',
                toaster: 'b-toaster-top-center'
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
      apiService.projectAttachmentCreate(this.project.id, this.addAttachmentForm)
        .then((val) => {
          this.$bvToast.toast(this.$pgettext('ProjectAttachment/Create/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('ProjectAttachment/Create/Toast/Success/Title', 'Saving project attachment'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.fetchProject()
          this.addAttachmentForm = { description: '', file: null }
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('ProjectAttachment/Create/Toast/Error/Message', 'Error occured or file type not allowed.'), {
            title: this.$pgettext('ProjectAttachment/Create/Toast/Error/Title', 'Saving project attachment'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error with project attachment deletion', err)
        })
    },
    deleteAttachment (attachment) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the attachment '${attachment.description}' ?`, {
        title: 'Plase Confirm',
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
              this.$bvToast.toast(this.$pgettext('ProjectAttachment/Delete/Toast/Success/Message', 'Success'), {
                title: this.$pgettext('ProjectAttachment/Delete/Toast/Success/Title', 'Deleting project attachment'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'primary',
                toaster: 'b-toaster-top-center'
              })
              this.fetchProject()
            })
            .catch((err) => {
              this.$bvToast.toast(this.$pgettext('ProjectAttachment/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                title: this.$pgettext('ProjectAttachment/Delete/Toast/Error/Title', 'Deleting project attachment'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'danger',
                toaster: 'b-toaster-top-center'
              })
              logger.default.error('Error with project attachment deletion', err)
              this.fetchProject()
            })
        })
        .catch((err) => {
          logger.default.error('Error with the delete attachment modal', err)
        })
    },
    addInventoryPart () {
      this.$bvModal.show('modalAddInventoryPart')
    },
    addExternalPart () {
      this.$bvModal.show('modalAddExternalPart')
    },
    onPartExternalSaved () {
      logger.default.info('Part saved, reloading project.')
      this.fetchProject()
    }
  }
}
</script>
