<template>
  <div class="presets_details">
    <div class="row">
      <div class="col-8">
        <ol class="breadcrumb">
          <li class="breadcrumb-item active">
            <router-link :to="{ name: 'parameters-presets-list' }">
              Part Parameters Presets
            </router-link>
          </li>
          <li class="breadcrumb-item active">
            {{ preset.name }}
          </li>
        </ol>
      </div>

      <div class="col-lg-3">
        <b-button variant="primary" :to="{ name: 'parameters-presets-edit', params: { presetId: presetId } }">
          <i
            class="fa fa-pencil-square-o"
            aria-hidden="true"
          />
        </b-button>
                &nbsp;
        <b-button variant="danger" @click.prevent="deletePreset(preset)">
          <i
            class="fa fa-trash-o"
            aria-hidden="true"
          />
        </b-button>
      </div>

    </div>

    <div class="row">
      <div class="col-md-8">
        <b-table id="tablePresetsList" ref="tablePresetItemsList" :items="preset.part_parameters_presets"
                 :fields="fields"
                 :sort-by.sync="sortBy" :sort-desc.sync="sortDesc"
                 condensed striped
                 sort-icon-left
                 show-empty
                 primary-key="uuid"
                 :no-local-sorting="true"
                 small
                 @sort-changed="sortTableChanged"
        >
          <template #cell(unit)="data">
            <template v-if="data.item.unit">{{ data.item.unit.name }} - {{ data.item.unit.prefix }}{{ data.item.unit.symbol }}</template>
          </template>
        </b-table>
      </div>
    </div>

  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'

export default {
  data: () => ({
    preset: {},
    fields: [
      { key: 'name', label: 'Name', sortable: true, tdClass: 'name' },
      { key: 'description', label: 'Description', sortable: false, tdClass: 'description' },
      { key: 'unit', label: 'Unit', sortable: false, tdClass: 'unit' }
    ],
    sortBy: 'name',
    sortDesc: false
  }),
  computed: {
    presetId () {
      return this.$route.params.presetId
    }
  },
  watch: {
  },
  created () {
    this.$nextTick(() => {
      this.fetchPreset(this.presetId)
    })
  },
  methods: {
    fetchPreset (presetId) {
      apiService.getPartParameterPreset(presetId)
        .then((res) => {
          this.preset = res.data
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::refresh::table', 'tablePresetItemsList')
        })
    },
    sortTableChanged (ctx) {
      // When changing the sorting order, reset the pagination to page 1
      let opts = ctx.sortDesc ? `-${ctx.sortBy}` : ctx.sortBy
      this.fetchPresets(1, opts)
    },
    pageChanged (page) {
      this.fetchPreset(this.presetId)
    },
    deletePreset (preset) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the preset '${preset.name}' ?`, {
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
            apiService.deletePartParameterPresets(preset.id)
              .then((val) => {
                this.$bvToast.toast(this.$pgettext('Preset/Delete/Toast/Success/Message', 'Success'), {
                  title: this.$pgettext('Preset/Delete/Toast/Success/Title', 'Deleting preset'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'primary',
                  toaster: 'b-toaster-top-center'
                })
                this.$router.push({ name: 'parameters-presets-list' })
              })
              .catch((err) => {
                this.$bvToast.toast(this.$pgettext('Preset/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('Preset/Delete/Toast/Error/Title', 'Deleting preset'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger',
                  toaster: 'b-toaster-top-center'
                })
                logger.default.error('Error with preset deletion', err)
                this.fetchParts(1, null)
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

<style>
table#tablePresetsList td.name {
  width: 25em;
}

table#tablePresetsList td.actions {
  width: 7em;
}
</style>
