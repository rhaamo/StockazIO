<template>
  <div class="projects_list">
    <div class="row">
      <div class="col-8">
        <ol class="breadcrumb">
          <li class="breadcrumb-item active">
            <router-link :to="{ name: 'projects-list' }">
              Projects
            </router-link>
          </li>
        </ol>
      </div>

      <div class="col-xl-1 col-2">
        <b-btn :to="{name: 'projects-new'}">
          New
        </b-btn>
      </div>

      <div class="col-xl-2 col-3">
        <b-form-select v-model="filter.state" :options="projectStates" />
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 mx-auto">
        <b-table id="tableProjectsList" ref="tableProjectsList" :items="projects"
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
          <template #cell(description)="data">
            <p style="white-space: pre-line;">
              {{ data.item.description }}
            </p>
          </template>
          <template #cell(state)="data">
            <span>{{ projectStateText(data.item.state) }}</span>
          </template>
          <template #cell(public)="data">
            <i v-if="data.item.public" class="fa fa-unlock" aria-hidden="true" />
            <i v-else class="fa fa-lock" aria-hidden="true" />
          </template>
        </b-table>
      </div>
    </div>

    <b-row>
      <b-col md="6" offset-md="1">
        <b-pagination
          v-model="currentPage"
          :total-rows="projectsCount"
          :per-page="perPage"
          aria-controls="tablePartsList"
          @change="pageChanged"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import apiService from '@/services/api/api.service'

export default {
  data: () => ({
    projects: [],
    fields: [
      { key: 'name', label: 'Name', sortable: true },
      { key: 'description', label: 'Description' },
      { key: 'state', label: 'State', sortable: true, tdClass: 'state' },
      { key: 'public', label: 'Public', sortable: true, tdClass: 'public' }
    ],
    sortBy: 'name',
    sortDesc: false,
    currentPage: 1,
    projectsCount: 0,
    filter: {
      state: null
    },
    projectStates: [
      { value: 1, text: 'Planned' },
      { value: 2, text: 'Ongoing' },
      { value: 3, text: 'Finished' },
      { value: 4, text: 'Waiting' },
      { value: 5, text: 'Abandonned' },
      { value: 99, text: 'Unknown' },
      { value: null, text: 'Filter by state' }
    ]
  }),
  computed: {
    perPage () {
      return 20
    }
  },
  watch: {
    'filter.state': function () {
      this.fetchProjects(1, null)
    }
  },
  created () {
    this.$nextTick(() => {
      this.fetchProjects(1, null)
    })
  },
  methods: {
    fetchProjects (page, opts) {
      let params = {
        page: page,
        size: this.perPage,
        ...opts
      }
      if (this.filter.state) {
        params.state = this.filter.state
      }
      apiService.getProjects(params)
        .then((res) => {
          this.projects = res.data.results
          this.projectsCount = res.data.count
          // eslint-disable-next-line vue/custom-event-name-casing
          this.$root.$emit('bv::refresh::table', 'tableProjectsList')
        })
    },
    sortTableChanged (ctx) {
      // When changing the sorting order, reset the pagination to page 1
      let opts = ctx.sortDesc ? `-${ctx.sortBy}` : ctx.sortBy
      this.fetchProjects(1, opts)
    },
    pageChanged (page) {
      this.fetchProjects(page, null)
    },
    projectStateText (value) {
      let a = this.projectStates.filter(function (e) { return e.value === value })
      return a && a.length ? a[0].text : 'Error'
    }
  }
}
</script>

<style>
table#tableProjectsList td.state {
  width: 8em;
}

table#tableProjectsList td.public {
  width: 5em;
}
</style>
