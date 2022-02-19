<template>
  <div class="add_part">
    <ViewModal
      :part="partDetails" :can-delete="true" @delete-part="deletePart"
      @view-part-modal-closed="onPartModalClosed"
    />
    <modalLabelGenerator
      :items="modalLabelGeneratorItems" @modal-label-generator-closed="labelGeneratorClosed"
    />

    <div class="row">
      <div class="col-12">
        <ol class="breadcrumb">
          <template v-if="actualCurrentCategory && categoryId && categoryId !== '0'">
            <li class="breadcrumb-item">
              Parts by category
            </li>
            <li class="breadcrumb-item active">
              <router-link :to="{ name: 'parts-category-list', params: { categoryId: actualCurrentCategory.id, category: actualCurrentCategory } }">
                {{ actualCurrentCategory.name }}
              </router-link>
            </li>
          </template>
          <template v-else>
            <li class="breadcrumb-item active">
              <router-link :to="{ name: 'parts-list' }">
                All parts
              </router-link>
            </li>
          </template>
        </ol>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-2">
        <vue-multiselect
          v-model="filter.footprint" :options="choicesFootprint"
          group-values="footprints" group-label="category" placeholder="Filter footprint"
          label="name" track-by="id" @input="filterFootprintChanged"
        />
        <b-form-checkbox
          v-model="filter.footprint"
          :value="{id: 0}"
          :unchecked-value="null"
          inline
          @input="filterFootprintChanged"
        >
          No footprint
        </b-form-checkbox>
      </div>

      <div class="col-2">
        <vue-treeselect
          v-model="filter.storage" :multiple="false"
          :options="choicesStorageLocation" search-nested :default-expand-level="Infinity"
          clearable :normalizer="storagesNormalizer" no-children-text
          placeholder="Filter storage" :disable-branch-nodes="true"
          @input="filterStorageChanged"
        />
        <b-form-checkbox
          v-model="filter.storage"
          :value="0"
          :unchecked-value="null"
          inline
          @input="filterStorageChanged"
        >
          No storage
        </b-form-checkbox>
      </div>

      <div class="col-2">
        <b-form-checkbox
          v-model="filter.qty"
          value="qty"
          :unchecked-value="null"
          inline
        >
          Only out of stock
        </b-form-checkbox>
      </div>

      <div class="col-2">
        <b-form-checkbox
          v-model="filter.qty"
          value="qtyMin"
          :unchecked-value="null"
          inline
        >
          Only qty &lt; min
        </b-form-checkbox>
      </div>

      <div class="col-2">
        <b-form-checkbox v-model="bulkEditMode" name="check-button" switch>
          Bulk-edit
        </b-form-checkbox>
      </div>
    </div>

    <div v-if="bulkEditMode" class="row mb-3">
      <div class="col-3">
        Bulk edit options:<br>
        <b-button id="popoverChangeCategory" variant="info">
          Change category
        </b-button>&nbsp;
        <b-popover target="popoverChangeCategory" :show.sync="bulkEditNewCategoryPopover">
          <template #title>
            For selected parts
          </template>
          <div>
            <vue-treeselect
              v-model="bulkEditNewCategory" :multiple="false" :options="choicesCategory"
              search-nested :default-expand-level="Infinity" clearable
              :normalizer="categoriesNormalizer" no-children-text placeholder="Film resistors ? MCUS ?"
            />
            <br>
            <b-button size="sm" variant="danger" @click="onBulkEditNewCategoryPopoverClose">
              Cancel
            </b-button>
            &nbsp;
            <b-button
              size="sm" variant="primary" :disabled="!bulkEditNewCategory"
              @click="onBulkEditNewCategoryPopoverOk"
            >
              Ok
            </b-button>
          </div>
        </b-popover>

        <b-button id="popoverChangeStorageLocation" variant="info">
          Change location
        </b-button>&nbsp;
        <b-popover target="popoverChangeStorageLocation" :show.sync="bulkEditNewStorageLocationPopover">
          <template #title>
            For selected parts
          </template>
          <div>
            <vue-treeselect
              v-model="bulkEditNewStorageLocation" :multiple="false" :options="choicesStorageLocation"
              search-nested :default-expand-level="Infinity" clearable
              :normalizer="storagesNormalizer" no-children-text placeholder="A box under the bench or some drawer ?"
              :disable-branch-nodes="true"
            />
            <br>
            <b-button size="sm" variant="danger" @click="onBulkEditNewStorageLocationPopoverClose">
              Cancel
            </b-button>
            &nbsp;
            <b-button
              size="sm" variant="primary" :disabled="!bulkEditNewStorageLocation"
              @click="onBulkEditNewStorageLocationPopoverOk"
            >
              Ok
            </b-button>
          </div>
        </b-popover>

        <b-button variant="danger" @click.prevent="deleteAllSelected">
          Delete
        </b-button>
      </div>
    </div>

    <b-card no-body class="mb-4">
      <b-tabs card>
        <b-tab no-body title="Table" active>
          <b-table
            id="tablePartsList" ref="tablePartsList" :items="parts"
            :fields="bulkEditMode ? fieldsBulkEdit : fields"
            :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" per-page="0"
            :current-page="currentPage" :busy.sync="busy"
            condensed striped
            sort-icon-left
            show-empty
            primary-key="uuid"
            :no-local-sorting="true"
            small
            @sort-changed="sortTableChanged"
          >
            <template #cell(select)="data">
              <b-form-checkbox v-model="data.item.selected" />
            </template>

            <template #cell(qrcode)="data">
              <div @click="showLabelGenerator(data.item)">
                <qrcode
                  :id="qrcodeId(data.item.id)"
                  v-b-tooltip.hover
                  :value="qrCodePart(data.item.uuid)"
                  :options="{ scale: 1, color: {dark: '#000000', light:'#0000'} }"
                  title="show label generator"
                  :data-uuid="data.item.uuid"
                  :data-name="data.item.name"
                  data-toggle="modal"
                  data-target="#modalQrCode"
                />
              </div>
            </template>

            <template #cell(name)="data">
              <template v-if="partGetDefaultAttachment(data.item.part_attachments)">
                <i
                  :id="`p_a_${data.item.id}`" title="Hover to show picture"
                  class="fa fa-picture-o"
                  aria-hidden="true"
                />
                <b-popover
                  :target="`p_a_${data.item.id}`"
                  placement="left"
                  triggers="hover focus"
                >
                  <b-img-lazy :src="partGetDefaultAttachment(data.item.part_attachments).picture_medium" width="250px" />
                </b-popover>
              &nbsp;&nbsp;
              </template>
              <a href="#" @click.prevent="viewPartModal(data.item)">{{ data.item.name }}</a>
              <br>
              <template v-if="data.item.description">
                {{ data.item.category ? data.item.category.name : 'No category' }}: {{ data.item.description }}
              </template>
              <template v-else>
                {{ data.item.category ? data.item.category.name : 'No category' }}
              </template>
            </template>

            <template #cell(storage)="data">
              {{ data.item.storage && data.item.storage.name ? data.item.storage.name : '-' }}
            </template>

            <template #cell(part_unit)="data">
              {{ data.item.part_unit && data.item.part_unit.name ? data.item.part_unit.name : '-' }}
            </template>

            <template #cell(stock_qty)="data">
              <span
                v-if="(data.item.stock_qty < data.item.stock_qty_min) || data.item.stock_qty == 0" :id="popoverStockQtyClass(data.item.id)"
                class="qtyMinWarning"
              >{{ data.item.stock_qty }}
                <i
                  v-b-tooltip.hover class="fa fa-circle"
                  aria-hidden="true"
                  title="Current stock is below minimum stock quantity or exhausted"
                />
              </span>
              <span
                v-else :id="popoverStockQtyClass(data.item.id)" v-b-tooltip.hover
                title="click to change qty"
              >{{ data.item.stock_qty }}</span>

              <b-popover
                :target="popoverStockQtyClass(data.item.id)"
                triggers="click"
                placement="auto"
                container="tablePartsList"
              >
                <template #title>
                  Change stock qty
                </template>

                <div align="center">
                  <b-form-spinbutton v-model="data.item.stock_qty" min="0" />
                  <br>
                  <b-button
                    size="sm" type="submit" variant="primary"
                    @click.prevent="popoverQtyUpdatePart(data.item.id, data.item.stock_qty)"
                  >
                    update
                  </b-button>
                </div>
              </b-popover>
            </template>

            <template #cell(stock_qty_min)="data">
              <span :id="popoverStockQtyMinClass(data.item.id)">{{ data.item.stock_qty_min }}</span>

              <b-popover
                :target="popoverStockQtyMinClass(data.item.id)"
                triggers="click"
                placement="auto"
                container="tablePartsList"
              >
                <template #title>
                  Change stock min qty
                </template>

                <div align="center">
                  <b-form-spinbutton v-model="data.item.stock_qty_min" min="0" />
                  <br>
                  <b-button
                    size="sm" type="submit" variant="primary"
                    @click.prevent="popoverQtyMinUpdatePart(data.item.id, data.item.stock_qty_min)"
                  >
                    update
                  </b-button>
                </div>
              </b-popover>
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
              <b-button variant="link" :to="{ name: 'parts-edit', params: { partId: data.item.id } }">
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
        <b-tab title="Thumbnails">
          <b-card-group
            v-for="(row, idx) in thumbnailsChunked" :key="idx" deck
            class="mb-4"
          >
            <b-card
              v-for="part in row" :key="part.id"
              :title="part.name"
              img-top
            >
              <b-card-text>{{ part.description || 'No description.' }}</b-card-text>
              <b-card-img-lazy
                v-if="partGetDefaultAttachment(part.part_attachments)" :src="partGetDefaultAttachment(part.part_attachments).picture_medium"
                top
              />
              <template v-else>
                <span class="fa-stack fa-5x">
                  <i class="fa fa-file-picture-o fa-stack-2x" />
                  <i class="fa fa-question fa-stack-1x text-warning" />
                </span>
              </template>
              <template #footer>
                <small class="text-muted">Qty: {{ part.stock_qty }}</small>
                <b-button
                  size="sm" variant="outline-primary" class="pull-right"
                  @click.prevent="viewPartModal(part)"
                >
                  View details
                </b-button>
              </template>
            </b-card>
          </b-card-group>
        </b-tab>
      </b-tabs>
    </b-card>

    <b-row>
      <b-col md="6" offset-md="1">
        <b-pagination
          v-model="currentPage"
          :total-rows="partsCount"
          :per-page="perPage"
          aria-controls="tablePartsList"
          @change="pageChanged"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import apiService from '../../services/api/api.service'
