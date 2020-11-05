<template>
  <div class="list_part_unit">
    <b-row>
      <b-col md="9">
        <b-breadcrumb>
          <b-breadcrumb-item :to="{name: 'orders-importer'}">
            Orders Importer
          </b-breadcrumb-item>
          <b-breadcrumb-item :to="{name: 'orders-importer-category-matcher'}">
            Category Matchers
          </b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
    </b-row>

    <b-form @submit.prevent="updateMatchers">
      <b-row>
        <b-col md="1">
          <b-button type="submit" variant="primary">
            update
          </b-button>
        </b-col>
        <b-col md="8">
          <div v-for="(_, i) in matchers" :key="i">
            <b-row>
              <b-col md="7">
                <b-form-group :id="pmId('regexp', i)" label="Regexp compatible string*" :label-for="pmId('regexp', i)">
                  <b-input-group prepend="/" append="/i">
                    <b-form-input
                      :id="pmId('regexp', i)"
                      v-model="matchers[i].regexp"
                      required
                    />
                  </b-input-group>
                </b-form-group>
              </b-col>

              <b-col>
                <b-form-group :id="pmId('category', i)" label="Category*" :label-for="pmId('category', i)">
                  <treeselect :id="pmId('category', i)" v-model="matchers[i].category" :multiple="false"
                              :options="choicesCategory" search-nested :default-expand-level="Infinity"
                              clearable :normalizer="categoriesNormalizer" no-children-text
                              placeholder="Film resistors ? MCUS ?"
                  />
                </b-form-group>
                </b-form-group>
              </b-col>
              <b-col md="1">
                <br><br>
                <div @click.prevent="deletePm(i)">
                  <i class="fa fa-minus-square" aria-hidden="true" /> remove
                </div>
              </b-col>
            </b-row>
            <hr>
          </div>
          <div @click.prevent="addPm">
            <i class="fa fa-plus-square" aria-hidden="true" /> add matcher
          </div>
        </b-col>
      </b-row>
    </b-form>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'
import logger from '@/logging'
import { mapState } from 'vuex'

import moment from 'moment'

export default {
  mixins: [
  ],
  props: {
  },
  data: () => ({
    matchers: []
  }),
  validations: {
  },
  computed: {
    ...mapState({
      serverSettings: state => state.server.settings,
      choicesCategory: state => { return [state.preloads.categories] }
    })
  },
  watch: {
  },
  created () {
    this.fetchMatchers()
  },
  methods: {
    ignoreIdCbox (id) {
      return `ignore-${id}`
    },
    formatDate (date) {
      return moment(date).format('ddd DD MMM YYYY')
    },
    fetchMatchers (orderId) {
      apiService.getCategoryMatchers()
        .then((val) => {
          this.matchers = val.data.map(x => {
            return {
              id: x.id,
              regexp: x.regexp,
              category: x.category ? x.category.id : null
            }
          })
        })
        .catch((err) => {
          this.$bvToast.toast(this.$pgettext('CategoryMatchers/Fetch/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('CategoryMatchers/Fetch/Toast/Error/Title', 'Fetching categories matchers'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Error getting categories matcher', err)
        })
    },
    categoriesNormalizer: function (node) {
      return { id: node.id, label: node.name, children: node.children && node.children.length ? node.children : 0 }
    },
    updateMatchers () {
      apiService.updateCategoryMatchers(this.matchers)
        .then(() => {
          this.$bvToast.toast(this.$pgettext('CategoryMatchers/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('CategoryMatchers/Add/Toast/Success/Title', 'Updating matchers'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary'
          })
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('CategoryMatchers/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('CategoryMatchers/Add/Toast/Error/Title', 'Updating matchers'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger'
          })
          logger.default.error('Cannot update matchers', error.message)
        })
    },
    pmId (func, idx) {
      return `input-pm-${func}-${idx}`
    },
    addPm () {
      this.matchers.push({
        regexp: '',
        category: null
      })
    },
    deletePm (idx) {
      this.$delete(this.matchers, idx)
    }
  }
}
</script>

<style>
table#tableOrderItems td.category {
  width: 20em;
}
</style>
<style src="@riophae/vue-treeselect/dist/vue-treeselect.css"></style>
