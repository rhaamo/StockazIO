import { defineStore } from "pinia";
import logger from "@/logging";
import apiService from "@/services/api/api.service";
import { differenceInMinutes, parseISO } from "date-fns";

// Equivalent to one day
const REFRESH_TIME = 1440;

export const usePreloadsStore = defineStore("preloads", {
  persist: true,
  state: () => {
    return {
      categories: {},
      footprints: [],
      storages: [],
      parameters_unit: [],
      part_units: [],
      manufacturers: [],
      distributors: [],
      label_templates: [],
      currentCategory: {
        id: null,
      },
      partParametersPresets: [],
      // Contain last (initial=null) date of fetch for each set of preload
      lastUpdate: {
        categories: null,
        footprints: null,
        storages: null,
        parameters_units: null,
        part_units: null,
        manufacturers: null,
        distributors: null,
        label_templates: null,
        parameters_presets: null,
      },
    };
  },
  // could also be defined as
  // state: () => ({ count: 0 })
  actions: {
    setCategories(value) {
      this.categories = value;
    },
    setFootprints(value) {
      this.footprints = value;
    },
    setStorages(value) {
      this.storages = value;
    },
    setParametersUnits(value) {
      this.parameters_unit = value;
    },
    setPartUnits(value) {
      this.part_units = value;
    },
    setManufacturers(value) {
      this.manufacturers = value;
    },
    setDistributors(value) {
      this.distributors = value;
    },
    setLabelTemplates(value) {
      this.label_templates = value;
    },
    setCurrentCategory(value) {
      this.currentCategory = value;
    },
    setPartParametersPresets(value) {
      this.partParametersPresets = value;
    },
    setLastUpdate(category, date) {
      if (category && date) {
        // Cannot save a Date() object in LocalStorage, so convert it to ISO String
        this.lastUpdate[category] = date.toISOString();
      } else {
        // When nulled to force reload
        this.lastUpdate[category] = date;
      }
    },
    incrementCategoryPartsCount(nodeId, by = 1) {
      function incrementNode(node, nodeId) {
        if (node.id === nodeId) {
          node.parts_count += by;
        } else if (node.children && node.children.length) {
          for (let i = 0; i < node.children.length; i++) {
            incrementNode(node.children[i], nodeId);
          }
        }
      }
      if (nodeId !== null) {
        if (typeof nodeId === "string") {
          nodeId = parseInt(nodeId);
        }
        incrementNode(this.categories, nodeId);
      }
    },
    decrementCategoryPartsCount(nodeId, by = 1) {
      function decrementNode(node, nodeId) {
        if (node.id === nodeId) {
          node.parts_count -= by;
        } else if (node.children && node.children.length) {
          for (let i = 0; i < node.children.length; i++) {
            decrementNode(node.children[i], nodeId);
          }
        }
      }
      if (nodeId !== null) {
        if (typeof nodeId === "string") {
          nodeId = parseInt(nodeId);
        }
        decrementNode(this.categories, nodeId);
      }
    },
    // Doesn't really works when called, async fucked
    async preloadStuff() {
      await this.preloadSidebar;
      await this.preloadFootprints;
      await this.preloadStorages;
      await this.preloadParametersUnits;
      await this.preloadPartUnits;
      await this.preloadManufacturers;
      await this.preloadDistributors;
      await this.preloadLabelTemplates;
      await this.preloadPartParametersPresets;
      return;
    },
    preloadSidebar() {
      // Preload sidebar
      let dateRefreshed = this.lastUpdate.categories;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Categories do not need reload");
        return;
      }
      return apiService
        .getCategories()
        .then((data) => {
          this.setCategories(data.data[0]);
          this.setLastUpdate("categories", new Date());
          logger.default.info("Categories preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload categories", error.message);
        });
    },
    preloadFootprints() {
      // Preload footprints
      let dateRefreshed = this.lastUpdate.footprints;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Footprints do not need reload");
        return;
      }
      return apiService
        .getFootprints()
        .then((data) => {
          this.setFootprints(data.data);
          this.setLastUpdate("footprints", new Date());
          logger.default.info("Footprints preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload footprints", error.message);
        });
    },
    preloadStorages() {
      // Preload storages
      let dateRefreshed = this.lastUpdate.storages;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Storages do not need reload");
        return;
      }
      return apiService
        .getStorages()
        .then((data) => {
          this.setStorages(data.data);
          this.setLastUpdate("storages", new Date());
          logger.default.info("Storages preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload storages", error.message);
        });
    },
    preloadParametersUnits() {
      // Preload units
      let dateRefreshed = this.lastUpdate.parameters_units;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Parameters Units do not need reload");
        return;
      }
      return apiService
        .getParametersUnits()
        .then((data) => {
          this.setParametersUnits(data.data);
          this.setLastUpdate("parameters_units", new Date());
          logger.default.info("Parameters Units preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload parameters units", error.message);
        });
    },
    preloadPartUnits() {
      // Preload part-units
      let dateRefreshed = this.lastUpdate.part_units;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Part Units do not need reload");
        return;
      }
      return apiService
        .getPartUnits()
        .then((data) => {
          this.setPartUnits(data.data);
          this.setLastUpdate("part_units", new Date());
          logger.default.info("Part Units preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload part units", error.message);
        });
    },
    preloadManufacturers() {
      // Preload manufacturers
      let dateRefreshed = this.lastUpdate.manufacturers;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Manufacturers do not need reload");
        return;
      }
      return apiService
        .getManufacturers()
        .then((data) => {
          this.setManufacturers(data.data);
          this.setLastUpdate("manufacturers", new Date());
          logger.default.info("Manufacturers preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload manufacturers", error.message);
        });
    },
    preloadDistributors() {
      // Preload distributors
      let dateRefreshed = this.lastUpdate.distributors;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Distributors do not need reload");
        return;
      }
      return apiService
        .getDistributors()
        .then((data) => {
          this.setDistributors(data.data);
          this.setLastUpdate("distributors", new Date());
          logger.default.info("Distributors preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload distributors", error.message);
        });
    },
    preloadLabelTemplates() {
      // Preload Label Templates
      let dateRefreshed = this.lastUpdate.label_templates;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Label Templates do not need reload");
        return;
      }
      return apiService
        .getLabelTemplates()
        .then((data) => {
          this.setLabelTemplates(data.data);
          this.setLastUpdate("label_templates", new Date());
          logger.default.info("Label Templates preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload Label Templates", error.message);
        });
    },
    preloadPartParametersPresets() {
      // Preload part parameters presets
      let dateRefreshed = this.lastUpdate.parameters_presets;
      if (dateRefreshed && differenceInMinutes(new Date(), parseISO(dateRefreshed)) < REFRESH_TIME) {
        // No refresh for now
        logger.default.info("Part parameters do not need reload");
        return;
      }
      return apiService
        .getPartParameterPresets()
        .then((data) => {
          this.setPartParametersPresets(data.data.results);
          this.setLastUpdate("categories", new Date());
          logger.default.info("Part parameters presets preloaded");
        })
        .catch((error) => {
          logger.default.error("Cannot preload part parameters presets", error.message);
        });
    },
  },
  getters: {
    getCategories() {
      return this.categories || {};
    },
    getFootprints() {
      return this.footprints || [];
    },
    getStorages() {
      return this.storages || [];
    },
    getParametersUnits() {
      return this.parameters_unit || [];
    },
    getPartUnits() {
      return this.part_units || [];
    },
    getManufacturers() {
      return this.manufacturers || [];
    },
    getDistributors() {
      return this.distributors || [];
    },
    getLabelTemplates() {
      return this.label_templates || [];
    },
    getCurrentCategory() {
      return this.currentCategory || { id: null };
    },
    getPartParametersPresets() {
      return this.partParametersPresets || [];
    },
    getLastUpdate(item) {
      if (item) {
        return this.lastUpdate[item];
      } else {
        return this.lastUpdate;
      }
    },
  },
});
