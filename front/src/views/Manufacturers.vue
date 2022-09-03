<template>
  <div class="list_manufacturers">
    <b-modal
      id="modalAddManufacturer" ref="modalAddManufacturer"
      size="md" :hide-footer="true"
      @cancel="modalAddManufacturerClose"
      @close="modalAddManufacturerClose"
      @hidden="modalAddManufacturerClose"
    >
      <template #modal-header="{ close }">
        <h5 id="modalPartTitle">
          <span class="modal-title">{{ modalTitle }}</span>
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
          <div class="col-md-12">
            <b-form enctype="multipart/form-data" @submit.prevent="saveManufacturer">
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  v-model="modalManufacturer.name"
                  required
                  :state="$v.modalManufacturer.name.$dirty ? !$v.modalManufacturer.name.$error : null"
                  autofocus
                />
                <div v-if="!$v.modalManufacturer.name.required" class="invalid-feedback d-block">
                  Name is required
                </div>
                <div v-if="!$v.modalManufacturer.name.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <b-form-group id="input-group-address" label="Address" label-for="short-address">
                <b-form-textarea
                  id="address"
                  v-model="modalManufacturer.address"
                  :state="$v.modalManufacturer.address.$dirty ? !$v.modalManufacturer.address.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-url" label="Website" label-for="short-url">
                <b-form-input
                  id="url"
                  v-model="modalManufacturer.url"
                  type="url"
                  :state="$v.modalManufacturer.url.$dirty ? !$v.modalManufacturer.url.$error : null"
                />
                <div v-if="!$v.modalManufacturer.url.url" class="invalid-feedback d-block">
                  Invalid url
                </div>
                <div v-if="!$v.modalManufacturer.url.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <b-form-group id="input-group-email" label="Email" label-for="email">
                <b-form-input
                  id="email"
                  v-model="modalManufacturer.email"
                  type="email"
                  :state="$v.modalManufacturer.email.$dirty ? !$v.modalManufacturer.email.$error : null"
                />
                <div v-if="!$v.modalManufacturer.email.email" class="invalid-feedback d-block">
                  Invalid email
                </div>
                <div v-if="!$v.modalManufacturer.email.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <b-form-group id="input-group-comment" label="Comment" label-for="comment">
                <b-form-textarea
                  id="comment"
                  v-model="modalManufacturer.comment"
                  :state="$v.modalManufacturer.comment.$dirty ? !$v.modalManufacturer.comment.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-phone" label="Phone" label-for="phone">
                <b-form-input
                  id="phone"
                  v-model="modalManufacturer.phone"
                  type="tel"
                  :state="$v.modalManufacturer.phone.$dirty ? !$v.modalManufacturer.phone.$error : null"
                />
                <div v-if="!$v.modalManufacturer.phone.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>
              <b-form-group id="input-group-fax" label="Fax" label-for="fax">
                <b-form-input
                  id="fax"
                  v-model="modalManufacturer.fax"
                  type="tel"
                  :state="$v.modalManufacturer.fax.$dirty ? !$v.modalManufacturer.fax.$error : null"
                />
                <div v-if="!$v.modalManufacturer.fax.maxLength" class="invalid-feedback d-block">
                  Maximum length is 255
                </div>
              </b-form-group>

              <b-form-group id="input-group-logo" label="Logo" label-for="logo">
                <b-form-file
                  id="logo"
                  ref="file"
                  v-model="modalManufacturer.logo"
                  :accept="allowedUploadTypes"
                  :state="$v.modalManufacturer.logo.$dirty ? !$v.modalManufacturer.logo.$error : null"
                />
                <template v-if="modalAction==='edit' && typeof modalManufacturer.logo === 'string'">
                  Current <a :href="modalManufacturer.logo" target="_blank">file</a>.
                </template>
              </b-form-group>

              <b-button type="submit" variant="primary">
                Save
              </b-button>
            </b-form>
          </div>
        </div>
      </div>
    </b-modal>

    <b-row>
      <b-col xl="9" cols="7">
        <b-breadcrumb>
          <b-breadcrumb-item>Manufacturers</b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
      <b-col xl="2" cols="4">
        <b-button
          variant="info"
          @click.prevent="showAddManufacturerModal"
        >
          Add a manufacturer
        </b-button>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="10">
        <b-table
          id="tableManufacturers"
          :items="manufacturers"
          :fields="fields"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          :per-page="perPage"
          :current-page="currentPage"
          responsive="sm"
          striped
          small
        >
          <template #cell(logo)="data">
            <template v-if="data.item.logo">
              <img :src="data.item.logo_mini" style="max-width: 100px;">
            </template>
          </template>

          <template #cell(url)="data">
            <template v-if="data.item.url">
              <a :href="data.item.url" target="_blank">{{ data.item.url }}</a>
            </template>
            <template v-if="data.item.url && data.item.email">
              <br>
            </template>
            <template v-if="data.item.email">
              {{ data.item.email }}
            </template>
          </template>

          <template #cell(phones)="data">
            <template v-if="data.item.phone">
              Tel: {{ data.item.phone }}
            </template>
            <template v-if="data.item.phone && data.item.fax">
              <br>
            </template>
            <template v-if="data.item.fax">
              Fax: {{ data.item.fax }}
            </template>
          </template>

          <template #cell(actions)="data">
            <b-button
              variant="link"
              @click.prevent="showEditManufacturerModal(data.item)"
            >
              <i
                class="fa fa-pencil-square-o"
                aria-hidden="true"
              />
            </b-button>
        &nbsp;
            <b-button
              variant="link"
              @click.prevent="deleteManufacturer(data.item)"
            >
              <i
                class="fa fa-trash-o"
                aria-hidden="true"
              />
            </b-button>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col md="6" offset-md="1">
        <b-pagination
          v-model="currentPage"
          :total-rows="rows"
          :per-page="perPage"
          aria-controls="tableManufacturers"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'
