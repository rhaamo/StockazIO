<template>
  <div class="details_part">
    <div v-if="part" class="row">
      <div class="col-lg-9">
        <span class="float-left" @click="showBigQrCode(part)">
          <qrcode
            :id="qrcodeId(part.id)"
            v-b-tooltip.hover
            :value="qrCodePart(part.uuid)"
            :options="{ scale: 1 }"
            title="click to show bigger QrCode"
            :data-uuid="part.uuid"
            :data-name="part.name"
            data-toggle="modal"
            data-target="#modalQrCode"
          />
        </span>
        <h3>
          <i :class="partDetailsPrivate" /> {{ part.name }}
        </h3>
      </div>
      <div class="col-lg-3">
        <b-button variant="link" :to="{ name: 'parts-edit', params: { partId: part.id } }">
          <i
            class="fa fa-pencil-square-o"
            aria-hidden="true"
          />
        </b-button>
                &nbsp;
        <b-button variant="link" @click.prevent="deletePart(part)">
          <i
            class="fa fa-trash-o"
            aria-hidden="true"
          />
        </b-button>
      </div>
    </div>

    <div v-if="part" class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-md-12">
            <div class="row no-gutters">
              <div class="col-md-3">
                <b>Qty:</b> <span class="qty">{{ part.stock_qty || 0 }}</span>
              </div>
              <div class="col-md-3">
                <b>Min:</b> <span class="qty-min">{{ part.stock_qty_min || 0 }}</span>
              </div>
              <div class="col-md-6">
                <b>Unit:</b> <span class="unit">{{ partDetailsUnit }}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12">
                <div class="description">
                  {{ part.description || '' }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-lg-12">
            <table class="table table-sm table-striped">
              <tbody>
                <tr>
                  <td>Footprint:</td>
                  <td><span class="footprint">{{ partDetailsFootprint }}</span></td>
                </tr>
                <tr>
                  <td>Storage:</td>
                  <td>
                    <span class="storage">{{ partDetailsStorage }}</span>
                    <template v-if="part.storage && part.storage.picture">
                      &nbsp;<i v-b-tooltip.hover class="fa fa-picture-o" title="Show location picture"
                               aria-hidden="true" @click="showLocationPicture"
                      />
                    </template>
                  </td>
                </tr>
                <tr>
                  <td>Category:</td>
                  <td><span class="category">{{ partDetailsCategory }}</span></td>
                </tr>
                <tr>
                  <td>Internal part number:</td>
                  <td><span class="internal-pn">{{ part.internal_part_number || '' }}</span></td>
                </tr>
                <tr>
                  <td>Comment:</td>
                  <td><span class="comment">{{ part.comment || '' }}</span></td>
                </tr>
                <tr>
                  <td>Production remarks:</td>
                  <td><span class="production-remarks">{{ part.production_remarks || '' }}</span></td>
                </tr>
                <tr>
                  <td>Sheet Need review:</td>
                  <td><i title="Shet review needed" :class="partDetailsNeedReviewClasses" /> <span class="need-review" /><span class="sheet-status" /></td>
                </tr>
                <tr>
                  <td>Part Condition:</td>
                  <td><span class="condition">{{ part.condition || '' }}</span></td>
                </tr>
                <tr>
                  <td>Can be sold:</td>
                  <td><i title="Can be sold" :class="partDetailsCanBeSoldClasses" /> <span class="can-be-sold" /></td>
                </tr>

                <tr>
                  <td>Added:</td>
                  <td>{{ partDetailsAddedOn }}</td>
                </tr>
                <tr>
                  <td>Updated:</td>
                  <td>{{ partDetailsUpdatedOn }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <b-tabs content-class="mt-3">
          <b-tab title="Parameters">
            <table id="table-parameters" class="table table-sm table-striped">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody v-if="part.part_parameters_value && part.part_parameters_value.length">
                <tr v-for="pu in part.part_parameters_value" :key="pu.id">
                  <td>{{ pu.name }}</td>
                  <td>{{ pu.description }}</td>
                  <td v-if="pu.unit">
                    {{ pu.value }}{{ pu.unit.symbol || '' }} ({{ pu.unit.name }})
                  </td>
                  <td v-else>
                    {{ pu.value }}
                  </td>
                </tr>
              </tbody>
            </table>
          </b-tab>
          <b-tab title="Distributors">
            <table id="table-distributors" class="table table-sm table-striped">
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Distributor</th>
                  <th>Datasheet</th>
                </tr>
              </thead>
              <tbody v-if="part.distributors_sku && part.distributors_sku.length">
                <tr v-for="dist in part.distributors_sku" :key="dist.id">
                  <td>{{ dist.sku }}</td>
                  <td>{{ dist.distributor.name }}</td>
                  <td v-if="dist.datasheet_url">
                    <a :href="dist.datasheet_url" target="_blank"><i class="fa fa-file-pdf-o" aria-hidden="true" /> {{ dist.datasheet_url }}</a>
                  </td>
                  <td v-else />
                </tr>
              </tbody>
            </table>
          </b-tab>
          <b-tab title="Manufacturers">
            <table id="table-manufacturers" class="table table-sm table-striped">
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Manufacturer</th>
                  <th>Datasheet</th>
                </tr>
              </thead>
              <tbody v-if="part.manufacturers_sku && part.manufacturers_sku.length">
                <tr v-for="manuf in part.manufacturers_sku" :key="manuf.id">
                  <td>{{ manuf.sku }}</td>
                  <td><img v-if="manuf.manufacturer && manuf.manufacturer.logo" :src="manuf.manufacturer.logo_mini" style="max-width:100px;">&nbsp;{{ manuf.manufacturer ? manuf.manufacturer.name : '-' }}</td>
                  <td v-if="manuf.datasheet_url">
                    <a :href="manuf.datasheet_url" target="_blank"><i class="fa fa-file-pdf-o" aria-hidden="true" /> {{ manuf.datasheet_url }}</a>
                  </td>
                  <td v-else />
                </tr>
              </tbody>
            </table>
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
              <tbody v-if="part.part_attachments && part.part_attachments.length">
                <tr v-for="file in part.part_attachments" :key="file.id">
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

          <b-tab title="Stock history">
            <table id="table-stock-history" class="table table-sm table-striped">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Amount</th>
                  <th />
                </tr>
              </thead>
              <tbody v-if="part.part_stock_history && part.part_stock_history.length">
                <tr v-for="psh in part.part_stock_history" :key="psh.id">
                  <td style="width: 15em;">
                    {{ formatDate(psh.created_at) }}
                  </td>
                  <td>{{ psh.diff }}</td>
                </tr>
              </tbody>
            </table>
          </b-tab>
        </b-tabs>
      </div>
    </div>
    <div v-else class="row">
      <div class="col-md-6">
        Part not yet loaded.
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '../../services/api/api.service'
import QRCode from 'qrcode'
import logger from '@/logging'
import { mapState } from 'vuex'
import moment from 'moment'

export default {
  props: {
    category: {
      type: Object
    }
  },
  data: () => ({
    part: null,
    addAttachmentForm: {
      description: '',
      file: null
    }
  }),
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings
    }),
    partId () {
      return this.$route.params.partId
    },
    partDetailsNeedReviewClasses () { return this.part && this.part.needs_review ? 'fa icon-need-review fa-check' : 'fa icon-need-review fa-close' },
    partDetailsCanBeSoldClasses () { return this.part && this.part.can_be_sold ? 'fa icon-need-review fa-dollar' : 'fa icon-need-review fa-close' },
    partDetailsPrivate () { return this.part && this.part.private ? 'fa icon-private fa-lock' : '' },
    partDetailsUnit () {
      if (this.part && this.part.part_unit) {
        if (this.part.part_unit.short_name) {
          return `${this.part.part_unit.name} (${this.part.part_unit.short_name})`
        } else {
          return this.part.part_unit.name
        }
      } else {
        return ''
      }
    },
    partDetailsFootprint () {
      if (this.part && this.part.footprint) {
        return this.part.footprint.name
      } else {
        return ''
      }
    },
    partDetailsStorage () {
      if (this.part && this.part.storage) {
        return this.part.storage.name
      } else {
        return ''
      }
    },
    partDetailsCategory () {
      if (this.part && this.part.category) {
        return this.part.category.name
      } else {
        return ''
      }
    },
    allowedUploadTypes () {
      let types = this.serverSettings.partAttachmentAllowedTypes || ['application/pdf', 'image/jpeg']
      return types.join(', ')
    },
    partDetailsAddedOn () {
      return this.part && this.part.created_at ? this.formatDate(this.part.created_at) : ''
    },
    partDetailsUpdatedOn () {
      return this.part && this.part.updated_at ? this.formatDate(this.part.updated_at) : ''
    }
  },
  watch: {
  },
  created () {
    this.fetchPart()
  },
  methods: {
    formatDate (date) {
      return moment(date).format('ddd MMM D YYYY HH:mm zz')
    },
    qrcodeId (id, size) {
      return size ? `qrcode-${id}-${size}` : `qrcode-${id}`
    },
    qrCodePart (uuid) {
      return `stockazio://part/${uuid}`
    },
    async showBigQrCode (part) {
      let qrCodeDataUrl = await QRCode.toDataURL(this.qrCodePart(part.uuid), { width: 300 }).then((url) => { return url })

      const h = this.$createElement
      const titleVNode = h('div', { domProps: { innerHTML: `QrCode for: ${part.name}` } })
      const messageVNode = h('div', { domProps: { style: 'text-align: center;' } }, [
        h('img', { domProps: { src: qrCodeDataUrl } }),
        h('div', {}, ['The content of the QrCode is:', h('br'), h('code', { class: ['qrCodeText'] }, [this.qrCodePart(part.uuid)])])
      ])
      this.$bvModal.msgBoxOk([messageVNode], {
        title: [titleVNode],
        buttonSize: 'sm',
        centered: true,
        size: 'lg'
      })
    },
    fetchPart () {
      apiService.getPart(this.partId)
        .then((res) => {
          this.part = res.data
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('Part/Details/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('Part/Details/Toast/Error/Title', 'Fetching part details'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error with part deletion', err.message)
        })
    },
    deletePart (part) {
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

          apiService.deletePart(part.id)
            .then((val) => {
              this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Success/Message', 'Success'), {
                title: this.$pgettext('Part/Delete/Toast/Success/Title', 'Deleting part'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'primary',
                toaster: 'b-toaster-top-center'
              })
              this.$store.commit('decrementCategoryPartsCount', categoryId)
              this.$router.push({ name: 'home' })
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
              this.fetchPart()
            })
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    },
    showLocationPicture () {
      let storage = this.part.storage
      const h = this.$createElement
      const titleVNode = h('div', { domProps: { innerHTML: `Location picture for: ${storage.name}` } })
      const messageVNode = h('div', { domProps: { style: 'text-align: center;' } }, [
        h('img', { domProps: { src: storage.picture_medium } }),
        h('br'),
        h('a', { domProps: { href: storage.picture, innerHTML: 'link to original', target: '_blank' } })
      ])
      this.$bvModal.msgBoxOk([messageVNode], {
        title: [titleVNode],
        buttonSize: 'sm',
        centered: true,
        size: 'lg'
      })
    },
    addAttachment () {
      apiService.partAttachmentCreate(this.part.id, this.addAttachmentForm)
        .then((val) => {
          this.$bvToast.toast(this.$pgettext('PartAttachment/Create/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('PartAttachment/Create/Toast/Success/Title', 'Saving part attachment'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
          this.fetchPart()
          this.addAttachmentForm = { description: '', file: null }
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('PartAttachment/Create/Toast/Error/Message', 'Error occured or file type not allowed.'), {
            title: this.$pgettext('PartAttachment/Create/Toast/Error/Title', 'Saving part attachment'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error with part attachment deletion', err)
        })
    },
    deleteAttachment (attachment) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the attachment '${attachment.description}' ?`, {
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

          apiService.partAttachmentDelete(this.part.id, attachment.id)
            .then((val) => {
              this.$bvToast.toast(this.$pgettext('PartAttachment/Delete/Toast/Success/Message', 'Success'), {
                title: this.$pgettext('PartAttachment/Delete/Toast/Success/Title', 'Deleting part attachment'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'primary',
                toaster: 'b-toaster-top-center'
              })
              this.fetchPart()
            })
            .catch((err) => {
              this.$bvToast.toast(this.$pgettext('PartAttachment/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                title: this.$pgettext('PartAttachment/Delete/Toast/Error/Title', 'Deleting part attachment'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'danger',
                toaster: 'b-toaster-top-center'
              })
              logger.default.error('Error with part attachment deletion', err)
              this.fetchPart()
            })
        })
        .catch((err) => {
          logger.default.error('Error with the delete attachment modal', err)
        })
    }
  }
}
</script>
