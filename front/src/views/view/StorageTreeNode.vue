<template>
  <li>
    <router-link v-if="node.uuid" :to="{ name: 'parts-list', query: { storage: node.id } }">
      {{ node.name }}
    </router-link>
    <template v-else>
      {{ node.name }}
    </template>
    <template v-if="node.uuid">
      &nbsp;<i
              v-b-tooltip.hover class="fa fa-barcode" aria-hidden="true"
              title="Show QrCode" @click="showBigQrCode(node)"
            />
      <template v-if="node.picture">
      &nbsp;
        <i
          v-b-tooltip.hover class="fa fa-picture-o" title="Show location picture"
          aria-hidden="true" @click="showLocationPicture(node)"
        />
      </template>
    </template>

    <ul v-if="node.children && node.children.length" class="children">
      <node v-for="child in node.children" :key="child.id" :node="child" />
    </ul>

    <ul v-if="node.storage_locations && node.storage_locations.length" class="storage_locations">
      <node v-for="child in node.storage_locations" :key="child.id" :node="child" />
    </ul>
  </li>
</template>

<script>
import QRCode from 'qrcode'

export default {
  name: 'StorageTreeNode',
  props: {
    'node': Object
  },
  methods: {
    qrCodeStorage (uuid) {
      return `stockazio://storageLocation/${uuid}`
    },
    async showBigQrCode (storage) {
      let qrCodeDataUrl = await QRCode.toDataURL(this.qrCodeStorage(storage.uuid), { width: 300 }).then((url) => { return url })

      const h = this.$createElement
      const titleVNode = h('div', { domProps: { innerHTML: `QrCode for: ${storage.name}` } })
      const messageVNode = h('div', { domProps: { style: 'text-align: center;' } }, [
        h('img', { domProps: { src: qrCodeDataUrl } }),
        h('div', {}, ['The content of the QrCode is:', h('br'), h('code', { class: ['qrCodeText'] }, [this.qrCodeStorage(storage.uuid)])])
      ])
      this.$bvModal.msgBoxOk([messageVNode], {
        title: [titleVNode],
        buttonSize: 'sm',
        centered: true,
        size: 'lg'
      })
    },
    showLocationPicture (storage) {
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
    }
  }
}
</script>