import logger from '@/logging'
import { mapState } from 'vuex'
import ViewModal from '@/components/parts/view_modal'
import modalLabelGenerator from '@/components/labels/modal-label-generator.vue'
import _ from '@/lodash'

export default {
  name: 'PartsList',
  components: {
    ViewModal,
    modalLabelGenerator
  },
  props: {
    category: {
      type: Object
    }
  },
  data: () => ({
    parts: [],
    currentPage: 1,
    partDetails: null,
    partsCount: 0,
    fields: [
      { key: 'qrcode', label: 'QrCode', tdClass: 'qrCode' },
      { key: 'name', label: 'Name', sortable: true },
      { key: 'storage', label: 'Storage', sortable: true },
      { key: 'stock_qty', label: 'Stock', sortable: true },
      { key: 'stock_qty_min', label: 'Min', sortable: true },
      { key: 'part_unit', label: 'Unit', sortable: true },
      { key: 'footprint', label: 'Footprint', sortable: true },
      { key: 'actions', label: 'Actions' }
    ],
    fieldsBulkEdit: [
      { key: 'select', label: '', tdClass: 'select' },
      { key: 'qrcode', label: 'QrCode', tdClass: 'qrCode' },
      { key: 'name', label: 'Name', sortable: true },
      { key: 'storage', label: 'Storage', sortable: true },
      { key: 'stock_qty', label: 'Stock', sortable: true },
      { key: 'stock_qty_min', label: 'Min', sortable: true },
      { key: 'part_unit', label: 'Unit', sortable: true },
      { key: 'footprint', label: 'Footprint', sortable: true },
      { key: 'actions', label: 'Actions' }
    ],
    sortBy: 'name',
    sortDesc: false,
    busy: false,
    popoverStockQtyShow: false,
    filter: {
      footprint: null,
      storage: null,
      qty: null
    },
    modalLabelGeneratorItems: [],
    bulkEditMode: false,
    bulkEditNewCategoryPopover: false,
    bulkEditNewCategory: null,
    bulkEditNewStorageLocationPopover: false,
    bulkEditNewStorageLocation: null
  }),
  computed: {
    ...mapState({
      currentCategory: state => { return state.preloads.currentCategory },
      serverSettings: state => state.server.settings,
      choicesCategory: state => { return [state.preloads.categories] },
      choicesStorageLocation: (state) => state.preloads.storages,
      choicesFootprint: (state) => {
        return state.preloads.footprints.map(x => { return { category: x.name, footprints: x.footprint_set.map(y => { return { id: y.id, name: y.name } }) } })
      },
      categories: state => { return [state.preloads.categories] }
    }),
    perPage () {
      return this.serverSettings.pagination.PARTS || 10
    },
    categoryId () {
      return this.$route.params.categoryId
    },
    storageId () {
      return this.$route.query.storage
    },
    storageUuid () {
      return this.$route.query.storage_uuid
    },
    searchQuery () {
      return this.$route.query.q
    },
    actualCurrentCategory () {
      return this.category || this.currentCategory
    },
    selectedParts () {
      return this.parts.filter(x => {
        if (x.selected) {
          return x
        }
      })
    },
    thumbnailsChunked () {
      return _.chunk(this.parts, 6)
    }
  },
  watch: {
    'categoryId': function () {
      this.fetchParts(1, null)
      this.categoryChanged()
    },
    'searchQuery': function () {
      this.fetchParts(1, { search: this.searchQuery })
    },
    'filter.qty': function () {
      if (this.filter.qty === 'qty') {
        this.fetchParts(1, { qtyType: 'qty' })
      } else if (this.filter.qty === 'qtyMin') {
        this.fetchParts(1, { qtyType: 'qtyMin' })
      } else {
        this.fetchParts(1, null)
      }
    },
    'storageUuid': function () {
      this.fetchParts(1, { storage_uuid: this.storageUuid })
    }
  },
  created () {
    this.$nextTick(() => {
      if (this.searchQuery) {
        this.fetchParts(1, { search: this.searchQuery })
      } else if (this.storageUuid) {
        this.fetchParts(1, { storage_uuid: this.storageUuid })
      } else {
        this.fetchParts(1, null)
        this.categoryChanged()
      }
    })
  },
  methods: {
    categoryChanged () {
      if (!this.categoryId || Number(this.categoryId) === 0) {
        this.$store.commit('setCurrentCategory', { id: this.categoryId, name: 'none' })
        return
      }
      let curCat = null
      const cb = (e) => {
        if (e.id === Number(this.categoryId)) {
          curCat = e
        }
        e.children.forEach(cb)
      }
      this.categories.forEach(cb)
      this.$store.commit('setCurrentCategory', { id: this.categoryId, name: curCat.name })
    },
    popoverQtyUpdatePart (id, qty) {
      apiService.updatePartialPart(id, { stock_qty: qty })
        .then(() => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Update/Toast/Success/Title', 'Updating part qty'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::hide::popover', this.popoverStockQtyClass(id))
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Update/Toast/Error/Title', 'Updating part qty'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot update part qty', error.message)
        })
    },
    popoverStockQtyClass (id) {
      return `popover-stock-qty-${id}`
    },
    popoverQtyMinUpdatePart (id, qty) {
      apiService.updatePartialPart(id, { stock_qty_min: qty })
        .then(() => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Update/Toast/Success/Title', 'Updating min part qty'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::hide::popover', this.popoverStockQtyMinClass(id))
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Update/Toast/Error/Title', 'Updating min part qty'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot update min part qty', error.message)
        })
    },
    popoverStockQtyMinClass (id) {
      return `popover-stock-qty-min-${id}`
    },
    pageChanged (page) {
      this.fetchParts(page, null)
    },
    sortTableChanged (ctx) {
      // When changing the sorting order, reset the pagination to page 1
      let opts = { ordering: ctx.sortDesc ? `-${ctx.sortBy}` : ctx.sortBy }
      this.fetchParts(1, opts)
    },
    qrcodeId (id, size) {
      return size ? `qrcode-${id}-${size}` : `qrcode-${id}`
    },
    qrCodePart (uuid) {
      return `web+stockazio:part,${uuid}`
    },
    showLabelGenerator (part) {
      this.closeBulkEditPopovers()
      this.modalLabelGeneratorItems = [part]
      // We need to wait a tick or the previous set will not be finalized before the modal is shown
      this.$nextTick(() => {
        this.$bvModal.show('modalLabelGenerator')
      })
    },
    labelGeneratorClosed () {
      this.modalLabelGeneratorItems = []
    },
    fetchParts (page, opts) {
      console.log('we have', this.perPage, 'per page')
      let params = {
        page: page,
        size: this.perPage,
        ...opts
      }
      if (this.categoryId !== null) {
        params.category_id = this.categoryId
      }
      if (this.searchQuery) {
        params.search = this.searchQuery
      }
      if (this.storageId && !this.filter.storage) {
        params.storage_id = this.storageId
      }
      if (this.storageUuid && !this.filter.storage) {
        params.storage_uuid = this.storageUuid
      }
      if (this.filter.footprint) {
        params.footprint_id = this.filter.footprint.id
      }
      if (this.filter.qty === 'qty') {
        params.qtyType = 'qty'
      } else if (this.filter.qty === 'qtyMin') {
        params.qtyType = 'qtyMin'
      }

      this.busy = true
      apiService.getParts(params)
        .then((res) => {
          this.parts = res.data.results
          this.partsCount = res.data.count
          this.busy = false
          this.bulkEditNewCategory = null
          this.bulkEditNewCategoryPopover = false
          this.bulkEditNewStorageLocation = null
          this.bulkEditNewStorageLocationPopover = false
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::refresh::table', 'tablePartsList')
        })
    },
    deletePart (part) {
      this.closeBulkEditPopovers()
      let categoryId = part.category ? part.category.id : null

      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the part '${part.name}' ?`, {
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
            apiService.deletePart(part.id)
              .then((val) => {
                this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Success/Message', 'Success'), {
                  title: this.$pgettext('Part/Delete/Toast/Success/Title', 'Deleting part'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'primary',
                  toaster: 'b-toaster-top-center'
                })
                this.fetchParts(1, null)
                this.$store.commit('decrementCategoryPartsCount', { nodeId: categoryId })
              })
              .catch((err) => {
                this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('Part/Delete/Toast/Error/Title', 'Deleting part'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger',
                  toaster: 'b-toaster-top-center'
                })
                logger.default.error('Error with part deletion', err)
                this.fetchParts(1, null)
              })
          }
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    },
    deleteAllSelected () {
      this.closeBulkEditPopovers()
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete all the selected parts ?`, {
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
            const _bulkDelete = async (parts) => {
              for (let x of parts) {
                await apiService.deletePart(x.id)
                  .then(() => {
                    this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Success/Message', 'Success'), {
                      title: this.$pgettext('Part/Delete/Toast/Success/Title', 'Deleting part'),
                      autoHideDelay: 5000,
                      appendToast: true,
                      variant: 'primary',
                      toaster: 'b-toaster-top-center'
                    })
                    this.$store.commit('decrementCategoryPartsCount', { nodeId: this.actualCurrentCategory.id })
                  })
                  .catch((err) => {
                    this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                      title: this.$pgettext('Part/Delete/Toast/Error/Title', 'Deleting part'),
                      autoHideDelay: 5000,
                      appendToast: true,
                      variant: 'danger',
                      toaster: 'b-toaster-top-center'
                    })
                    logger.default.error('Error with part deletion', err)
                  })
              }
            }
            _bulkDelete(this.selectedParts)
              .then(() => {
              // Then reload
                this.fetchParts(1, null)
              })
          }
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    },
    viewPartModal (part) {
      this.closeBulkEditPopovers()
      apiService.getPart(part.id)
        .then((val) => {
          this.partDetails = val.data
          this.$bvModal.show('modalManage')
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('Part/ShowModal/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/ShowModal/Toast/Error/Title', 'Part details'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error fetching part', err)
          this.partDetails = null
        })
    },
    storagesNormalizer: function (node) {
      let childs = (node.children || []).concat(node.storage_locations || [])
      let id = node.uuid ? node.id : `cat_${node.id}`
      return { id: id, label: node.name, children: childs && childs.length ? childs : 0 }
    },
    categoriesNormalizer: function (node) {
      return { id: node.id, label: node.name, children: node.children && node.children.length ? node.children : 0 }
    },
    filterFootprintChanged (value, id) {
      if (value) {
        this.fetchParts(1, { footprint_id: value.id })
      } else {
        this.fetchParts(1, null)
      }
    },
    filterStorageChanged (value, id) {
      if (value || value === 0) {
        this.fetchParts(1, { storage_id: value })
      } else {
        this.fetchParts(1, null)
      }
    },
    onPartModalClosed () {
      this.partDetails = null
    },
    partGetDefaultAttachment (attachments) {
      // If only one attachment, and it is a picture, elect as default
      if (attachments.length === 1 && attachments[0].picture) {
        return attachments[0]
      }

      // Else return the one marked as default
      let att = attachments.filter(x => {
        if (x.picture_default) {
          return x
        }
      })[0] // return first item
      if (att) {
        return att
      }

      // Else return first attachment being an image
      return attachments.filter(x => {
        if (x.picture) {
          return x
        }
      })[0] // return first item
    },
    onBulkEditNewCategoryPopoverClose () {
      this.bulkEditNewCategory = null
      this.bulkEditNewCategoryPopover = false
    },
    onBulkEditNewCategoryPopoverOk () {
      if (!(this.selectedParts && this.selectedParts.length)) {
        return
      }

      let ids = this.selectedParts.map(x => { return x.id })

      apiService.changePartsCategory(ids, this.bulkEditNewCategory)
        .then((val) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Update/Toast/Success/Title', 'Updating part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.fetchParts(1, null)

          this.$nextTick(() => {
            this.$store.commit('decrementCategoryPartsCount', { nodeId: this.actualCurrentCategory.id, by: ids.length })
            this.$store.commit('incrementCategoryPartsCount', { nodeId: this.bulkEditNewCategory, by: ids.length })
            this.bulkEditNewCategoryPopover = false
          })
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Update/Toast/Error/Title', 'Updating part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error with category part update', err)
          this.fetchParts(1, null)
        })
    },
    closeBulkEditPopovers () {
      this.bulkEditNewCategoryPopover = false
      this.bulkEditNewStorageLocationPopover = false
    },
    onBulkEditNewStorageLocationPopoverClose () {
      this.closeBulkEditPopovers()
      this.bulkEditNewStorageLocationPopover = false
    },
    onBulkEditNewStorageLocationPopoverOk () {
      if (!(this.selectedParts && this.selectedParts.length)) {
        return
      }

      let ids = this.selectedParts.map(x => { return x.id })

      apiService.changePartsStorageLocation(ids, this.bulkEditNewStorageLocation)
        .then((val) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('Part/Update/Toast/Success/Title', 'Updating part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.fetchParts(1, null)

          this.$nextTick(() => {
            this.closeBulkEditPopovers()
          })
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('Part/Update/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Update/Toast/Error/Title', 'Updating part'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error with category storage location update', err)
          this.fetchParts(1, null)
        })
    }
  }
}
</script>
