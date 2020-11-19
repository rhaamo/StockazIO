<template>
  <b-modal id="modalAddInventoryPart" ref="modalAddInventoryPart"
           size="xl" hide-footer @cancel="partModalClose"
           @close="partModalClose" @hidden="partModalClose"
           @shown="fetchParts(1, null)"
  >
    <template #modal-header="{ close }">
      <h5 id="modalPartTitle">
        Select part from inventory
      </h5>
      <button type="button" class="close" data-dismiss="modal"
              aria-label="Close" @click="close()"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </template>

    <div class="container">
      <div class="row">
        <div class="col-md-11 mx-auto">
          <b-form @submit.prevent="save">
            <b-row>
              <b-col>
                <b-form-group id="input-group-qty" label="Qty*" label-for="qty">
                  <b-form-input
                    id="qty"
                    v-model="form.qty"
                    required
                    type="number"
                    inputmode="numeric"
                    :state="$v.form.qty.$dirty ? !$v.form.qty.$error : null"
                  />
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group id="input-group-notes" label="Notes" label-for="notes">
                  <b-form-input
                    id="notes"
                    ref="inputnotes"
                    v-model="form.notes"
                    :state="$v.form.notes.$dirty ? !$v.form.notes.$error : null"
                  />
                </b-form-group>
              </b-col>
            </b-row>
            <b-form-group>
              <b-form-checkbox
                id="sourced"
                v-model="form.sourced"
                name="sourced"
                :value="true"
                :unchecked-value="false"
                inline
                :state="$v.form.sourced.$dirty ? !$v.form.sourced.$error : null"
              >
                Sourced
              </b-form-checkbox>
            </b-form-group>

            <hr>

            <div v-if="partSelected">
              <b>Selected part:</b> {{ partSelected.name }} <template v-if="partSelected.category">
                from <i>{{ partSelected.category.name }}</i>
              </template><br>
              <template v-if="partSelected.description">
                {{ partSelected.description }}
              </template>
            </div>

            <div v-if="!form.part_id">
              Please choose a part.
            </div>

            <hr>

            <div>
              <b-form @submit.prevent="searchPart">
                <b-input-group prepend="Search part" class="mt-3">
                  <b-form-input v-model="searchTerm" />
                  <b-input-group-append>
                    <b-button type="submit" variant="info">
                      <i class="fa fa-search" aria-hidden="true" />
                    </b-button>
                  </b-input-group-append>
                </b-input-group>
              </b-form>
            </div>

            <div>
              <b-table id="tablePartsList" ref="tablePartsList" :items="parts"
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
                  {{ data.item.name }}
                  <br>
                  <template v-if="data.item.description">
                    {{ data.item.category ? data.item.category.name : 'No category' }}: {{ data.item.description }}
                  </template>
                  <template v-else>
                    {{ data.item.category ? data.item.category.name : 'No category' }}
                  </template>
                </template>

                <template #cell(stock_qty)="data">
                  <span v-if="(data.item.stock_qty < data.item.stock_qty_min) || data.item.stock_qty == 0"
                        class="qtyMinWarning"
                  >{{ data.item.stock_qty }}
                    <i v-b-tooltip.hover class="fa fa-circle"
                       aria-hidden="true"
                       title="Current stock is below minimum stock quantity or exhausted"
                    />
                  </span>
                  <span v-else>{{ data.item.stock_qty }}</span>
                </template>

                <template #cell(footprint)="data">
                  <span
                    v-b-tooltip.hover
                    :title="data.item.footprint ? data.item.footprint.description : ''"
                  >
                    {{ data.item.footprint ? data.item.footprint.name : '-' }}
                  </span>
                </template>

                <template #cell(actions)="data">
                  <b-button :variant="(partSelected && partSelected.uuid === data.item.uuid) ? 'info' : 'outline-info'" @click.prevent="selectPart(data.item)">
                    <template v-if="partSelected && partSelected.uuid === data.item.uuid">
                      selected
                    </template>
                    <template v-else>
                      select
                    </template>
                  </b-button>
                </template>
              </b-table>
            </div>

            <div>
              <b-pagination
                v-model="currentPage"
                :total-rows="partsCount"
                :per-page="perPage"
                aria-controls="tablePartsList"
                @change="pageChanged"
              />
            </div>

            <b-button class="mt-3" type="submit" variant="primary">
              Add part
            </b-button>
          </b-form>
        </div>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, minValue, integer } from 'vuelidate/lib/validators'
