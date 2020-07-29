<template>
  <div id="app">
    <div id="login">
      <span>{{loginMessage}}</span>
      <span v-show='!isLoggedin'>
        <button type="button" @click="showLogin" >Log in!</button>
      </span>
      <span v-show='isLoggedin'>
        <button v-on:click='logout'>Logout</button>
        <button>Change Password</button>
      </span>
    </div>
    <div class="textbox">
      <form v-on:submit.prevent="onSubmit" v-on:submit:=find>
        <label>Search for a condition:</label>
        <br />
        <input v-bind:value="condition"
  v-on:input="condition = $event.target.value" type="text" />
        <br />
        <button type="submit" v-on:click=find>Show top 100</button>
        <button type="button" v-on:click=gameSetup>Give me a game</button>
      </form>
    </div>
    <div v-show='showResults' id="results" >
      <table v-show='showResults' id="scores">
        <tr>
          <th>Drug Name</th>
          <th>Studies</th>
        </tr>
        <tr></tr>
        <tr v-for="result in results" :key="result">
          <td>{{ result._id }}</td>
          <td>{{ result.count }}</td>
        </tr>
      </table>
    </div>
    <div id='game' v-show="showGame">
      <form class="textbox" v-on:submit.prevent="onSubmit" v-on:submit:=reveal>
        <label>Your guess:</label>
        <br />
        <input type="text" v:bind:value="guess" v-on:input="guess = $event.target.value" />
        <button type="submit" v-on:click=reveal>Take the guess</button>
        <button type='button' v-on:click=logScore>I give up! Log my score.</button>
      </form>
      <table id='revealed'>
        <thead>
          <th> Found: {{this.found}} - Remaining: {{this.total - this.found}}</th>
          <th>Score: {{(this.found / this.total * 100).toFixed(2)}}%</th>
        </thead>
        <tr v-show="gameMessage != ''">
          <span> {{gameMessage}} </span>
        </tr>
        <tbody name='fade' is='transition-group'>
          <tr v-for="vendetta in revealed" :key="vendetta._id">
            {{vendetta._id}} - {{vendetta.count}}
          </tr>
        </tbody>
      </table>
      <th> Remaining: {{this.total - this.found}}</th>
      <table id='remaining'>
        <tr v-for="vendetta in pool" :key="vendetta._id">
            ??? - {{vendetta.count}}
        </tr>
      </table>
    </div>
    <loginModal v-show="isLoginVisible" @close="hideLogin" />
  </div>
</template>

<script>
import axios from 'axios';
import loginModal from './loginModal.vue';

export default {
  name: 'main_page',
  components: {
    loginModal,
  },
  data() {
    return {
      results: '',
      condition: '',
      guess: '',
      pool: '',
      revealed: [],
      total: 0,
      found: 0,
      showResults: '',
      showGame: '',
      isLoginVisible: false,
      loginMessage: 'You are not logged in.',
      isLoggedin: false,
      gameMessage: '',
    };
  },
  methods: {
    find() {
      this.showResults = true;
      this.showGame = false; // TODO: check if a game is being interrupted.
      this.reset();
      const path = `http://localhost:5000/condition?condition=${this.condition}`;
      axios.get(path).then((res) => {
        this.results = res.data.slice(0, 100);
      });
    },
    gameSetup() {
      let i;
      // TODO: something in case the list is empty
      this.showResults = false;
      this.showGame = true;
      this.reset();
      const path = `http://localhost:5000/condition?condition=${this.condition}`;
      axios.get(path).then((res) => {
        this.pool = res.data;
        if (this.pool !== []) {
          for (i = 0; i < this.pool.length; i += 1) {
            this.total += this.pool[i].count;
          }
        } else {
        // Error Message
        }
      });
    },
    reset() {
      this.total = 0;
      this.found = 0;
      this.pool = [];
      this.revealed = [];
      this.guess = '';
    },
    reveal() {
      let removed = [];
      let i;
      if (this.guess.length > 2) {
        for (i = 0; i < this.pool.length; i += 1) {
          // eslint-disable-next-line
          if (this.pool[i]._id.search(new RegExp(`\\b${this.guess}\\b`, 'i')) != -1) { // eslint disagrees with the necessary _ here, had to disable it
            removed = this.pool.splice(i, 1); // TODO handle guesses with escape characters?
            i -= 1;
            this.revealed.reverse();
            this.revealed.push(removed[0]);
            this.revealed.reverse();
            this.found += removed[0].count;
            this.showGameMessage({ type: 'guess', result: 'success' });
          }
        }
        if (removed.length === 0) {
          this.showGameMessage({ type: 'guess', result: 'failure' });
        }
      }
    },
    showLogin() {
      this.isLoginVisible = true;
    },
    hideLogin() {
      if (localStorage.user) {
        this.loginMessage = `Welcome, ${localStorage.user}!`;
        this.isLoggedin = true;
      }
      this.isLoginVisible = false;
    },
    logout() {
      localStorage.clear();
      this.isLoggedin = false;
      this.loginMessage = 'You are not logged in.';
    },
    logScore() {
      if (this.isLoggedin) {
        const payload = JSON.parse(`{"condition": "${this.condition}", "username": "${localStorage.user}", "result": ${(this.found / this.total) * 100}}`);
        const path = 'http://localhost:5000/scores';
        axios.post(path, payload).then((res) => {
          if (res.data.success === true) {
            this.showGameMessage({ type: 'scoring', result: 'success' });
          }
        }).catch(() => {
          this.showGameMessage({ type: 'scoring', result: 'failure' });
        });
      }
    },
    showGameMessage(something) {
      const successMessages = ['Good guess!', "That's it!", 'Well done!'];
      const failureMessages = ["Nope, that's not it.", 'Try again!'];
      if (something.type === 'scoring') {
        if (something.result === 'success') {
          this.gameMessage = 'Score posted successfully!';
        } else {
          this.gameMessage = 'Score posting failed, try again later.';
        }
      } else if (something.type === 'guess') {
        if (something.result === 'success') {
          this.gameMessage = successMessages[Math.floor(Math.random() * successMessages.length)];
        } else {
          this.gameMessage = failureMessages[Math.floor(Math.random() * failureMessages.length)];
        }
      }
      setTimeout(() => { this.gameMessage = ''; }, 2000);
    },
  },
  created() {
    this.showResults = false;
    this.showGame = false;
    if (localStorage.user) {
      this.loginMessage = `Welcome, ${localStorage.user}!`;
      this.isLoggedin = true;
    }
  },
};
</script>

<style scoped lang="css">
  .fade-enter-active, .fade-leave-active{
    transition: opacity 1s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
    transform: translateY(30px);
  }

  .textbox{
    width: 50%;
    border-style:groove;
    border-width: 5px;
  }
</style>
