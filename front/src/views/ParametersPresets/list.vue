<template>
  <div class="presets_list">
    <div class="row">
      <div class="col-8">
        <ol class="breadcrumb">
          <li class="breadcrumb-item active">
            <router-link :to="{ name: 'parameters-presets-list' }">
              Part Parameters Presets
            </router-link>
          </li>
        </ol>
      </div>

      <div class="col-xl-1 col-2">
        <b-btn :to="{name: 'parameters-presets-add'}">
          New
        </b-btn>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 mx-auto">
        <b-table
          id="tablePresetsList" ref="tablePresetsList" :items="presets"
          :fields="fields"
          :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" per-page="0"
          :current-page="currentPage"
          condensed striped
          sort-icon-left
          show-empty
          primary-key="uuid"
          :no-local-sorting="true"
          small
          @sort-changed="sortTableChanged"
        >
          <template #cell(name)="data">
            <p style="white-space: pre-line;">
              <router-link :to="{name: 'parameters-presets-details', params: { presetId: data.item.id }}">
                {{ data.item.name }}
              </router-link>
            </p>
          </template>

          <template #cell(actions)="data">
            <b-button variant="link" :to="{ name: 'parameters-presets-edit', params: { presetId: data.item.id } }">
              <i
                class="fa fa-pencil-square-o"
                aria-hidden="true"
              />
            </b-button>
                &nbsp;
            <b-button variant="link" @click.prevent="deletePreset(data.item)">
              <i
                class="fa fa-trash-o"
                aria-hidden="true"
              />
            </b-button>
          </template>
        </b-table>
      </div>
    </div>

    <b-row>
      <b-col md="6" offset-md="1">
        <b-pagination
          v-model="currentPage"
          :total-rows="presetsCount"
          :per-page="perPage"
          aria-controls="tablePartsList"
          @change="pageChanged"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'
import { useToast } from 'vue-toastification'
import ToastyToast from '@/components/toasty-toast'

export default {
  name: 'ParametersPresetsList',
  data: () => ({
    presets: [],
    fields: [
      { key: 'name', label: 'Name', sortable: true, tdClass: 'name' },
      { key: 'actions', label: 'Actions', tdClass: 'actions' }
    ],
    sortBy: 'name',
    sortDesc: false,
    currentPage: 1,
    presetsCount: 0
  }),
  computed: {
    perPage () {
      return 20
    }
  },
  watch: {
  },
  created () {
    this.$nextTick(() => {
      this.fetchPresets(1, null)
    })
  },
  setup () {
    const toast = useToast()
    return { toast }
  },
  methods: {
    fetchPresets (page, opts) {
      let params = {
        page: page,
        size: this.perPage,
        ...opts
      }
      apiService.getPartParameterPresets(params)
        .then((res) => {
          this.presets = res.data.results
          this.presetsCount = res.data.count
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::refresh::table', 'tablePresetsList')
        })
    },
    sortTableChanged (ctx) {
      // When changing the sorting order, reset the pagination to page 1
      let opts = ctx.sortDesc ? `-${ctx.sortBy}` : ctx.sortBy
      this.fetchPresets(1, opts)
    },
    pageChanged (page) {
      this.fetchPresets(page, null)
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
                this.toast.success({
                  component: ToastyToast,
                  props: {
                    title: this.$pgettext('Preset/Delete/Toast/Success/Title', 'Deleting preset'),
                    message: this.$pgettext('Preset/Delete/Toast/Success/Message', 'Success')
                  }
                })
                this.$store.commit('setPartParametersPresets', val.data)
                this.$store.commit('setLastUpdate', { item: 'parameters_presets', value: new Date() })
                this.fetchPresets(this.currentPage, null)
              })
              .catch((err) => {
                this.toast.error({
                  component: ToastyToast,
                  props: {
                    title: this.$pgettext('Preset/Delete/Toast/Error/Title', 'Deleting preset'),
                    message: this.$pgettext('Preset/Delete/Toast/Error/Message', 'An error occured, please try again later')
                  }
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
