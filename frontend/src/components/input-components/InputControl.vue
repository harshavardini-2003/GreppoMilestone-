<template>
    <div>
        <number-input
            v-if="data.type == 'Number'"
            :id="data.id"
            :name="data.name"
        />
        <text-input
            v-if="data.type == 'Text'"
            :id="data.id"
            :name="data.name"
        />
        <select-input
            v-if="data.type == 'Select'"
            :id="data.id"
            :name="data.name"
            :options="data.options"
        />
        <multi-select-input
            v-if="data.type == 'Multiselect'"
            :id="data.id"
            :name="data.name"
            :options="data.options"
        />
    </div>
</template>

<script>
import MultiSelectInput from "./MultiSelectInput.vue";
import NumberInput from "./NumberInput.vue";
import SelectInput from "./SelectInput.vue";
import TextInput from "./TextInput.vue";

export default {
    name: "InputControl",
    props: {
        data: Object,
    },
    components: { NumberInput, SelectInput, MultiSelectInput, TextInput },
};
</script>

<style></style>