import apiService from '@/services/api/api.service'
import logger from '@/logging'

export default {
  mixins: [
    validationMixin
  ],
  props: {
    project: {
      type: Object
    }
  },
  data: () => ({
    visible: false,
    form: {
      part_id: null,
      qty: 1,
      sourced: false,
      notes: ''
    },
    searchTerm: '',
    fields: [
      { key: 'name', label: 'Name', sortable: true, tdClass: 'name' },
      { key: 'stock_qty', label: 'Stock', sortable: false, tdClass: 'stock_qty' },
      { key: 'footprint', label: 'Footprint', sortable: true, tdClass: 'footprint' },
      { key: 'actions', label: '', sortable: false, tdClass: 'actions' }
    ],
    currentPage: 1,
    partsCount: 0,
    sortBy: 'name',
    sortDesc: false,
    parts: [],
    partSelected: null
  }),
  validations: {
    form: {
      part_id: { required, integer },
      qty: {
        required,
        minValue: minValue(0)
      },
      sourced: {},
      notes: {}
    }
  },
  computed: {
    perPage () {
      return 10
    }
  },
  methods: {
    fetchParts (page, opts) {
      logger.default.info('Fetching parts page', page, 'with opts', opts)
      let params = {
        page: page,
        size: this.perPage,
        ...opts
      }
      if (this.searchTerm && !params.search) {
        params.search = this.searchTerm
      }
      apiService.getParts(params)
        .then((res) => {
          this.parts = res.data.results
          this.partsCount = res.data.count
        })
    },
    partModalClose () {
      this.$bvModal.hide('modalAddInventoryPart')
      this.$emit('add-part-inventory-modal-closed')
    },
    save () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('form has errors')
        return
      }

      let part = {
        part: this.form.part_id,
        qty: this.form.qty,
        sourced: this.form.sourced,
        notes: this.form.notes,
        project: this.project.id
      }

      apiService.projectAddPart(this.project.id, part)
        .then(() => {
          this.$bvToast.toast(this.$pgettext('ProjectAddPart/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('ProjectAddPart/Update/Toast/Success/Title', 'Adding inventory part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.clearForm()
          this.$bvModal.hide('modalAddInventoryPart')
          this.$emit('add-part-inventory-saved')
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('ProjectAddPart/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('ProjectAddPart/Update/Toast/Error/Title', 'Adding inventory part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot add inventory part', error.message)
        })
    },
    clearForm () {
      this.form.part_id = null
      this.form.qty = 1
      this.form.sourced = false
      this.form.notes = ''
      this.partSelected = null
      this.$v.$reset()
    },
    sortTableChanged (ctx) {
      // When changing the sorting order, reset the pagination to page 1
      let opts = { ordering: ctx.sortDesc ? `-${ctx.sortBy}` : ctx.sortBy }
      this.fetchParts(1, opts)
    },
    pageChanged (page) {
      this.fetchParts(page, null)
    },
    searchPart () {
      this.fetchParts(1, { search: this.searchTerm })
    },
    selectPart (part) {
      this.partSelected = part
      this.form.part_id = part.id
    }
  }
}
</script>

<style>
table#tablePartsList td.stock_qty {
  width: 5em;
}

table#tablePartsList td.footprint {
  width: 8em;
}

table#tablePartsList td.actions {
  width: 8em;
}
</style>