import { validationMixin } from 'vuelidate'
import { required, email, url, maxLength } from 'vuelidate/lib/validators'
import { mapState } from 'vuex'
import { useToast } from 'vue-toastification'
import ToastyToast from '@/components/toasty-toast'

export default {
  name: 'ViewManufacturers',
  mixins: [
    validationMixin
  ],
  props: {
  },
  data: () => ({
    currentPage: 1,
    fields: [
      { key: 'name', label: 'Name', sortable: true },
      { key: 'logo', label: 'Logo' },
      { key: 'address', label: 'Address' },
      { key: 'url', label: 'URL' }, // includes email
      { key: 'comment', label: 'Comment' },
      { key: 'phones', label: 'Phones' }, // includes phone and fax
      { key: 'actions', label: 'Actions' }
    ],
    sortBy: 'name',
    sortDesc: false,
    modalTitle: '',
    modalManufacturer: {
      name: '',
      address: '',
      url: '',
      email: '',
      comment: '',
      phone: '',
      fax: '',
      logo: null
    },
    modalAction: 'create'
  }),
  setup () {
    const toast = useToast()
    return { toast }
  },
  validations: {
    modalManufacturer: {
      name: { required, maxLength: maxLength(255) },
      address: {},
      url: { url, maxLength: maxLength(255) },
      email: { email, maxLength: maxLength(255) },
      comment: {},
      phone: { maxLength: maxLength(255) },
      fax: { maxLength: maxLength(255) },
      logo: {}
    }
  },
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings,
      manufacturers: state => state.preloads.manufacturers
    }),
    rows () {
      return this.manufacturers.length
    },
    perPage () {
      return this.serverSettings.pagination.MANUFACTURERS || 10
    },
    allowedUploadTypes () {
      let types = this.serverSettings.partAttachmentAllowedTypes || ['application/pdf', 'image/jpeg']
      return types.join(', ')
    }
  },
  watch: {
  },
  created () {
  },
  methods: {
    fetchManufacturers () {
      apiService.getManufacturers()
        .then((val) => {
          this.$store.commit('setManufacturers', val.data)
          this.$store.commit('setLastUpdate', { item: 'manufacturers', value: new Date() })
        })
        .catch((err) => {
          this.toast.error({
            component: ToastyToast,
            props: {
              title: this.$pgettext('Manufacturers/Fetch/Toast/Error/Title', 'Fetching manufacturers'),
              message: this.$pgettext('Manufacturers/Fetch/Toast/Error/Message', 'An error occured, please try again later')
            }
          })
          logger.default.error('Error getting manufacturers', err)
        })
    },
    showAddManufacturerModal (manufacturers) {
      this.modalManufacturer = { ...manufacturers }
      this.modalTitle = 'Add manufacturer'
      this.modalAction = 'create'
      this.$bvModal.show('modalAddManufacturer')
    },
    showEditManufacturerModal (manufacturers) {
      this.modalManufacturer = { ...manufacturers }
      this.modalTitle = 'Edit manufacturer'
      this.modalAction = 'edit'
      this.$bvModal.show('modalAddManufacturer')
    },
    modalAddManufacturerClose () {
      this.modalTitle = ''
      this.clearForm()
    },
    saveManufacturer () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        return
      }

      if (this.modalAction === 'create') {
        apiService.createManufacturer(this.modalManufacturer)
          .then(() => {
            this.toast.success({
              component: ToastyToast,
              props: {
                title: this.$pgettext('Manufacturer/Add/Toast/Success/Title', 'Adding manufacturer'),
                message: this.$pgettext('Manufacturer/Add/Toast/Success/Message', 'Success')
              }
            })
            this.$bvModal.hide('modalAddManufacturer')
            this.clearForm()
            this.fetchManufacturers()
          })
          .catch((error) => {
            this.toast.error({
              component: ToastyToast,
              props: {
                title: this.$pgettext('Manufacturer/Add/Toast/Error/Title', 'Adding manufacturer'),
                message: this.$pgettext('Manufacturer/Add/Toast/Error/Message', 'An error occured, please try again later')
              }
            })
            logger.default.error('Cannot save distributor', error.message)
          })
      } else {
        apiService.updateManufacturer(this.modalManufacturer.id, this.modalManufacturer)
          .then(() => {
            this.toast.success({
              component: ToastyToast,
              props: {
                title: this.$pgettext('Manufacturer/Update/Toast/Success/Title', 'Updating manufacturer'),
                message: this.$pgettext('Manufacturer/Update/Toast/Success/Message', 'Success')
              }
            })
            this.$bvModal.hide('modalAddManufacturer')
            this.clearForm()
            this.fetchManufacturers()
          })
          .catch((error) => {
            this.toast.error({
              component: ToastyToast,
              props: {
                title: this.$pgettext('Distributor/Update/Toast/Error/Title', 'Updating manufacturer'),
                message: this.$pgettext('Distributor/Update/Toast/Error/Message', 'An error occured, please try again later')
              }
            })
            logger.default.error('Cannot update manufacturer', error.message)
          })
      }
    },
    clearForm () {
      this.modalManufacturer.name = ''
      this.modalManufacturer.short_name = ''
      this.modalManufacturer.description = ''
      this.$v.$reset()
    },
    deleteManufacturer (manufacturer) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the manufacturer '${manufacturer.name}' ? All associated parts SKU will be lost.`, {
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
            apiService.deleteManufacturer(manufacturer.id)
              .then((val) => {
                this.toast.success({
                  component: ToastyToast,
                  props: {
                    title: this.$pgettext('Manufacturer/Delete/Toast/Success/Title', 'Deleting manufacturer'),
                    message: this.$pgettext('Manufacturer/Delete/Toast/Success/Message', 'Success')
                  }
                })
                this.fetchManufacturers()
              })
              .catch((err) => {
                this.toast.error({
                  component: ToastyToast,
                  props: {
                    title: this.$pgettext('Manufacturer/Delete/Toast/Error/Title', 'Deleting manufacturer'),
                    message: this.$pgettext('Manufacturer/Delete/Toast/Error/Message', 'An error occured, please try again later')
                  }
                })
                logger.default.error('Error with manufacturer deletion', err)
                this.fetchManufacturers()
              })
          }
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    }
  }
}
</script>
