<template>
  <div id="app" :key="String($store.state.server.serverUrl)">
    <!-- navigation -->
    <header class="navbar navbar-dark navbar-expand-lg bg-dark p-0 shadow fixed-top">
      <div class="container-fluid">
        <router-link :to="{ name: 'home' }" class="navbar-brand col-sm-3 col-md-2 mr-0">
          StockazIO <small>- {{ backendVersion }}</small>
        </router-link>
        <button
          class="navbar-toggler" type="button" data-toggle="collapse"
          data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon" />
        </button>

        <div id="navbarSupportedContent" class="collapse navbar-collapse">
          <template v-if="currentUser">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item dropdown" id="editDropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <i class="fa fa-cogs fa-fw" /> Edit
                </a>
                <ul class="dropdown-menu">
                  <li><router-link :to="{}" class="dropdown-item"><i class="fa fa-paw fa-fw" /> Footprints</router-link></li>
                  <li><router-link :to="{name: 'manufacturers-list'}" class="dropdown-item"><i class="fa fa-home fa-fw" /> Manufacturers</router-link></li>
                  <li><router-link :to="{name: 'distributors-list'}" class="dropdown-item"><i class="fa fa-car fa-fw" /> Distributors</router-link></li>
                  <li><router-link :to="{name: 'storages-list'}" class="dropdown-item"><i class="fa fa-archive fa-fw" /> Storage</router-link></li>
                  <li><router-link :to="{name: 'part-units-list'}" class="dropdown-item"><i class="fa fa-cogs fa-fw" /> Parts units</router-link></li>
                  <li><router-link :to="{name: 'parameters-units-list'}" class="dropdown-item"><i class="fa fa-cogs fa-fw" /> Parameters Units</router-link></li>
                  <li><router-link :to="{name: 'parameters-presets-list'}" class="dropdown-item"><i class="fa fa-cogs fa-fw" /> Part Parameters Presets</router-link></li>
                  <li><router-link :to="{name: 'label-templates-list'}" class="dropdown-item"><i class="fa fa-cogs fa-fw" /> Label Templates</router-link></li>
                </ul>
              </li>

              <li class="nav-item dropdown" id="viewDropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                <i class="fa fa-list fa-fw" /> View
                </a>
                <ul class="dropdown-menu">
                  <li><router-link :to="{name: 'view-infos'}" class="dropdown-item"><i class="fa fa-cogs fa-fw" /> Informations</router-link></li>
                  <li><router-link :to="{name: 'view-storage-tree'}" class="dropdown-item"><i class="fa fa-list-alt fa-fw" /> Storage tree</router-link></li>
                  <li><router-link :to="{name: 'public-parts'}" class="dropdown-item"><i class="fa fa-list-alt fa-fw" /> Public parts</router-link></li>
                </ul>
              </li>

              <li class="nav-item dropdown" id="toolsDropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                <i class="fa fa-tasks fa-fw" /> Tools
                </a>
                <ul class="dropdown-menu">
                  <li><router-link :to="{name: 'orders-importer'}" class="dropdown-item"><i class="fa fa-shopping-cart fa-fw" /> Orders importer</router-link></li>
                </ul>
              </li>

              <li class="nav-item">
                <router-link :to="{name: 'projects-list'}" class="nav-link"><i class="fa fa-list-ul fa-fw" /> Projects</router-link>
              </li>

              <li class="nav-item ml-4" title="Full form">
                <router-link :to="{name: 'parts-new'}" class="nav-link"><i class="fa fa-plus fa-fw" /> Add part</router-link>
              </li>

              <li class="nav-item" title="Simplified form">
                <router-link :to="{name: 'parts-quick-new'}" class="nav-link"><i class="fa fa-fast-forward fa-fw" /> Quick add part</router-link>
              </li>
            </ul>

            <ul class="navbar-nav d-flex">
              <li class="nav-item dropdown" id="userDropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                <i class="fa fa-user fa-fw" /> {{ currentUsername }}
                </a>
                <ul class="dropdown-menu">
                  <li><router-link :to="{}" class="dropdown-item"><i class="fa fa-key fa-fw" /> Change password</router-link></li>
                  <li><router-link to="#reloadDatas" @click.prevent="forceReloadDatas" class="dropdown-item"><i class="fa fa-refresh" /> Force reload datas</router-link></li>
                  <li><router-link to="#urlHandler" @click.prevent="registerUrlHandler" class="dropdown-item"><i class="fa fa-link" /> Register URL Handler</router-link></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><router-link to="#logout" @click.prevent="logout" class="dropdown-item"><i class="fa fa-sign-out fa-fw" /> Logout</router-link></li>
                </ul>
              </li>
            </ul>

            <form class="d-flex" role="search" @submit="doSearch">
              <input class="form-control me-2" type="search" placeholder="Search"
                aria-label="Search"
                v-model="searchTerm"
              >
              <button class="btn btn-outline-success" type="submit" title="Search">Search</button>
            </form>

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
      </div>
    </header>

    <div v-if="shouldDisplayCategories" class="container-fluid">
      <div class="row">
        <nav v-if="shouldDisplayCategories" class="col-md-3 col-xl-2 d-md-block bg-light sidebar">
          <div class="sidebar-sticky position-sticky pt-3">
            <CategoryTree :tree-data="categories" />
          </div>
        </nav>

        <main role="main" class="col-md-9 ms-sm-auto ml-auto col-xl-10 px-md-4">
          <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <router-view />
          </div>
        </main>
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

