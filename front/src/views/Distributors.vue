<template>
  <div class="list_distributors">
    <b-modal id="modalAddDistributor" ref="modalAddDistributor"
             size="md" :hide-footer="true"
             @cancel="modalAddDistributorClose"
             @close="modalAddDistributorClose"
             @hidden="modalAddDistributorClose"
    >
      <template #modal-header="{ close }">
        <h5 id="modalPartTitle">
          <span class="modal-title">{{ modalTitle }}</span>
        </h5>
        <button type="button" class="close" data-dismiss="modal"
                aria-label="Close" @click="close()"
        >
          <span aria-hidden="true">&times;</span>
        </button>
      </template>
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <b-form @submit.prevent="saveDistributor">
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  v-model="modalDistributor.name"
                  required
                  :state="$v.modalDistributor.name.$dirty ? !$v.modalDistributor.name.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-address" label="Address" label-for="short-address">
                <b-form-textarea
                  id="address"
                  v-model="modalDistributor.address"
                  :state="$v.modalDistributor.address.$dirty ? !$v.modalDistributor.address.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-url" label="Website" label-for="short-url">
                <b-form-input
                  id="url"
                  v-model="modalDistributor.url"
                  type="url"
                  :state="$v.modalDistributor.url.$dirty ? !$v.modalDistributor.url.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-email" label="Email" label-for="email">
                <b-form-input
                  id="email"
                  v-model="modalDistributor.email"
                  type="email"
                  :state="$v.modalDistributor.email.$dirty ? !$v.modalDistributor.email.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-comment" label="Comment" label-for="comment">
                <b-form-textarea
                  id="comment"
                  v-model="modalDistributor.comment"
                  :state="$v.modalDistributor.comment.$dirty ? !$v.modalDistributor.comment.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-phone" label="Phone" label-for="phone">
                <b-form-input
                  id="phone"
                  v-model="modalDistributor.phone"
                  type="tel"
                  :state="$v.modalDistributor.phone.$dirty ? !$v.modalDistributor.phone.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-fax" label="Fax" label-for="fax">
                <b-form-input
                  id="fax"
                  v-model="modalDistributor.fax"
                  type="tel"
                  :state="$v.modalDistributor.fax.$dirty ? !$v.modalDistributor.fax.$error : null"
                />
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
          <b-breadcrumb-item>Distributors</b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
      <b-col xl="2" cols="4">
        <b-button
          variant="info"
          @click.prevent="showAddDistributorModal"
        >
          Add a distributor
        </b-button>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="10">
        <b-table
          id="tableDistributors"
          :items="distributors"
          :fields="fields"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          :per-page="perPage"
          :current-page="currentPage"
          responsive="sm"
          striped
          small
        >
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
              @click.prevent="showEditDistributorsModal(data.item)"
            >
              <i
                class="fa fa-pencil-square-o"
                aria-hidden="true"
              />
            </b-button>
        &nbsp;
            <b-button
              variant="link"
              @click.prevent="deleteDistributor(data.item)"
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
          aria-controls="tableDistributors"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'
import { validationMixin } from 'vuelidate'
import { required, email, url } from 'vuelidate/lib/validators'
import { mapState } from 'vuex'

