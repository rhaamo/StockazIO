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
        <b-col cols="2" xl="1">
          <b-button type="submit" variant="primary">
            update
          </b-button>
        </b-col>
        <b-col cols="9" xl="8">
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
                  <div v-if="!$v.matchers.$each[i].regexp.required" class="invalid-feedback d-block">
                    Regexp string is required
                  </div>
                  <div v-if="!$v.matchers.$each[i].regexp.maxLength" class="invalid-feedback d-block">
                    Maximum length is 255
                  </div>
                </b-form-group>
              </b-col>

              <b-col>
                <b-form-group :id="pmId('category', i)" label="Category*" :label-for="pmId('category', i)">
                  <vue-treeselect
                    :id="pmId('category', i)" v-model="matchers[i].category" :multiple="false"
                    :options="choicesCategory" search-nested :default-expand-level="Infinity"
                    clearable :normalizer="categoriesNormalizer" no-children-text
                    placeholder="Film resistors ? MCUS ?"
                  />
                  <div v-if="!$v.matchers.$each[i].category.required" class="invalid-feedback d-block">
                    Category is required
                  </div>
                  <div v-if="!$v.matchers.$each[i].category.integer" class="invalid-feedback d-block">
                    Category is invalid
                  </div>
                </b-form-group>
              </b-col>
              <b-col cols="2">
                <div class="pt-2">
                  <br>
                  <BtnDeleteInline
                    size="sm" btn-variant-main="danger" btn-variant-ok="success"
                    btn-variant-cancel="danger" btn-main-text="remove"
                    btn-main-text-disabled="Confirm ?" btn-ok-text="Yes"
                    btn-cancel-text="No" @action-confirmed="deletePm(i)"
                  />
                </div>
              </b-col>
            </b-row>
            <hr>
          </div>
          <b-button size="sm" variant="info" @click.prevent="addPm">
            add matcher
          </b-button>
        </b-col>
      </b-row>
    </b-form>
  </div>
</template>

<script>
import BtnDeleteInline from '@/components/btn_delete_inline'
import apiService from '@/services/api/api.service'
import logger from '@/logging'
import { mapState } from 'vuex'
import { validationMixin } from 'vuelidate'
import { required, maxLength, integer } from 'vuelidate/lib/validators'

import dateFnsFormat from 'date-fns/format'
import dateFnsParseISO from 'date-fns/parseISO'

export default {
  components: {
    BtnDeleteInline
  },
  mixins: [
    validationMixin
  ],
  props: {
  },
  data: () => ({
    matchers: [],
    deleted: []
  }),
  validations: {
    matchers: {
      $each: {
        regexp: {
          required,
          maxLength: maxLength(255)
        },
        category: { required, integer: integer }
      }
    }
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
      return date ? dateFnsFormat(dateFnsParseISO(date), 'E d MMM yyyy') : ''
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
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Error getting categories matcher', err)
        })
    },
    categoriesNormalizer: function (node) {
      return { id: node.id, label: node.name, children: node.children && node.children.length ? node.children : 0 }
    },
    updateMatchers () {
      this.$v.$touch()
      if (this.$v.$invalid) {
        logger.default.error('Form has errors')
        return
      }

      apiService.updateCategoryMatchers({ update: this.matchers, delete: this.deleted })
        .then(() => {
          this.$bvToast.toast(this.$pgettext('CategoryMatchers/Add/Toast/Success/Message', 'Success'), {
            title: this.$pgettext('CategoryMatchers/Add/Toast/Success/Title', 'Updating matchers'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'primary',
            toaster: 'b-toaster-top-center'
          })
        })
        .catch((error) => {
          this.$bvToast.toast(this.$pgettext('CategoryMatchers/Add/Toast/Error/Message', 'An error occured, please try again later'), {
            title: this.$pgettext('CategoryMatchers/Add/Toast/Error/Title', 'Updating matchers'),
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'danger',
            toaster: 'b-toaster-top-center'
          })
          logger.default.error('Cannot update matchers', error.message)
        })
    },
    pmId (func, idx, suffix) {
      return `input-pm-${func}-${idx}${suffix ? `-${suffix}` : ''}`
    },
    addPm () {
      this.matchers.push({
        regexp: '',
        category: null
      })
    },
    deletePm (idx) {
      if (this.matchers[idx].id) {
        // mark it as deletion
        this.deleted.push(this.matchers[idx].id)
      }
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
<style src="@bosquig/vue3-treeselect/dist/vue3-treeselect.css"></style>
