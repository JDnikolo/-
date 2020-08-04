<template>
  <div>
    <div id='scoreContainer'>
    Scores:
    </div>
    <div>
      <marquee-text :duration='120'>
        <span v-for="(scores,index) in something" :key="index">
          {{ scores.username }}, {{ scores.condition }}: {{ scores.result.toFixed(2) }}% ||
           </span>
      </marquee-text>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MarqueeText from 'vue-marquee-text-component';

export default {
  name: 'scoreboard',
  components: {
    MarqueeText,
  },
  data() {
    return {
      something: '',
      time: 120,
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
    this.timer = setInterval(this.getScores, 10000);
  },
};
</script>