export default {
  mixins: [
    validationMixin
  ],
  props: {
  },
  data: () => ({
    distributors: [],
    currentPage: 1,
    fields: [
      { key: 'name', label: 'Name', sortable: true },
      { key: 'address', label: 'Address' },
      { key: 'url', label: 'URL' }, // includes email
      { key: 'comment', label: 'Comment' },
      { key: 'phones', label: 'Phones' }, // includes phone and fax
      { key: 'actions', label: 'Actions' }
    ],
    sortBy: 'name',
    sortDesc: false,
    modalTitle: '',
    modalDistributor: {
      name: '',
      address: '',
      url: '',
      email: '',
      comment: '',
      phone: '',
      fax: ''
    },
    modalAction: 'create'
  }),
  validations: {
    modalDistributor: {
      name: { required },
      address: {},
      url: { url },
      email: { email },
      comment: {},
      phone: {},
      fax: {}
    }
  },
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings
    }),
    rows () {
      return this.distributors.length
    },
    perPage () {
      return this.serverSettings.pagination.DISTRIBUTORS || 10
    }
  },
  watch: {
  },
  created () {
    this.fetchDistributors()
  },
  methods: {
    fetchDistributors () {
      apiService.getDistributors()
        .then((val) => {
          this.distributors = val.data
          this.$store.dispatch('preloadDistributors')
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('distributors/Fetch/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('distributors/Fetch/Toast/Error/Title', 'Fetching distributors'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Error getting distributors', err)
        })
    },
    showAddDistributorModal (distributors) {
      this.modalDistributor = { ...distributors }
      this.modalTitle = 'Add distributor'
      this.modalAction = 'create'
      this.$bvModal.show('modalAddDistributor')
    },
    showEditDistributorsModal (distributors) {
      this.modalDistributor = { ...distributors }
      this.modalTitle = 'Edit distributor'
      this.modalAction = 'edit'
      this.$bvModal.show('modalAddDistributor')
    },
    modalAddDistributorClose () {
      this.modalTitle = ''
      this.clearForm()
    },
    saveDistributor () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        return
      }

      if (this.modalAction === 'create') {
        apiService.createDistributor(this.modalDistributor)
          .then(() => {
            this.$bvToast.toast(this.$pgettext('Distributor/Add/Toast/Success/Message', 'Success'), {
              title: this.$pgettext('Distributor/Add/Toast/Success/Title', 'Adding distributor'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'primary'
            })
            this.$bvModal.hide('modalAddDistributor')
            this.clearForm()
            this.fetchDistributors()
          })
          .catch((error) => {
            this.$bvToast.toast(this.$pgettext('Distributor/Add/Toast/Error/Message', 'An error occured, please try again later'), {
              title: this.$pgettext('Distributor/Add/Toast/Error/Title', 'Adding distributor'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger'
            })
            logger.default.error('Cannot save distributor', error.message)
          })
      } else {
        apiService.updateDistributor(this.modalDistributor.id, this.modalDistributor)
          .then(() => {
            this.$bvToast.toast(this.$pgettext('Distributor/Update/Toast/Success/Message', 'Success'), {
              title: this.$pgettext('Distributor/Update/Toast/Success/Title', 'Updating distributor'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'primary'
            })
            this.$bvModal.hide('modalAddDistributor')
            this.clearForm()
            this.fetchDistributors()
          })
          .catch((error) => {
            this.$bvToast.toast(this.$pgettext('Distributor/Update/Toast/Error/Message', 'An error occured, please try again later'), {
              title: this.$pgettext('Distributor/Update/Toast/Error/Title', 'Updating distributor'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger'
            })
            logger.default.error('Cannot update distributor', error.message)
          })
      }
    },
    clearForm () {
      this.modalDistributor.name = ''
      this.modalDistributor.short_name = ''
      this.modalDistributor.description = ''
      this.$v.$reset()
    },
    deleteDistributor (distributor) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the distributor '${distributor.name}' ? All associated parts SKU will be lost.`, {
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

          if (value === true) {
            apiService.deleteDistributor(distributor.id)
              .then((val) => {
                this.$bvToast.toast(this.$pgettext('Distributor/Delete/Toast/Success/Message', 'Success'), {
                  title: this.$pgettext('Distributor/Delete/Toast/Success/Title', 'Deleting distributor'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'primary'
                })
                this.fetchDistributors()
              })
              .catch((err) => {
                this.$bvToast.toast(this.$pgettext('Distributor/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('Distributor/Delete/Toast/Error/Title', 'Deleting distributor'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger'
                })
                logger.default.error('Error with distributor deletion', err)
                this.fetchDistributors()
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
