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
          <template #cell(name)="data">
            <p style="white-space: pre-line;">
              <router-link :to="{name: 'projects-details', params: { projectId: data.item.id }}">
                {{ data.item.name }}
              </router-link>
            </p>
          </template>

          <template #cell(description)="data">
            <p style="white-space: pre-line;">
              {{ data.item.description }}
            </p>
          </template>
          <template #cell(state)="data">
            <span>{{ projectStateText(data.item.state) }}</span>
            <div v-if="data.item.state_notes">
              {{ data.item.state_notes }}
            </div>
          </template>
          <template #cell(public)="data">
            <i v-if="data.item.public" class="fa fa-unlock" aria-hidden="true" />
            <i v-else class="fa fa-lock" aria-hidden="true" />
          </template>

          <template #cell(actions)="data">
            <b-button variant="link" :to="{ name: 'projects-edit', params: { projectId: data.item.id } }">
              <i
                class="fa fa-pencil-square-o"
                aria-hidden="true"
              />
            </b-button>
                &nbsp;
            <b-button variant="link" @click.prevent="deleteProject(data.item)">
              <i
                class="fa fa-trash-o"
                aria-hidden="true"
              />
            </b-button>
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
import logger from '@/logging'

export default {
  data: () => ({
    projects: [],
    fields: [
      { key: 'name', label: 'Name', sortable: true, tdClass: 'name' },
      { key: 'description', label: 'Description', tdClass: 'description' },
      { key: 'state', label: 'State', sortable: true, tdClass: 'state' },
      { key: 'public', label: 'Visibility', sortable: true, tdClass: 'visibility' },
      { key: 'actions', label: 'Actions', tdClass: 'actions' }
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
    },
    deleteProject (project) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to delete the project '${project.name}' ?`, {
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
            apiService.deleteProject(project.id)
              .then((val) => {
                this.$bvToast.toast(this.$pgettext('Project/Delete/Toast/Success/Message', 'Success'), {
                  title: this.$pgettext('Project/Delete/Toast/Success/Title', 'Deleting project'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'primary',
                  toaster: 'b-toaster-top-center'
                })
                this.fetchProjects(this.currentPage, null)
              })
              .catch((err) => {
                this.$bvToast.toast(this.$pgettext('Project/Delete/Toast/Error/Message', 'An error occured, please try again later'), {
                  title: this.$pgettext('Project/Delete/Toast/Error/Title', 'Deleting project'),
                  autoHideDelay: 5000,
                  appendToast: true,
                  variant: 'danger',
                  toaster: 'b-toaster-top-center'
                })
                logger.default.error('Error with project deletion', err)
                this.fetchParts(1, null)
              })
          }
        })
        .catch((err) => {
          logger.default.error('Error with the delete modal', err)
        })
    }
  }
}
</script>

<style>
table#tableProjectsList td.name {
  width: 25em;
}

table#tableProjectsList td.description {
}

table#tableProjectsList td.state {
  width: 15em;
}

table#tableProjectsList td.visibility {
  width: 7em;
}

table#tableProjectsList td.actions {
  width: 7em;
}
</style>
