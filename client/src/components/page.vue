<template>
<div>
<div id='main'>
Text goes here
</div>
<div>
{{ something }}
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
        this.something = res.data;
      })
        .catch((error) => {
          // eslint-disable-next-line
			console.error(error)
        });
    },
  },
  created() {
    this.getScores();
  },
};
</script>
