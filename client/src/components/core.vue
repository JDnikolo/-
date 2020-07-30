<template>
  <div id="app" class='outside'>
    <header id="login" class="header">
      <span>{{loginMessage}}</span>
      <span v-show='!isLoggedin'>
        <button type="button" @click="showLogin" >Log in!</button>
      </span>
      <span v-show='isLoggedin'>
        <button v-on:click='logout'>Logout</button>
        <button @click=showPass>Change Password</button>
      </span>
    </header>
    <section>
    <div class="container">
      <form v-on:submit.prevent=find>
        <label>Search for a condition:</label>
        <br />
        <input v-bind:value="condition"
  v-on:input="condition = $event.target.value" type="text" />
        <button type="button" @click=random>Random Condition</button>
        <br />
        <button type="submit" v-on:click=find>Show top 100</button>
        <button type="button" v-on:click=gameSetup>Give me a game</button>
      </form>
    </div>
    <div v-show='showResults' id="results" >
      <table class="table" v-show='showResults' id="scores">
        <thead class='tablehead'>
          <th>Drug Name</th>
          <th>Studies</th>
        </thead>
        <tr></tr>
        <tr v-for="result in results" :key="result">
          <td>{{ result._id }}</td>
          <td>{{ result.count }}</td>
        </tr>
      </table>
    </div>
    <div id='game' v-show="showGame">
      <form class="container" v-on:submit.prevent=reveal>
        <label>Your guess:</label>
        <br />
        <input type="text" v:bind:value="guess" v-on:input="guess = $event.target.value" />
        <button type="submit">Take the guess</button>
        <button type='button' v-on:click=closeGame>I give up!</button>
        <br />
        <span> {{gameMessage}} </span>
      </form>
      <table class="table" id='revealed'>
        <thead class='tablehead'>
          <th> Found: {{this.found}} - Remaining: {{this.total - this.found}}</th>
          <th>Score: {{(this.found / this.total * 100).toFixed(2)}}%</th>
        </thead>
        <tr>
        </tr>
        <tbody name='fade' is='transition-group'>
          <tr v-for="vendetta in revealed" :key="vendetta._id">
            {{vendetta._id}} - {{vendetta.count}}
          </tr>
        </tbody>
      </table>
      <table id='remaining' class="table">
        <th> Remaining: {{this.total - this.found}}</th>
        <tr v-for="vendetta in pool" :key="vendetta._id">
            ??? - {{vendetta.count}}
        </tr>
      </table>
    </div>
    <div class="container" id="Game End" v-show="showEnd">
      <table>
        <tr>
          <td> Final Score = {{(this.found / this.total * 100).toFixed(2)}}%
            <button type="button" @click=logScore>Submit my score!</button></td>
        </tr>
        <tr> <span> {{gameMessage}} </span>
        </tr>
        <tr>
          <table id='revealed'>
            <thead class='tablehead'>
              <th> Found: {{this.found}} - Remaining: {{this.total - this.found}}</th>
            </thead>
            <tbody name='fade' is='transition-group'>
              <tr v-for="vendetta in revealed" :key="vendetta._id">
                {{vendetta._id}} - {{vendetta.count}}
              </tr>
            </tbody>
          </table>
        </tr>
      </table>
    </div>
    </section>
    <loginModal v-show="isLoginVisible" @close="hideLogin" />
    <changePasswordModal v-show='isPassVisible' @close=hidePass />
    <footer>Footer</footer>
  </div>
</template>

<script>
import axios from 'axios';
import loginModal from './loginModal.vue';
import changePasswordModal from './changePasswordModal.vue';

export default {
  name: 'main_page',
  components: {
    loginModal, changePasswordModal,
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
      showResults: false,
      showGame: false,
      showEnd: false,
      isLoginVisible: false,
      isPassVisible: false,
      loginMessage: 'You are not logged in.',
      isLoggedin: false,
      gameMessage: '',
      scorePosted: false,
    };
  },
  methods: {
    find() {
      this.showEnd = false;
      this.showGame = false; // TODO: check if a game is being interrupted.
      this.reset();
      const path = `http://localhost:5000/condition?condition=${this.condition}`;
      axios.get(path).then((res) => {
        this.results = res.data.slice(0, 100);
        this.showResults = true;
      });
    },
    gameSetup() {
      let i;
      // TODO: something in case the list is empty
      this.showEnd = false;
      this.showResults = false;
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
        this.showGame = true;
      });
    },
    reset() {
      this.scorePosted = false;
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
    showPass() {
      this.isPassVisible = true;
    },
    hidePass() {
      this.isPassVisible = false;
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
    closeGame() {
      this.showGame = false;
      this.showEnd = true;
    },
    logScore() {
      if (!this.scorePosted) {
        if (this.isLoggedin) {
          const payload = JSON.parse(`{"condition": "${this.condition}", "username": "${localStorage.user}", "result": ${(this.found / this.total) * 100}}`);
          const path = 'http://localhost:5000/scores';
          axios.post(path, payload).then((res) => {
            if (res.data.success === true) {
              this.showGameMessage({ type: 'scoring', result: 'success' });
              this.scorePosted = true;
            }
          }).catch(() => {
            this.showGameMessage({ type: 'scoring', result: 'failure' });
          });
        } else {
          this.gameMessage = 'You must be logged in to submit your score!';
          setTimeout(() => { this.showLogin(); }, 2000);
        }
      } else {
        this.gameMessage = "You've already submitted this score. Time for a new one!";
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
    random() {
      this.reset();
      this.showGame = false;
      this.showEnd = false;
      this.showResults = false;
      const page = Math.floor(Math.random() * 56750);
      // 56750: total number of conditions in base currently.
      const path = `http://localhost:5000/conditionlist?page=${page}&size=1`;
      axios.get(path).then((res) => {
        this.condition = res.data[0].condition;
      }).catch((error) => {
        if (error.request) {
          this.condition = 'Lupus';
        }
      });
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

  .table{
    width:90%;
    margin: auto;
    text-align: center;
    border-style:dashed;
    border-width: 2px;
  }
  .tablehead{
    border-bottom-style: double;
    border-bottom-width: 1px;
  }
  .container{
    margin: auto;
    text-align: center;
    width: 80%;
    border-style:groove;
    border-width: 2px;
  }
  .outside{
    margin:30px;
  }
  .header{
    background:white;
    border-bottom: 1px solid #eeeeee;
    position:fixed;
    left:0;
    top:0;
    width:100vw;
    z-index:200;
    height:auto;
  }
</style>
