import axios from "axios";
import logger from "@/logging";
import { merge } from "lodash";
import { defineStore } from "pinia";
import apiService from "@/services/api/api.service";

function getDefaultUrl() {
  return (
    window.location.protocol +
    "//" +
    window.location.hostname +
    (window.location.port ? ":" + window.location.port : "") +
    "/"
  );
}

export const useServerStore = defineStore("server", {
  persist: true,
  state: () => ({
    serverUrl: process.env.VUE_APP_SERVER_URL,
    settings: {
      pagination: {},
      partAttachmentAllowedTypes: [],
      backendVersion: "",
      registrationEnabled: false,
    },
    parts_uncategorized_count: 0,
  }),
  getters: {
    defaultUrl() {
      return getDefaultUrl();
    },
  },
  actions: {
    setServerUrl(value) {
      logger.default.info("Setting serverUrl with", value);
      if (value && !value.endsWith("/")) {
        value = value + "/";
      }
      this.serverUrl = value;
      if (!value) {
        axios.defaults.baseURL = null;
        return;
      }
      axios.defaults.baseURL = this.serverUrl;
    },
    setSettings(value) {
      logger.default.info("Merging settings with", value);
      merge(this.settings, value);
      this.settings = {
        ...this.settings,
        ...value,
      };
    },
    parts_uncategorized_count(value) {
      this.parts_uncategorized_count = value;
    },
    fetchSettings() {
      return apiService.getSettings().then(
        (response) => {
          logger.default.info("Successfully fetched server settings");
          let sections = {};
          sections.partAttachmentAllowedTypes =
            response.data.part_attachment_allowed_types;
          sections.pagination = response.data.pagination;
          sections.backendVersion = response.data.version;
          sections.registrationEnabled = false; // TODO
          this.settings = sections;
          this.parts_uncategorized_count =
            response.data.parts_uncategorized_count;
        },
        (response) => {
          logger.default.error("Error while fetching settings", response.data);
        }
      );
    },
  },
});
