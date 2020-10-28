<template>
  <div class="add_part">
    <div class="row">
      <div class="col-lg-9">
        <ol class="breadcrumb">
          <template v-if="category">
            <li class="breadcrumb-item">
              Parts by category
            </li>
            <li class="breadcrumb-item active">
              <router-link :to="{ name: 'parts-category-list', params: { categoryId: category.id, category: category } }">
                {{ category.name }}
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

    <div class="row">
      <div class="col-md-12 mx-auto">
        <table class="table table-condensed table-stripped">
          <thead>
            <tr>
              <th width="25">
                <i class="fa fa-qrcode" />
              </th>
              <th>
                <a href="">Name</a>
                <i
                  v-if="sortBy == 'name'"
                  class="fa fa-sort-alpha-asc"
                  aria-hidden="true"
                />
                <i
                  v-else
                  class="fa fa-sort-alpha-desc"
                  aria-hidden="true"
                />
              </th>
              <th>Storage</th>
              <th>Stock</th>
              <th>Min</th>
              <th>Unit</th>
              <th>Footprint</th>
              <th>
                <i
                  class="fa fa-tasks"
                  aria-hidden="true"
                />
              </th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="part in parts"
              :key="part.id"
            >
              <td>
                <div @click="showBigQrCode(part)">
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
                </div>
              </td>
              <td>
                <a
                  title="View part modal"
                  href=""
                  :data-name="part.name"
                  data-edit-url=""
                  data-delete-url=""
                  data-page-url=""
                  :data-id="part.id"
                  data-toggle="modal"
                  data-target="#modalPart"
                >{{ part.name }}</a>
                <template v-if="part.description">
                  <br>{{ part.description }}
                </template>
              </td>
              <td>{{ part.storage ? part.storage.name : '-' }}</td>
              <td>{{ part.stock_qty }}</td>
              <td>{{ part.stock_qty_min }}</td>
              <td>{{ part.part_unit ? part.part_unit.name : '-' }}</td>
              <td>
                <span
                  v-b-tooltip.hover
                  :title="part.footprint ? part.footprint.description : ''"
                >
                  {{ part.footprint ? part.footprint.name : '-' }}
                </span>
              </td>
              <td>
                <b-button variant="link" @click.prevent="editPart(part)">
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
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '../../services/api/api.service'
import QRCode from 'qrcode'
import logger from '@/logging'

export default {
  props: {
    category: {
      type: Object
    }
  },
  data: () => ({
    parts: [],
    page: 0, // TODO/FIXME no pagination yet
    search_query: '' // TODO/FIXME no search yet
  }),
  computed: {
    categoryId () {
      return this.$route.params.categoryId
    },
    sortBy () {
      return (this.$route.params.sort === 'name' || this.$route.params.sort === '-name') ? 'name' : null
    }
  },
  watch: {
    'categoryId': function () {
      this.fetchParts()
    }
  },
  created () {
    this.fetchParts()
  },
  methods: {
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
    fetchParts () {
      if (this.categoryId) {
        apiService.getPartsByCategory(this.categoryId)
          .then((res) => {
            this.parts = res.data
            console.log('cat', res.data)
          })
      } else {
        apiService.getParts()
          .then((res) => {
            this.parts = res.data
            console.log('no cat', res.data)
          })
      }
    },
    deletePart (part) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the part '${part.name}' ?`, {
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

          apiService.deletePart(part.id)
            .then((val) => {
              this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Success/Message', 'Success'), {
                title: this.$pgettext('Part/Delete/Toast/Success/Title', 'Deleting part'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'primary'
              })
              this.fetchParts()
              console.log(val)
            })
            .catch((err) => {
              this.$bvToast.toast(this.$pgettext('Part/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                title: this.$pgettext('Part/Delete/Toast/Error/Title', 'Deleting part'),
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'danger'
              })
              logger.default.error('Error with part deletion', err)
              this.fetchParts()
            })
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    }
  }
}
</script>
