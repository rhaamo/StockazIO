<template>
  <div>
    <b-button-group>
      <b-button :size="size"
                :variant="clicked ? 'secondary' : btnVariantMain"
                :disabled="clicked"
                @click.prevent="btnClicked"
      >
        {{ clicked ? btnMainTextDisabled : btnMainText }}
      </b-button>
      <template v-if="clicked">
        <b-button :size="size" :variant="btnVariantOk" @click.prevent="actionConfirmed">
          {{ btnOkText }}
        </b-button>
        <b-button :size="size" :variant="btnVariantCancel" @click.prevent="actionCancelled">
          {{ btnCancelText }}
        </b-button>
      </template>
    </b-button-group>
  </div>
</template>

<script>
export default {
  props: {
    size: {
      type: String,
      default: 'sm'
    },
    btnVariantMain: {
      type: String,
      default: 'danger'
    },
    btnVariantOk: {
      type: String,
      default: 'success'
    },
    btnVariantCancel: {
      type: String,
      default: 'danger'
    },
    btnMainText: {
      type: String,
      default: 'remove item'
    },
    btnMainTextDisabled: {
      type: String,
      default: 'Confirm ?'
    },
    btnOkText: {
      type: String,
      default: 'Yes'
    },
    btnCancelText: {
      type: String,
      default: 'No'
    }
  },
  data: () => ({
    clicked: false
  }),
  computed: {
  },
  methods: {
    btnClicked () {
      this.clicked = true
    },
    actionConfirmed () {
      this.$emit('action-confirmed')
    },
    actionCancelled () {
      this.clicked = false
      this.$emit('action-cancelled')
    }
  }
}
</script>
