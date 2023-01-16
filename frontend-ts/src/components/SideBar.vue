<template>
  <nav class="flex flex-col justify-between w-52 z-50">
    <div class="flex flex-col py-4">
      <SidebarItem
        title="General"
        :links="general"
        @select="setSelected"
        :selected="selected === 'General'"
      >
        <template #icon><HashtagIcon /></template>
      </SidebarItem>

      <SidebarItem
        title="Traffic"
        :links="traffic"
        @select="setSelected"
        :selected="selected === 'Traffic'"
      >
        <template #icon><HashtagIcon /></template>
      </SidebarItem>

      <SidebarItem
        title="Accounting"
        :links="accounting"
        @select="setSelected"
        :selected="selected === 'Accounting'"
      >
        <template #icon><HashtagIcon /></template>
      </SidebarItem>

      <SidebarItem
        title="Technical"
        :links="technical"
        @select="setSelected"
        :selected="selected === 'Technical'"
      >
        <template #icon><HashtagIcon /></template>
      </SidebarItem>

      <SidebarItem
        title="Production"
        :links="production"
        @select="setSelected"
        :selected="selected === 'Production'"
      >
        <template #icon><HashtagIcon /></template>
      </SidebarItem>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import SidebarItem from "./SidebarItem.vue";
import { HashtagIcon } from "@heroicons/vue/outline";

const emits = defineEmits(["afterset"]);

const selected = ref("");
const setSelected = (menu: string) => {
  selected.value = menu;
  emits("afterset");
};
const general = [
  {
    name: "Activities",
    location: "/",
  },
  {
    name: "Profile",
    location: "/profile",
  },
  {
    name: "People",
    location: "/people",
  },
];
const traffic = [
  {
    name: "Ads",
    location: "/ads",
  },
  {
    name: "Packages",
    location: "/packages",
  },
];
const technical = [
  {
    name: "Inventory",
    location: "/inventory",
  },
  {
    name: "Consumption",
    location: "/power",
  },
  {
    name: "Brown Out",
    location: "/power_outage",
  },
  {
    name: "Transmitter",
    location: "/transmitter",
  },
];

const accounting = [
  {
    name: "Billing",
    location: "/billing",
  },
];

const production = [
  {
    name: "Promos",
    location: "/promos",
  },
];

interface Link {
  name: string;
  location: string;
}
const extractPropArray = (objArray: Array<Link>) => {
  return objArray.map((prop) => prop.location);
};

onMounted(() => {
  const generalLocations = extractPropArray(general);
  const trafficLocations = extractPropArray(traffic);
  const technicalLocations = extractPropArray(technical);
  const accountingLocations = extractPropArray(accounting);
  const productionLocations = extractPropArray(production);

  if (generalLocations.includes(location.pathname)) selected.value = "General";
  else if (trafficLocations.includes(location.pathname))
    selected.value = "Traffic";
  else if (technicalLocations.includes(location.pathname))
    selected.value = "Technical";
  else if (accountingLocations.includes(location.pathname))
    selected.value = "Acounting";
  else if (productionLocations.includes(location.pathname))
    selected.value = "Production";
});
</script>
