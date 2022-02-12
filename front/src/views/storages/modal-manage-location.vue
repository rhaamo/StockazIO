<template>
  <b-modal
    id="modalStoragesManageLocation" ref="modalStoragesManageLocation"
    size="md" hide-footer @cancel="manageLocationClose"
    @close="manageLocationClose" @hidden="manageLocationClose"
    @show="manageLocationShow"
  >
    <template #modal-header="{ close }">
      <h5 id="modalPartTitle">
        Manage storage Location
      </h5>
      <button
        type="button" class="close" data-dismiss="modal"
        aria-label="Close" @click="close()"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </template>

    <div class="container">
      <div class="row">
        <div class="col-md-11 mx-auto">
          <b-form @submit.prevent="saveOrUpdate">
            <b-form-group id="input-group-name" label="Name" label-for="name">
              <b-form-input
                id="name"
                ref="inputname"
                v-model="form.name"
                required
                placeholder="That one box"
                :state="$v.form.name.$dirty ? !$v.form.name.$error : null"
              />
              <div v-if="!$v.form.name.required" class="invalid-feedback d-block">
                Location name is required
              </div>
              <div v-if="!$v.form.name.maxLength" class="invalid-feedback d-block">
                Maximum length is 255
              </div>
            </b-form-group>

            <b-form-group id="input-group-description" label="Description" label-for="description">
              <b-form-input
                id="description"
                ref="inputdescription"
                v-model="form.description"
                placeholder="Full of emptyness"
                :state="$v.form.description.$dirty ? !$v.form.description.$error : null"
              />
              <div v-if="!$v.form.description.maxLength" class="invalid-feedback d-block">
                Maximum length is 255
              </div>
            </b-form-group>

            <b-form-group id="input-group-storage_location" label="Storage place:" label-for="storage_location">
              <vue-treeselect
                v-model="form.parent_id"
                :required="true" :multiple="false" :options="choicesStorageLocation"
                search-nested :default-expand-level="Infinity" clearable
                no-children-text placeholder="In the House ? The Workshop ?"
                :disable-branch-nodes="true" :normalizer="storagesNormalizer"
              />
            </b-form-group>

            <b-form-group id="input-group-picture" label="Picture" label-for="picture">
              <b-form-file
                id="picture"
                ref="file"
                v-model="form.picture"
                :accept="allowedUploadTypes"
                :state="$v.form.picture.$dirty ? !$v.form.picture.$error : null"
              />
              <template v-if="mode==='edit' && typeof item.picture === 'string'">
                Current <a :href="item.picture" target="_blank">file</a>.
              </template>
            </b-form-group>

            <b-button class="mt-3" type="submit" variant="primary">
              Save
            </b-button>
          </b-form>
        </div>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength } from 'vuelidate/lib/validators'
import logger from '@/logging'
import { mapState } from 'vuex'
import apiService from '@/services/api/api.service'

export default {
  mixins: [
    validationMixin
  ],
  props: {
    parent: {
      type: Number
    },
    mode: {
      type: String
    },
    item: {
      type: Object
    }
  },
  data: () => ({
    modalManageLocationParent: null,
    form: {
      name: '',
      description: '',
      parent_id: '',
      picture: null
    }
  }),
  validations: {
    form: {
      name: { required, maxLength: maxLength(255) },
      description: { maxLength: maxLength(255) },
      parent_id: { required },
      picture: {}
    }
  },
  computed: {
    ...mapState({
      choicesStorageLocation: (state) => state.preloads.storages,
      serverSettings: state => state.server.settings
    }),
    allowedUploadTypes () {
      let types = this.serverSettings.partAttachmentAllowedTypes || ['image/jpeg', 'image/png']
      return types.join(', ')
    }
  },
  methods: {
    storagesNormalizer: function (node) {
      let childs = (node.children || []).concat(node.storage_locations || [])
      let id = node.uuid ? node.id : `cat_${node.id}`
      return { id: id, label: node.name, children: childs && childs.length ? childs : 0 }
    },
    manageLocationShow () {
      // the ID is prefixed with 'cat_' for categories when normalized in the treeselect
      // to avoid clashes between category IDs and location IDs that could be identical
      this.form.parent_id = `cat_${this.parent}`
      if (this.item) {
        this.form.name = this.item.name
        this.form.description = this.item.description
        this.form.parent_id = `cat_${this.item.category}`
        this.form.picture = this.item.picture
      }
    },
    manageLocationClose () {
      this.clearForm()
      this.$bvModal.hide('modalStoragesManageLocation')
      this.$emit('modal-storages-manage-location-closed')
    },
    saveOrUpdate () {
      if (this.mode === 'add') {
        this.save()
      } else {
        this.update()
      }
    },
    save () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('form has errors')
        return
      }

      let storageLocation = {
        name: this.form.name,
        description: this.form.description,
        category: this.form.parent_id.split('_')[1],
        picture: this.form.picture
      }

      apiService.createStorageLocation(storageLocation)
        .then(() => {
          this.$bvToast.toast(this.$pgettext('StorageLocation/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('StorageLocation/Add/Toast/Success/Title', 'Add storage Location'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.manageLocationClose()
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('StorageLocation/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('StorageLocation/Add/Toast/Error/Title', 'Add storage Location'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot add storage Location', error.message)
        })
    },
    update () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('form has errors')
        return
      }

      let storageLocation = {
        name: this.form.name,
        description: this.form.description,
        category: this.form.parent_id.split('_')[1],
        picture: this.form.picture
      }

      apiService.updateStorageLocation(this.item.id, storageLocation)
        .then(() => {
          this.$bvToast.toast(this.$pgettext('StorageLocation/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('StorageLocation/Update/Toast/Success/Title', 'Update storage Location'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.manageLocationClose()
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('StorageLocation/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('StorageLocation/Update/Toast/Error/Title', 'Update storage Location'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot update storage Location', error.message)
        })
    },
    clearForm () {
      this.form.name = ''
      this.form.description = ''
      this.form.parent_id = ''
      this.form.picture = null
      this.$v.$reset()
    }
  }
}
</script>

<style>
</style>
