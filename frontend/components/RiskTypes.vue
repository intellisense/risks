<template>
  <v-data-table
      v-bind:headers="headers"
      :items="items"
      hide-actions
      class="elevation-1"
    >
    <template slot="items" slot-scope="props">
      <td class="text-xs-center"><a href="#" @click.prevent="showRiskTypeDetails(props.index);">{{ props.item.name }}</a></td>
      <td class="text-xs-center">{{ props.item.fields_count }}</td>
      <td class="text-xs-center">{{ props.item.created }}</td>
      <td class="text-xs-center">{{ props.item.modified }}</td>
      <td class="text-xs-center">
        <v-btn icon @click="removeRiskType(props.item, props.index)" color="error">
          <v-icon>delete_forever</v-icon>
        </v-btn>
      </td>
    </template>
    <template slot="no-data">
      <v-alert :value="true" color="info" icon="warning">
        There are no risk types created, create a new one by clicking on <strong>NEW RISK TYPE</strong> button.
      </v-alert>
    </template>
  </v-data-table>
</template>

<script>
  import bus from '../EventBus.js';
  import axios from 'axios';
  export default {
    props: {
      items: {
        type: Array,
        required: true
      }
    },
    data () {
      return {
        headers: [
          {text: 'Risk Type', align: 'center', value: 'name', sortable: false},
          {text: 'Fields Count', value: 'fields_count', align: 'center', sortable: false},
          {text: 'Created', value: 'created', align: 'center', sortable: false},
          {text: 'Modified', value: 'modified', align: 'center', sortable: false},
          {text: 'Action', value: 'action', align: 'center', sortable: false}
        ]
      }
    },
    methods: {
      showRiskTypeDetails: function (i) {
        bus.$emit('showRiskTypeDetails', i);
      },
      removeRiskType: function (rt, i) {
        axios.delete('api/risks/' + rt.id + '/')
          .then(response => {
            bus.$emit('removeItem', i);
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    }
  }
</script>
