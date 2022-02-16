<template>
  <div id="app" :key="String($store.state.server.serverUrl)">
    <!-- navigation -->
    <b-navbar type="dark" fixed="top" class="navbar-expand-lg bg-dark p-0 shadow">
      <b-navbar-brand :to="{ name: 'home' }" class="col-sm-3 col-md-2 mr-0">
        StockazIO <small>- {{ backendVersion }}</small>
      </b-navbar-brand>
      <button
        class="navbar-toggler" type="button" data-toggle="collapse"
        data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon" />
      </button>

      <div id="navbarSupportedContent" class="collapse navbar-collapse">
        <template v-if="currentUser">
          <ul class="navbar-nav mr-auto">
            <b-nav-item-dropdown id="editDropdown">
              <template #button-content>
                <i class="fa fa-cogs fa-fw" /> Edit
              </template>
              <b-dropdown-item :to="{}">
                <i class="fa fa-paw fa-fw" /> Footprints
              </b-dropdown-item>
              <b-dropdown-item :to="{name: 'manufacturers-list'}">
                <i class="fa fa-home fa-fw" /> Manufacturers
              </b-dropdown-item>
              <b-dropdown-item :to="{name: 'distributors-list'}">
                <i class="fa fa-car fa-fw" /> Distributors
              </b-dropdown-item>
              <b-dropdown-item :to="{name: 'storages-list'}">
                <i class="fa fa-archive fa-fw" /> Storage
              </b-dropdown-item>
              <b-dropdown-item :to="{ name: 'part-units-list' }">
                <i class="fa fa-cogs fa-fw" /> Parts units
              </b-dropdown-item>
              <b-dropdown-item :to="{ name: 'parameters-units-list' }">
                <i class="fa fa-cogs fa-fw" /> Parameters Units
              </b-dropdown-item>
              <b-dropdown-item :to="{ name: 'parameters-presets-list' }">
                <i class="fa fa-cogs fa-fw" /> Part Parameters Presets
              </b-dropdown-item>
              <b-dropdown-item :to="{ name: 'label-templates-list' }">
                <i class="fa fa-cogs fa-fw" /> Label Templates
              </b-dropdown-item>
            </b-nav-item-dropdown>

            <b-nav-item-dropdown id="viewDropdown">
              <template #button-content>
                <i class="fa fa-list fa-fw" /> View
              </template>
              <b-dropdown-item :to="{name: 'view-infos'}">
                <i class="fa fa-cogs fa-fw" /> Informations
              </b-dropdown-item>
              <b-dropdown-item :to="{name: 'view-storage-tree'}">
                <i class="fa fa-list-alt fa-fw" /> Storage tree
              </b-dropdown-item>
              <b-dropdown-item :to="{name: 'public-parts'}">
                <i class="fa fa-list-alt fa-fw" /> Public parts
              </b-dropdown-item>
            </b-nav-item-dropdown>

            <b-nav-item-dropdown id="manageDropdown">
              <template #button-content>
                <i class="fa fa-tasks fa-fw" /> Tools
              </template>
              <b-dropdown-item :to="{name: 'orders-importer'}">
                <i class="fa fa-shopping-cart fa-fw" /> Orders importer
              </b-dropdown-item>
            </b-nav-item-dropdown>

            <b-nav-item :to="{name: 'projects-list'}">
              <i class="fa fa-list-ul fa-fw" /> Projects
            </b-nav-item>
            <b-nav-item :to="{name: 'parts-new'}" class="ml-4" title="Full form">
              <i class="fa fa-plus fa-fw" /> Add part
            </b-nav-item>
            <b-nav-item :to="{name: 'parts-quick-new'}" title="Simplified form">
              <i class="fa fa-fast-forward fa-fw" /> Quick add part
            </b-nav-item>
          </ul>

          <ul class="navbar-nav">
            <b-nav-item-dropdown id="userDropdown">
              <template #button-content>
                <i class="fa fa-user fa-fw" /> {{ currentUser.username }}
              </template>
              <b-dropdown-item :to="{}">
                <i class="fa fa-key fa-fw" /> Change password
              </b-dropdown-item>
              <b-dropdown-divider />
              <b-dropdown-item @click.prevent="logout">
                <i class="fa fa-sign-out fa-fw" /> Logout
              </b-dropdown-item>
            </b-nav-item-dropdown>
          </ul>

          <b-form @submit="doSearch">
            <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
              <b-input id="inline-form-input-search" v-model="searchTerm" placeholder="Search" />
              <b-input-group-append>
                <b-button type="submit" title="Search">
                  Search
                </b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form>
        </template>
        <template v-else>
          <b-navbar-nav class="mr-auto">
            <b-nav-item :to="{name: 'login_form'}">
              Login
            </b-nav-item>
            <b-nav-item :to="{name: 'public-parts'}">
              Public parts list
            </b-nav-item>
            <b-nav-item :to="{name: 'about'}">
              About
            </b-nav-item>
          </b-navbar-nav>
        </template>
      </div>
    </b-navbar>

    <div v-if="shouldDisplayCategories" class="container-fluid">
      <div class="row">
        <nav v-if="shouldDisplayCategories" class="col-md-3 col-xl-2 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <CategoryTree :tree-data="categories" />
          </div>
        </nav>

        <div role="main" class="col-md-9 ml-auto col-xl-10">
          <router-view />
        </div>
      </div>
    </div>
    <div v-else class="container-fluid">
      <div class="row justify-content-md-center">
        <div role="main" class="col-md-10 col-lg-10">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import initializeSomeStuff from './store/store_init'

import CategoryTree from './components/categories/tree'

export default {
  components: {
    CategoryTree
  },
  data () {
    return {
      searchTerm: ''
    }
  },
  computed: {
    backendVersion () { return this.$store.state.server.settings.backendVersion },
    currentUser () { return this.$store.state.user.currentUser && this.$store.state.oauth.loggedIn },
    categories () { return this.$store.state.preloads.categories },
    shouldDisplayCategories () {
      if (this.currentUser) { return true }
      if (this.$route.name === 'public-parts' || this.$route.name === 'public-parts-category-list') { return true }
      return false
    }
  },
  created () {
  },
  methods: {
    logout () {
      this.$store.dispatch('user/logout').then(() => {
        this.$router.replace({ name: 'login_form' })
      })
    },
    doSearch (event) {
      event.preventDefault()
      let search = this.searchTerm
      this.searchTerm = ''
      if (search.startsWith('stockazio://storageLocation/') || search.startsWith('web+stockazio:storageLocation,')) {
        let str = search.split('/')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-list', query: { storage_uuid: uuid } }).catch(() => {})
      } else if (search.startsWith('stockazio://part/') || search.startsWith('web+stockazio:part,')) {
        let str = search.split('/')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-details', params: { partId: uuid } }).catch(() => {})
      } else {
        this.$router.replace({ name: 'parts-list', query: { q: search } }).catch(() => {})
      }
    }
  }
}
</script>

<style lang="scss" src="./App.scss"></style>
