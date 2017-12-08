<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" fullscreen transition="dialog-bottom-transition" :overlay=false>
      <v-btn color="primary" dark slot="activator">New Risk Type</v-btn>
      <v-card>

        <v-toolbar dark color="primary">
          <v-btn icon @click="closeDialog()" dark>
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title v-model="dialogTitle">{{ dialogTitle }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark flat @click="validateRiskType()">Save</v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-progress-linear v-bind:indeterminate="true" v-if="inProgress" class="ma-0"></v-progress-linear>

        <v-container grid-list-md fluid>
          <v-layout row wrap>
            <v-flex xs4>
              <v-card>
                <v-card-title>
                  <div>
                    <h3 class="headline">Controls</h3>
                    <p>Drag form controls from this panel to the right <strong>design stage</strong> to add them.</p>
                  </div>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="px-0">
                  <template>
                    <div class="text-xs-center pa-3">
                      <draggable v-model="controls" class="dragArea" :options="{group:{ name:'controls', pull:'clone', put:false }, sort:false}" :clone="clone">
                        <v-chip outline v-for="(item, index) in controls" :key="index" color="primary">{{ item.name }}</v-chip>
                      </draggable>
                    </div>
                  </template>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs4>
              <v-card>
                <v-card-title primary-title>
                  <div>
                    <h3 class="headline">Design Stage</h3>
                  </div>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="design-area">
                  <v-form v-model="valid">
                    <v-text-field
                      v-model="riskTypeName"
                      label="Risk Type Name"
                      :counter="255"
                      required
                    ></v-text-field>
                    <draggable v-model="selectedControls" class="dropArea dragArea" :options="{group:'controls'}">
                      <div v-for="(item, index) in selectedControls" :key="index">
                        <v-card class="pa-3 mb-2">
                          <v-subheader class="pl-0">
                            <v-btn icon @click="removeSelectedControl(index)">
                              <v-icon>delete_forever</v-icon>
                            </v-btn>
                            <strong>{{ item.name }}</strong>
                          </v-subheader>
                          <v-card-text class="pt-0">
                            <v-text-field
                              label="Label"
                              v-model.trim="item.label"
                              :counter="255"
                              required
                            ></v-text-field>
                            <v-text-field
                              v-if="item.field_type == 'select'"
                              label="Comma separated options"
                              v-model.trim="item.options"
                              :counter="255"
                              required
                            ></v-text-field>
                            <v-text-field
                              label="Help Text"
                              v-model.trim="item.help_text"
                              hint="The help text appears below the field on the form. Use it to clarify what this field means or to give further instructions."
                              persistent-hint
                            ></v-text-field>
                            <v-checkbox
                              label="Required?"
                              v-model="item.required"
                            ></v-checkbox>
                          </v-card-text>
                        </v-card>
                        <v-divider></v-divider>
                      </div>
                    </draggable>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-flex>
            <v-flex xs4>
              <v-card>
                <v-card-title>
                  <div>
                    <h3 class="headline">Preview</h3>
                    <p>Preview of the Risk Type form.</p>
                  </div>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-3">
                  <template v-model="selectedControls">
                    <v-form>
                      <div v-for="(item, index) in selectedControls" :key="index" v-if="item.label != '' && item.label != undefined">
                        <v-text-field
                          v-if="item.field_type == 'char'"
                          :label="item.label"
                          :hint="item.help_text"
                          persistent-hint
                          :required="item.required ? true : false"
                        ></v-text-field>

                        <v-text-field
                          v-if="item.field_type == 'integer'"
                          :label="item.label"
                          :hint="item.help_text"
                          persistent-hint
                          :required="item.required ? true : false"
                          mask="##########"
                        ></v-text-field>

                        <v-menu
                          v-if="item.field_type == 'date'"
                          lazy
                          :close-on-content-click="false"
                          v-model="menu"
                          transition="scale-transition"
                          offset-y
                          full-width
                          :nudge-right="40"
                          max-width="290px"
                          min-width="290px"
                        >
                          <v-text-field
                            slot="activator"
                            :label="item.label"
                            :hint="item.help_text"
                            persistent-hint
                            v-model="dateFormatted"
                            prepend-icon="event"
                            @blur="date = parseDate(dateFormatted)"
                            :required="item.required ? true : false"
                          ></v-text-field>
                          <v-date-picker v-model="date" @input="dateFormatted = formatDate($event)" no-title scrollable actions>
                            <template slot-scope="{ save, cancel }">
                              <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn flat color="primary" @click="cancel">Cancel</v-btn>
                                <v-btn flat color="primary" @click="save">OK</v-btn>
                              </v-card-actions>
                            </template>
                          </v-date-picker>
                        </v-menu>

                        <v-select
                          v-if="item.field_type == 'select'"
                          v-bind:items="item.options.replace(/^[\s,]+|[\s,]+$/g, '').split(',')"
                          :label="item.label"
                          :hint="item.help_text"
                          persistent-hint
                          :required="item.required ? true : false"
                        ></v-select>

                      </div>
                    </v-form>
                  </template>
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
      <v-snackbar
        :timeout="snackTimeout"
        :color="snackColor"
        :top="snackY === 'top'"
        :bottom="snackY === 'bottom'"
        :right="snackX === 'right'"
        :left="snackX === 'left'"
        :multi-line="snackMode === 'multi-line'"
        :vertical="snackMode === 'vertical'"
        v-model="snackbar"
      >
        {{ snackText }}
        <v-btn dark flat @click.native="snackbar = false">Close</v-btn>
      </v-snackbar>
    </v-dialog>

  </v-layout>
</template>

<script>
  import axios from 'axios';
  import draggable from 'vuedraggable';
  import bus from '../EventBus';
  export default {
    props: {
      items: {
        type: Array,
        required: true
      }
    },
    components: {
      draggable
    },
    created () {
      this.fetchData();
      bus.$on('showRiskTypeDetails', i => {
        this.riskType = this.items[i];
        this.riskType.index = i;
        this.selectedControls = this.riskType.fields;
        this.dialogTitle = this.riskType.name;
        this.riskTypeName = this.riskType.name;
        this.dialog = true;
      });
    },
    data () {
      return {
        dialogTitle: 'New Risk Type',
        dialog: false,
        valid: true,
        inProgress: false,
        controls: [],
        selectedControls: [],
        riskTypeName: '',
        riskType: null,
        snackbar: false,
        snackY: 'top',
        snackX: null,
        snackMode: '',
        snackTimeout: 6000,
        snackText: '',
        snackColor: 'error',
        date: null,
        dateFormatted: null,
        menu: false
      }
    },
    methods: {
      fetchData () {
        axios.get('api/fields/')
          .then(response => {
            this.controls = response.data;
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      clone (el) {
        return {
          name: el.name,
          field_type: el.field_type,
          id: el.id || 0,
          label: '',
          required: false,
          help_text: '',
          options: ''
        }
      },
      removeSelectedControl (i) {
        this.selectedControls.splice(i, 1);
      },
      validateRiskType () {
        let l = this.selectedControls.length;
        if (l > 0 || this.riskTypeName) {
          if (!this.riskTypeName) {
            this.showError('Please provide Risk Type Name');
            return false;
          }
          if (l === 0) {
            this.showError('Please add at least one field from controls');
            return false;
          }
          for (let i = 0; i < l; i++) {
            let el = this.selectedControls[i];
            if (!el.label || el.label.trim() === '') {
              this.showError('Please provide label for ' + el.name);
              return false;
            }
          }
          // all good lets save
          this.saveRiskType();
        } else {
          this.closeDialog();
        }
      },
      closeDialog () {
        this.dialog = false;
        this.inProgress = false;
        this.snackbar = false;
        this.selectedControls = [];
        this.snackText = '';
        this.dialogTitle = 'New Risk Type';
        this.riskTypeName = '';
        this.riskType = null;
      },
      saveRiskType () {
        let self = this;
        self.inProgress = true;
        let data = {
          'name': this.riskTypeName,
          'fields': this.selectedControls
        };
        if (self.riskType) {
          // update existing
          axios.patch('api/risks/' + self.riskType.id + '/', data)
            .then(response => {
              bus.$emit('updateItems', self.riskType, response.data);
              self.closeDialog();
            })
            .catch(function (error) {
              console.log(error);
              self.inProgress = false;
              self.showError('Sorry! Something went wrong');
            });
        } else {
          // create new
          axios.post('api/risks/', data)
            .then(response => {
              self.items.unshift(response.data);
              self.closeDialog();
            })
            .catch(function (error) {
              console.log(error);
              self.inProgress = false;
              self.showError('Sorry! Something went wrong');
            });
        }
      },
      formatDate (date) {
        if (!date) {
          return null
        }

        const [year, month, day] = date.split('-');
        return `${month}/${day}/${year}`
      },
      parseDate (date) {
        if (!date) {
          return null
        }

        const [month, day, year] = date.split('/');
        return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
      },
      showError (err) {
        this.snackbar = false;
        this.snackText = err;
        this.snackbar = true;
      }
    }
  }
</script>


<style>
  .dropArea { min-height: 50px; }
  .chip--active:not(.chip--disabled):after, .chip--selected:not(.chip--disabled):after, .chip:focus:not(.chip--disabled):after { left: 0; }
  .chip.chip--outline { width: 200px; justify-content: center; display: block; margin: 0 auto 10px; }
  .design-area .chip.chip--outline { display: inline-flex; }
</style>