import { useToast } from 'vue-toastification'
import ToastyToast from '@/components/toasty-toast'

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
    currentUsername () { return this.$store.state.user.currentUser.username },
    categories () { return this.$store.state.preloads.categories },
    shouldDisplayCategories () {
      if (this.currentUser) { return true }
      if (this.$route.name === 'public-parts' || this.$route.name === 'public-parts-category-list') { return true }
      return false
    }
  },
  created () {
  },
  setup () {
    const toast = useToast()
    return { toast }
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
      if (search.startsWith('stockazio://storageLocation/')) {
        let str = search.split('/')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-list', query: { storage_uuid: uuid } }).catch(() => {})
      } else if (search.startsWith('web+stockazio:storageLocation,')) {
        let str = search.split(',')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-list', query: { storage_uuid: uuid } }).catch(() => {})
      } else if (search.startsWith('stockazio://part/')) {
        let str = search.split('/')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-details', params: { partId: uuid } }).catch(() => {})
      } else if (search.startsWith('web+stockazio:part,')) {
        let str = search.split(',')
        let uuid = str[str.length - 1]
        this.$router.replace({ name: 'parts-details', params: { partId: uuid } }).catch(() => {})
      } else {
        this.$router.replace({ name: 'parts-list', query: { q: search } }).catch(() => {})
      }
    },
    forceReloadDatas () {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to force reload of all datas ?`, {
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
            this.$store.commit('setLastUpdate', { item: 'categories', value: null })
            this.$store.commit('setLastUpdate', { item: 'footprints', value: null })
            this.$store.commit('setLastUpdate', { item: 'storages', value: null })
            this.$store.commit('setLastUpdate', { item: 'parameters_units', value: null })
            this.$store.commit('setLastUpdate', { item: 'part_units', value: null })
            this.$store.commit('setLastUpdate', { item: 'manufacturers', value: null })
            this.$store.commit('setLastUpdate', { item: 'distributors', value: null })
            this.$store.commit('setLastUpdate', { item: 'label_templates', value: null })
            this.$store.commit('setLastUpdate', { item: 'parameters_presets', value: null })
            this.$store.dispatch('preloadStuff').then(() => {
              this.toast.success({
                component: ToastyToast,
                props: {
                  title: this.$pgettext('Datas/Preloading/Toast/Success/Title', 'Reloading datas'),
                  message: this.$pgettext('Datas/Preloading/Toast/Success/Message', 'Success')
                }
              })
            })
          }
        })
    },
    registerUrlHandler () {
      navigator.registerProtocolHandler('web+stockazio', `${window.location.origin}/urlhandler?q=%s`, 'StockazIO handler')
    }
  }
}
</script>

<style lang="scss" src="./App.scss"></style>
