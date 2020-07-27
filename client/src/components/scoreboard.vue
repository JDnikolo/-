<template>
  <div>
    <div id='scoreContainer'>
    Scores:
    </div>
    <div>
    <table id='scores'>
      <tr>
        <th>Name</th>
        <th>Condition</th>
        <th>Score</th>
      </tr>
      <tr>
        <tr v-for="scores in something" :key="scores">
              <td>{{ scores.username }}</td>
              <td>{{ scores.condition }}</td>
              <td>{{ scores.result }}</td>
      </tr>
    </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'page',
  data() {
    return {
      something: '!',
    };
  },
  methods: {
    getScores() {
      const path = 'http://localhost:5000/scores';
      axios.get(path).then((res) => {
        const reply = res.data;
        reply.sort((a, b) => b.result - a.result);
        this.something = reply;
      })
        .catch((error) => {
          // eslint-disable-next-line
			console.error(error)
        });
    },
  },
  created() {
    this.getScores();
    this.timer = setInterval(this.getScores, 30000);
  },
};
</script>
