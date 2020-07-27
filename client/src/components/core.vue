<template>
  <div id="container">
    <div id="textbox">
      <form v-on:submit.prevent="onSubmit" v-on:submit:=find>
        <label>Search for a condition:</label>
        <br />
        <input v-bind:value="condition"
  v-on:input="condition = $event.target.value" type="text" />
        <br />
        <button type="submit" v-on:click=find>Go</button>
      </form>
    </div>
    <div id="results">
      <span>Results go here:</span>
      <table id="scores">
        <tr>
          <th>Drug Name</th>
          <th>Relevant Studies</th>
        </tr>
        <tr></tr>
        <tr v-for="result in results" :key="result">
          <td>{{ result._id }}</td>
          <td>{{ result.count }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'conditions',
  data() {
    return {
      results: '',
      condition: '',
    };
  },
  methods: {
    find() {
      const path = `http://localhost:5000/condition?condition=${this.condition}`;
      axios.get(path).then((res) => {
        this.results = res.data.slice(0, 100);
      });
    },
  },
};
</script>
