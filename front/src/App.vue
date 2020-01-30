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

          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="fa fa-cogs fa-fw"></i> Edit
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" :to="{}"><i class="fa fa-paw fa-fw"></i> Footprints</a>
              <a class="dropdown-item" :to="{}"><i class="fa fa-home fa-fw"></i> Manufacturers</a>
              <a class="dropdown-item" :to="{}"><i class="fa fa-car fa-fw"></i> Distributors</a>
              <a class="dropdown-item" :to="{}"><i class="fa fa-archive fa-fw"></i> Storage</a>
              <a class="dropdown-item" :to="{}"><i class="fa fa-cogs fa-fw"></i> Parts units</a>
              <a class="dropdown-item" :to="{}"><i class="fa fa-cogs fa-fw"></i> Parameters Units</a>
            </div>
          </li>

          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="fa fa-list fa-fw"></i> View
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" :to="{}"><i class="fa fa-cogs fa-fw"></i> Informations</a>
              <a class="dropdown-item" :to="{}"><i class="fa fa-list-alt fa-fw"></i> Storage tree</a>
              <a class="dropdown-item" :to="{}"><i class="fa fa-money fa-fw"></i> Parts to sold</a>
              <a class="dropdown-item" :to="{}"><i class="fa fa-list-alt fa-fw"></i> Public parts</a>
            </div>
          </li>

          <li class="nav-item">
            <a class="nav-link" :to="{}"><i class="fa fa-plus fa-fw"></i> Add part</a>
          </li>

          <li class="nav-item">
            <a class="nav-link" :to="{}"><i class="fa fa-fast-forward fa-fw"></i> Quick add part</a>
          </li>
        </ul>

        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="fa fa-user fa-fw"></i> { currentUser.username }
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <a class="dropdown-item" :to="{}"><i class="fa fa-key fa-fw"></i> Change password</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" :to="{}"><i class="fa fa-sign-out fa-fw"></i> Logout</a>
            </div>
          </li>
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

    <div class="container-fluid">
        <div class="row">
            <nav v-if='currentUser' class="col-md-2 d-none d-md-block bg-light sidebar">
                <div class="sidebar-sticky">
                    todo nav
                </div>
            </nav>

            <div role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
                <router-view />
            </div>
        </div>
    </div>
  </div>
</template>

<style lang="scss" src="./App.scss"></style>

<script>
import initializeSomeStuff from './store/store_init'

export default {
  computed: {
    backendVersion () { return this.$store.state.server.settings.backendVersion },
    currentUser () { return this.$store.state.user.currentUser }
  },
  async created () {
    if (!this.$store.state.server.serverUrl) {
      // we have several way to guess the API server url. By order of precedence:
      // 1. use the url specified when building via VUE_APP_SERVER_URL
      // 2. use the current url
      let defaultServerUrl = process.env.VUE_APP_SERVER_URL || this.$store.getters['server/defaultUrl']()
      this.$store.commit('server/serverUrl', defaultServerUrl)
    } else {
      // needed to trigger initialization of axios / service worker
      this.$store.commit('server/serverUrl', this.$store.state.server.serverUrl)
    }
    // Fetch server settings
    this.$store.dispatch('server/fetchSettings').finally(() => {
    // Start oauth init
      let store = this.$store
      initializeSomeStuff({ store })
    })
  }
}
</script>
