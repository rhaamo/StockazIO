<template>
  <div id="app" :key="String($store.state.server.serverUrl)">
    <!-- navigation -->
    <b-navbar type="dark" fixed="top" class="navbar-expand-lg bg-dark p-0 shadow">
      <b-navbar-brand :to="{ name: 'home' }" class="col-sm-3 col-md-2 mr-0">
        StockazIO <small>- {{ backendVersion }}</small>
      </b-navbar-brand>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <template v-if="currentUser">
        <ul class="navbar-nav mr-auto">

          <b-nav-item-dropdown id="editDropdown">
            <template #button-content>
              <i class="fa fa-cogs fa-fw"></i> Edit
            </template>
            <b-dropdown-item :to="{}"><i class="fa fa-paw fa-fw"></i> Footprints</b-dropdown-item>
            <b-dropdown-item :to="{}"><i class="fa fa-home fa-fw"></i> Manufacturers</b-dropdown-item>
            <b-dropdown-item :to="{}"><i class="fa fa-car fa-fw"></i> Distributors</b-dropdown-item>
            <b-dropdown-item :to="{}"><i class="fa fa-archive fa-fw"></i> Storage</b-dropdown-item>
            <b-dropdown-item :to="{}"><i class="fa fa-cogs fa-fw"></i> Parts units</b-dropdown-item>
            <b-dropdown-item :to="{}"><i class="fa fa-cogs fa-fw"></i> Parameters Units</b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item-dropdown id="viewDropdown">
            <template #button-content>
              <i class="fa fa-list fa-fw"></i> View
            </template>
            <b-dropdown-item :to="{name: 'view-infos'}"><i class="fa fa-cogs fa-fw"></i> Informations</b-dropdown-item>
            <b-dropdown-item :to="{}"><i class="fa fa-list-alt fa-fw"></i> Storage tree</b-dropdown-item>
            <b-dropdown-item :to="{}"><i class="fa fa-money fa-fw"></i> Parts to sold</b-dropdown-item>
            <b-dropdown-item :to="{}"><i class="fa fa-list-alt fa-fw"></i> Public parts</b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item :to="{name: 'parts-new'}"><i class="fa fa-plus fa-fw"></i> Add part</b-nav-item>
          <b-nav-item :to="{}"><i class="fa fa-fast-forward fa-fw"></i> Quick add part</b-nav-item>
        </ul>

        <ul class="navbar-nav">
          <b-nav-item-dropdown id="userDropdown">
            <template #button-content>
              <i class="fa fa-user fa-fw"></i> {{ currentUser.username }}
            </template>
            <b-dropdown-item :to="{}"><i class="fa fa-key fa-fw"></i> Change password</b-dropdown-item>
            <b-dropdown-divider/>
            <b-dropdown-item @click.prevent="logout"><i class="fa fa-sign-out fa-fw"></i> Logout</b-dropdown-item>
          </b-nav-item-dropdown>
        </ul>

        <form class="form-inline my-2 my-lg-0" :to="{}" method="GET">
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" id="q" name="q">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
        </template>
        <template v-else>
              <ul class="navbar-nav mr-auto">
                  <li class="nav-item">
                    <a class="nav-link" :to="{}">Login</a>
                  </li>
              </ul>
        </template>
      </div>
    </b-navbar>

    <div v-if="currentUser" class="container-fluid">
        <div class="row">
            <nav v-if='currentUser' class="col-md-2 d-none d-md-block bg-light sidebar">
                <div class="sidebar-sticky">
                    <CategoryTree :tree-data="categories"></CategoryTree>
                </div>
            </nav>

            <div role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
                <router-view />
            </div>
        </div>
    </div>
    <div v-else class="container-fluid">
        <div class="row justify-content-md-center">
            <div role="main" class="col-md-10 col-lg-10 px-4">
                <router-view />
            </div>
        </div>
    </div>
  </div>
</template>

<style lang="scss" src="./App.scss"></style>

<script>
// import initializeSomeStuff from './store/store_init'

import CategoryTree from './components/categories/tree'

export default {
  components: {
    CategoryTree
  },
  data () {
    return {
    }
  },
  computed: {
    backendVersion () { return this.$store.state.server.settings.backendVersion },
    currentUser () { return this.$store.state.user.currentUser && this.$store.state.oauth.loggedIn },
    categories () { return this.$store.state.preloads.categories }
  },
  methods: {
    logout () {
      this.$store.dispatch('user/logout').then(() => {
        this.$router.replace({ name: 'login_form' })
      })
    }
  },
  created () {
    if (this.$store.state.oauth.loggedIn) {
      this.$store.dispatch('preloadStuff')
    }
  }
}
</script>
