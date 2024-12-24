<template>
  <div>
    <div class="mt-4 grid align-items-center justify-content-center">
      <Card class="p-2">
        <template #title>Password Reset</template>
        <template #content>
          <form @submit.prevent="submit(!v$.$invalid)" class="text-center">
            <div>
              <div class="field">
                <InputText
                  id="email"
                  v-model="email"
                  :class="{
                    'p-invalid': v$.email.$invalid && submitted,
                  }"
                  placeholder="Enter your email"
                />
                <small v-if="(v$.email.$invalid && submitted) || v$.email.$pending.$response" class="p-error"
                  ><br />
                  {{ v$.email.required.$message }}
                  <template v-if="v$.email.required && v$.email.email"><br /></template>
                  {{ v$.email.email.$message }}
                </small>
              </div>

              <PvButton label="Request reset link" icon="pi pi-user" type="submit"></PvButton>
            </div>
          </form>
        </template>
      </Card>
    </div>
  </div>
</template>

<script>
import { useVuelidate } from "@vuelidate/core";
import { required, email } from "@vuelidate/validators";
import { useOauthStore } from "@/stores/oauth";
import { useUserStore } from "@/stores/user";
import logger from "@/logging";
import { usePreloadsStore } from "@/stores/preloads";
import { useToast } from "primevue/usetoast";
import apiService from "@/services/api/api.service";

export default {
  data: () => ({
    email: null,
    submitted: false,
  }),
  setup: () => ({
    v$: useVuelidate(),
    oauthStore: useOauthStore(),
    userStore: useUserStore(),
    preloadsStore: usePreloadsStore(),
    toast: useToast(),
  }),
  validations: {
    email: { required, email },
  },
  mounted() {},
  methods: {
    submit(isFormValid) {
      this.submitted = true;

      if (!isFormValid) {
        return;
      }

      apiService
        .userPasswordResetRequest({ email: this.email })
        .then(() => {
          this.toast.add({
            severity: "success",
            summary: "Password Reset",
            detail: "If the email exists you will get an email soon",
            life: 5000,
          });
          this.$router.push({ name: "home" });
        })
        .catch((error) => {
          logger.default.error("cannot request new password reset link:", error);
          this.toast.add({
            severity: "error",
            summary: "Password Reset",
            detail: "An error occured, please try again later",
            life: 5000,
          });
        });
    },
  },
};
</script>
