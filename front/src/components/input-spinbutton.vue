<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-7">
          <div class="input-group">
            <button class="btn btn-outline-secondary form-control-sm" type="button" id="decrement"
              @click.prevent="decrement"
            >-</button>
            <input type="text" class="form-control form-control-sm" placeholder=""
              :value="count"
            >
            <button class="btn btn-outline-secondary form-control-sm" type="button" id="increment"
              @click.prevent="increment"
            >+</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  // https://github.com/cdmoro/bootstrap-vue-3/issues/396
  export default {
    props: {
      initial: Number,
      min: Number
    },
    data: () => ({
      count: null
    }),
    mounted () {
      this.count = this.initial
    },
    methods: {
      increment () {
        this.count = this.count + 1
        this.$emit('update:initial', this.count)
      },
      decrement () {
        if (this.count - 1 > this.min) {
          this.count = this.count - 1
        }
        this.$emit('update:initial', this.count)
      }
    }
  }
</script>