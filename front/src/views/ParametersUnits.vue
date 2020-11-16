<template>
  <div class="list_part_unit">
    <b-modal id="modalAddParametersUnit" ref="modalAddParametersUnit"
             size="md" :hide-footer="true"
             @cancel="modalAddParametersUnitClose"
             @close="modalAddParametersUnitClose"
             @hidden="modalAddParametersUnitClose"
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
            <b-form @submit.prevent="saveParametersUnit">
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  v-model="modalParameterUnit.name"
                  required
                  placeholder="Ampere"
                  :state="$v.modalParameterUnit.name.$dirty ? !$v.modalParameterUnit.name.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-prefix" label="Prefix" label-for="short-prefix">
                <b-form-input
                  id="prefix"
                  v-model="modalParameterUnit.prefix"
                  placeholder="µ"
                  :state="$v.modalParameterUnit.prefix.$dirty ? !$v.modalParameterUnit.prefix.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-symbol" label="Symbol" label-for="short-symbol">
                <b-form-input
                  id="symbol"
                  v-model="modalParameterUnit.symbol"
                  placeholder="A"
                  :state="$v.modalParameterUnit.symbol.$dirty ? !$v.modalParameterUnit.symbol.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-description" label="Description" label-for="description">
                <b-form-input
                  id="description"
                  v-model="modalParameterUnit.description"
                  placeholder=""
                  :state="$v.modalParameterUnit.description.$dirty ? !$v.modalParameterUnit.description.$error : null"
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
          <b-breadcrumb-item>Parameters Units</b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
      <b-col xl="2" cols="4">
        <b-button
          variant="info"
          @click.prevent="showAddParametersUnitModal"
        >
          Add a parameters unit
        </b-button>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="10">
        <b-table
          id="tableParametersUnits"
          :items="parametersUnits"
          :fields="fields"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          :per-page="perPage"
          :current-page="currentPage"
          responsive="sm"
          striped
          small
        >
          <template #cell(actions)="data">
            <b-button
              variant="link"
              @click.prevent="showEditParametersUnitModal(data.item)"
            >
              <i
                class="fa fa-pencil-square-o"
                aria-hidden="true"
              />
            </b-button>
        &nbsp;
            <b-button
              variant="link"
              @click.prevent="deleteParametersUnit(data.item)"
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
          aria-controls="tableParametersUnits"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import { mapState } from 'vuex'

export default {
  mixins: [
    validationMixin
  ],
  props: {
  },
  data: () => ({
    parametersUnits: [],
    currentPage: 1,
    search_query: '', // TODO/FIXME no search yet
    fields: [
      { key: 'name', label: 'Name', sortable: true },
      { key: 'prefix', label: 'Prefix' },
      { key: 'symbol', label: 'Symbol' },
      { key: 'description', label: 'Description' },
      { key: 'actions', label: 'Actions' }
    ],
    sortBy: 'name',
    sortDesc: false,
    modalTitle: '',
    modalParameterUnit: {
      name: '',
      prefix: '',
      symbol: '',
      description: ''
    },
    modalAction: 'create'
  }),
  validations: {
    modalParameterUnit: {
      name: { required },
      prefix: {},
      symbol: {},
      description: {}
    }
  },
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings
    }),
    rows () {
      return this.parametersUnits.length
    },
    perPage () {
      return this.serverSettings.pagination.PARAMETERS_UNITS || 10
    }
  },
  watch: {
  },
  created () {
    this.fetchParametersUnits()
  },
  methods: {
    fetchParametersUnits () {
      apiService.getParametersUnits()
        .then((val) => {
          this.parametersUnits = val.data
          console.log(val.data)
          this.$store.dispatch('preloadParametersUnits')
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('ParametersUnits/Fetch/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('ParametersUnits/Fetch/Toast/Error/Title', 'Fetching part units'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Error getting part units', err)
        })
    },
    showAddParametersUnitModal (parametersUnits) {
      this.modalParameterUnit = { ...parametersUnits }
      this.modalTitle = 'Add Part Unit'
      this.modalAction = 'create'
      this.$bvModal.show('modalAddParametersUnit')
    },
    showEditParametersUnitModal (parametersUnits) {
      this.modalParameterUnit = { ...parametersUnits }
      this.modalTitle = 'Edit Part Unit'
      this.modalAction = 'edit'
      this.$bvModal.show('modalAddParametersUnit')
    },
    modalAddParametersUnitClose () {
      this.modalTitle = ''
      this.clearForm()
    },
    saveParametersUnit () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        return
      }

      if (this.modalAction === 'create') {
        apiService.createParametersUnits(this.modalParameterUnit)
          .then(() => {
            this.$bvToast.toast(this.$pgettext('ParametersUnit/Add/Toast/Success/Message', 'Success'), {
              title: this.$pgettext('ParametersUnit/Add/Toast/Success/Title', 'Adding part unit'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'primary'
            })
            this.$bvModal.hide('modalAddParametersUnit')
            this.clearForm()
            this.fetchParametersUnits()
          })
          .catch((error) => {
            this.$bvToast.toast(this.$pgettext('ParametersUnit/Add/Toast/Error/Message', 'An error occured, please try again later'), {
              title: this.$pgettext('ParametersUnit/Add/Toast/Error/Title', 'Adding part unit'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger'
            })
            logger.default.error('Cannot save part unit', error.message)
          })
      } else {
        apiService.updateParametersUnits(this.modalParameterUnit.id, this.modalParameterUnit)
          .then(() => {
            this.$bvToast.toast(this.$pgettext('ParametersUnit/Update/Toast/Success/Message', 'Success'), {
              title: this.$pgettext('ParametersUnit/Update/Toast/Success/Title', 'Updating part unit'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'primary'
            })
            this.$bvModal.hide('modalAddParametersUnit')
            this.clearForm()
            this.fetchParametersUnits()
          })
          .catch((error) => {
            this.$bvToast.toast(this.$pgettext('ParametersUnit/Update/Toast/Error/Message', 'An error occured, please try again later'), {
              title: this.$pgettext('ParametersUnit/Update/Toast/Error/Title', 'Updating part unit'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger'
            })
            logger.default.error('Cannot update part unit', error.message)
          })
      }
    },
    clearForm () {
      this.modalParameterUnit.name = ''
      this.modalParameterUnit.short_name = ''
      this.modalParameterUnit.description = ''
      this.$v.$reset()
    },
    deleteParametersUnit (ParametersUnit) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the part '${ParametersUnit.name}' ? Any associated part will loose that information.`, {
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
            apiService.deleteParametersUnits(ParametersUnit.id)
              .then((val) => {
                this.$bvToast.toast(this.$pgettext('ParametersUnit/Delete/Toast/Success/Message', 'Success'), {
                  title: this.$pgettext('ParametersUnit/Delete/Toast/Success/Title', 'Deleting part unit'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'primary'
                })
                this.fetchParametersUnits()
              })
              .catch((err) => {
                this.$bvToast.toast(this.$pgettext('ParametersUnit/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('ParametersUnit/Delete/Toast/Error/Title', 'Deleting part unit'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger'
                })
                logger.default.error('Error with part unit deletion', err)
                this.fetchParametersUnits()
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
