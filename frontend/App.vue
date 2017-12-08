<template>
  <v-app id="app">
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-title>Insurance Risks App</v-toolbar-title>
      <div class="d-flex align-center" style="margin-left: auto">
        <risk-builder :items="items"></risk-builder>
      </div>
    </v-toolbar>
    <v-content>
      <v-container grid-list-md>
        <v-layout row wrap>
          <risk-types :items="items"></risk-types>
        </v-layout>
      </v-container>
    </v-content>
    <v-footer color="indigo" app>
      <span class="white--text">&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
  import axios from 'axios';
  import RiskTypes from './components/RiskTypes.vue';
  import RiskBuilder from './components/RiskBuilder.vue';
  import bus from './EventBus';
  export default {
    name: 'app',
    components: {
      RiskTypes,
      RiskBuilder
    },
    created () {
      this.fetchData();
      bus.$on('updateItems', (o, n) => {
        const newData = this.items.slice();
        newData[o.index] = n;
        this.items = newData;
      });
      bus.$on('removeItem', i => {
        this.items.splice(i, 1);
      });
    },
    data () {
      return {
        items: []
      }
    },
    props: {
      source: String
    },
    methods: {
      fetchData () {
        axios.get('api/risks/')
          .then(response => {
            this.items = response.data;
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    }
  };
</script>
