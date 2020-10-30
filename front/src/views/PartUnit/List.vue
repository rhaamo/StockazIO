<template>
  <div class="list_part_unit">
    <b-modal id="modalAddPartUnit" ref="modalAddPartUnit"
             size="sm" :hide-footer="true"
             @cancel="modalAddPartUnitClose"
             @close="modalAddPartUnitClose"
             @hidden="modalAddPartUnitClose"
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
            <b-form @submit.prevent="savePartUnit">
              <b-form-group id="input-group-name" label="Name*" label-for="name">
                <b-form-input
                  id="name"
                  v-model="modalPartUnit.name"
                  required
                  placeholder="Centimeters"
                  :state="$v.modalPartUnit.name.$dirty ? !$v.modalPartUnit.name.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-short-name" label="Short Name*" label-for="short-name">
                <b-form-input
                  id="short-name"
                  v-model="modalPartUnit.short_name"
                  required
                  placeholder="cm"
                  :state="$v.modalPartUnit.short_name.$dirty ? !$v.modalPartUnit.short_name.$error : null"
                />
              </b-form-group>
              <b-form-group id="input-group-description" label="Description" label-for="description">
                <b-form-input
                  id="description"
                  v-model="modalPartUnit.description"
                  placeholder=""
                  :state="$v.modalPartUnit.description.$dirty ? !$v.modalPartUnit.description.$error : null"
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
      <b-col md="9">
        <b-breadcrumb>
          <b-breadcrumb-item>Part Units</b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
      <b-col md="2">
        <b-button
          variant="info"
          @click.prevent="showAddPartUnitModal"
        >
          Add a part unit
        </b-button>
      </b-col>
    </b-row>

    <b-row>
      <b-col md="6" offset-md="1">
        <b-table
          :items="partUnits"
          :fields="fields"
          :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc"
          responsive="sm"
          striped
        >
          <template #cell(actions)="data">
            <b-button
              variant="link"
              @click.prevent="showEditPartUnitModal(data.item)"
            >
              <i
                class="fa fa-pencil-square-o"
                aria-hidden="true"
              />
            </b-button>
        &nbsp;
            <b-button
              variant="link"
              @click.prevent="deletePartUnit(data.item)"
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
  </div>
</template>

<script>
import apiService from '../../services/api/api.service'
import logger from '@/logging'
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {
  mixins: [
    validationMixin
  ],
  props: {
  },
  data: () => ({
    partUnits: [],
    page: 0, // TODO/FIXME no pagination yet
    search_query: '', // TODO/FIXME no search yet
    fields: [
      { key: 'name', label: 'Name', sortable: true },
      { key: 'short_name', label: 'Short name' },
      { key: 'description', label: 'Description' },
      { key: 'actions', label: 'Actions' }
    ],
    sortBy: 'name',
    sortDesc: false,
    modalTitle: '',
    modalPartUnit: {
      name: '',
      short_name: '',
      description: ''
    },
    modalAction: 'create'
  }),
  validations: {
    modalPartUnit: {
      name: { required },
      short_name: { required },
      description: {}
    }
  },
  computed: {
  },
  watch: {
  },
  created () {
    this.fetchPartUnits()
  },
  methods: {
    fetchPartUnits () {
      apiService.getPartUnits()
        .then((val) => {
          this.partUnits = val.data
          console.log(val.data)
          this.$store.dispatch('preloadPartUnits')
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('PartUnits/Fetch/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('PartUnits/Fetch/Toast/Error/Title', 'Fetching part units'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Error getting part units', err)
        })
    },
    showAddPartUnitModal (partUnit) {
      this.modalPartUnit = { ...partUnit }
      this.modalTitle = 'Add Part Unit'
      this.modalAction = 'create'
      this.$bvModal.show('modalAddPartUnit')
    },
    showEditPartUnitModal (partUnit) {
      this.modalPartUnit = { ...partUnit }
      this.modalTitle = 'Edit Part Unit'
      this.modalAction = 'edit'
      this.$bvModal.show('modalAddPartUnit')
    },
    modalAddPartUnitClose () {
      this.modalTitle = ''
      this.clearForm()
    },
    savePartUnit () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        return
      }

      if (this.modalAction === 'create') {
        apiService.createPartUnit(this.modalPartUnit)
          .then(() => {
            this.$bvToast.toast(this.$pgettext('PartUnit/Add/Toast/Success/Message', 'Success'), {
              title: this.$pgettext('PartUnit/Add/Toast/Success/Title', 'Adding part unit'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'primary'
            })
            this.$bvModal.hide('modalAddPartUnit')
            this.clearForm()
            this.fetchPartUnits()
          })
          .catch((error) => {
            this.$bvToast.toast(this.$pgettext('PartUnit/Add/Toast/Error/Message', 'An error occured, please try again later'), {
              title: this.$pgettext('PartUnit/Add/Toast/Error/Title', 'Adding part unit'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger'
            })
            logger.default.error('Cannot save part unit', error.message)
          })
      } else {
        apiService.updatePartUnit(this.modalPartUnit.id, this.modalPartUnit)
          .then(() => {
            this.$bvToast.toast(this.$pgettext('PartUnit/Update/Toast/Success/Message', 'Success'), {
              title: this.$pgettext('PartUnit/Update/Toast/Success/Title', 'Updating part unit'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'primary'
            })
            this.$bvModal.hide('modalAddPartUnit')
            this.clearForm()
            this.fetchPartUnits()
          })
          .catch((error) => {
            this.$bvToast.toast(this.$pgettext('PartUnit/Update/Toast/Error/Message', 'An error occured, please try again later'), {
              title: this.$pgettext('PartUnit/Update/Toast/Error/Title', 'Updating part unit'),
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger'
            })
            logger.default.error('Cannot update part unit', error.message)
          })
      }
    },
    clearForm () {
      this.modalPartUnit.name = ''
      this.modalPartUnit.short_name = ''
      this.modalPartUnit.description = ''
      this.$v.$reset()
    },
    deletePartUnit (partUnit) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the part '${partUnit.name}' ?`, {
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

          apiService.deletePartUnit(partUnit.id)
            .then((val) => {
              this.$bvToast.toast(this.$pgettext('PartUnit/Delete/Toast/Success/Message', 'Success'), {
                title: this.$pgettext('PartUnit/Delete/Toast/Success/Title', 'Deleting part unit'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'primary'
              })
              this.fetchPartUnits()
            })
            .catch((err) => {
              this.$bvToast.toast(this.$pgettext('PartUnit/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                title: this.$pgettext('PartUnit/Delete/Toast/Error/Title', 'Deleting part unit'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'danger'
              })
              logger.default.error('Error with part unit deletion', err)
              this.fetchPartUnits()
            })
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    }
  }
}
</script>
