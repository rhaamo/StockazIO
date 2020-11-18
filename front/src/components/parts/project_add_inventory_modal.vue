<template>
  <b-modal id="modalAddInventoryPart" ref="modalAddInventoryPart"
           size="xl" @cancel="partModalClose" @close="partModalClose"
           @hidden="partModalClose"
  >
    <template #modal-header="{ close }">
      <h5 id="modalPartTitle">
        Select part
      </h5>
      <button type="button" class="close" data-dismiss="modal"
              aria-label="Close" @click="close()"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </template>
    <div class="container">
      <div class="row">
        aaa
      </div>
    </div>
    <template #modal-footer="{ cancel }">
      <b-button size="sm" variant="success" @click="cancel">
        Close
      </b-button>
    </template>
  </b-modal>
</template>

<script>
export default {
  props: {
    part: {
      type: Object
    }
  },
  computed: {
  },
  methods: {
    partModalClose () {
      this.$bvModal.hide('modalManage')
      this.$emit('add-part-modal-closed')
    }
  }
}
</script>
