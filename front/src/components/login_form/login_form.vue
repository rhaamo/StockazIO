<template>
  <div>
    <div class="row justify-content-md-center">
      <div class="col-md-3">
        <b-form class="login" @submit.prevent="submitPassword">
          <h1 v-translate>
            Sign in
          </h1>
          <b-form-group
            id="ig-username"
            :label="labels.usernameLabel"
            label-for="username"
          >
            <b-form-input
              id="username"
              v-model="user.username"
              type="text"
              :placeholder="labels.usernamePlaceholder"
              :state="$v.user.username.$dirty ? !$v.user.username.$error : null"
              aria-describedby="login-live-feedback"
            />
            <b-form-invalid-feedback id="login-live-feedback">
              <translate translate-context="Content/Login/Feedback/Username/Required">
                Please enter your login
              </translate>
            </b-form-invalid-feedback>
          </b-form-group>

          <b-form-group
            id="ig-password"
            :label="labels.passwordLabel"
            label-for="password"
          >
            <b-form-input
              id="password"
              v-model="user.password"
              type="password"
              :placeholder="labels.passwordPlaceholder"
              :state="$v.user.password.$dirty ? !$v.user.password.$error : null"
              aria-describedby="password-live-feedback"
            />
            <b-form-invalid-feedback id="password-live-feedback">
              <translate translate-context="Content/Login/Feedback/Password/Required">
                Please enter your password
              </translate>
            </b-form-invalid-feedback>
          </b-form-group>

          <b-button type="submit" variant="primary">
            <translate translate-context="Content/Login/Button/Login">
              Login
            </translate>
          </b-button>
          <router-link :to="{name: 'password-reset'}">
            <translate translate-context="Content/Login/Link/Reset password">
              Reset password
            </translate>
          </router-link>
        </b-form>

        <br>
        <b-alert v-if="error" variant="danger" show>
          {{ error }}
        </b-alert>
      </div>
    </div>
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, maxLength } from 'vuelidate/lib/validators'
import { mapState } from 'vuex'

export default {
  mixins: [validationMixin],
  data: () => ({
    user: {},
    error: false
  }),
  validations: {
    user: {
      username: { required, maxLength: maxLength(250) },
      password: { required, maxLength: maxLength(250) }
    }
  },
  computed: {
    ...mapState({
      registrationEnabled: state => state.server.settings.registrationEnabled
    }),
    labels () {
      return {
        usernameLabel: this.$pgettext('Content/Login/Input.Label/Username', 'Username:'),
        usernamePlaceholder: this.$pgettext('Content/Login/Input.Placeholder/Username', 'Enter username'),
        passwordLabel: this.$pgettext('Content/Login/Input.Label/Password', 'Password:'),
        passwordPlaceholder: this.$pgettext('Content/Login/Input.Placeholder/Password', 'Enter password')
      }
    },
    accountIsConfirmed () { return 'account_confirmed' in this.$route.query }
  },
  methods: {
    submitPassword: function () {
      this.$v.$touch()

      if (this.$v.$invalid) {
        return false
      }

      // do some OAuth2 magic here
    },
    clearError () {
      this.error = false
    },
    focusOnPasswordInput () {
      let passwordInput = this.$refs.passwordInput
      passwordInput.focus()
      passwordInput.setSelectionRange(0, passwordInput.value.length)
    }
  }
}
</script>
