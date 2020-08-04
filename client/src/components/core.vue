<template class='outside'>
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
    <div class="container" id="scores">
      <scoreboard />
    </div>
    <div class="container">
      <form v-on:submit.prevent=find>
        <label>Search for a condition:</label>
        <br />
        <input id='gameForm' v-model="condition"
        display-attribute='condition' autocomplete="off" type="text"/>
        <button id='formButton' type="button" @click=random>Random Condition</button>
        <br />
        <button id='formButton' type="submit" v-on:click=find>Show top 100</button>
        <button id='formButton' type="button" v-on:click=gameSetup>Give me a game</button>
      </form>
    </div>
    <div v-show='showResults' id="results" >
      <table class="table" v-show='showResults' id="scores">
        <thead>
          <th>Drug Name</th>
          <th># of Studies</th>
        </thead>
        <tbody>
        <tr v-for="(result,index) in results" :key="index">
          <td>{{ result._id }}</td>
          <td>{{ result.count }}</td>
        </tr>
        </tbody>
      </table>
    </div>
    <div id='game' v-show="showGame">
      <form id="guess" class="container" v-on:submit.prevent=reveal>
        <label class="label">Your guess:</label>
        <br />
        <input id='gameForm' type="text" v:bind:value="guess"
        v-on:input="guess = $event.target.value" autocomplete="off"/>
        <button id="gameButton" type="submit">Take the guess</button>
        <button id="gameButton" type='button' v-on:click=closeGame>I give up!</button>
        <br />
      </form>
      <transition name="fade">
        <div class='alert' v-show="gameMessage != ''"> {{gameMessage}} </div>
      </transition>
      <div id="gameStats" class="container">
        <span>Found: {{this.found}} - Remaining: {{this.total - this.found}}</span>
        <br />
        <span>Score: {{(this.found / this.total * 100).toFixed(2)}}% </span>
      </div>
      <table class="table" id='revealed'>
        <transition-group name='fade'>
          <tr v-for="vendetta in revealed" :key="vendetta._id">
            {{vendetta._id}} - {{vendetta.count}}
          </tr>
        </transition-group>
      </table>
      <table id='remaining' class="table">
        <tr v-for="vendetta in pool" :key="vendetta._id">
            ??? - {{vendetta.count}}
        </tr>
      </table>
    </div>
    <div id="Game End" v-show="showEnd">
      <div id='gameStats' class='container'>
      Final Score = {{(this.found / this.total * 100).toFixed(2)}}%
      <br />
      <button id="gameButton" type="button" @click=logScore>Submit my score!</button>
      <br />
      <span> {{gameMessage}} </span>
      </div>
          <table id='revealed' class="table">
            <thead class='tablehead'>
              <th> Found: {{this.found}} - Remaining: {{this.total - this.found}}</th>
            </thead>
            <tbody name='fade' is='transition-group'>
              <tr v-for="vendetta in revealed" :key="vendetta._id">
                {{vendetta._id}} - {{vendetta.count}}
              </tr>
            </tbody>
           </table>
    </div>
    <loginModal v-show="isLoginVisible" @close="hideLogin" />
    <changePasswordModal v-show='isPassVisible' @close=hidePass />
    <footer>Fonts:
      <a href="https://fonts.google.com/specimen/Jura?subset=greek#standard-styles">Jura</a>
      , Designed by Daniel Johnson, Cyreal
      <br />
      <span class="Lato">
        <a href='https://fonts.google.com/specimen/Lato#standard-styles'>Lato</a>
        , Designed by Łukasz Dziedzic
      </span>
      <br />
      <span class="italic Lato">
        <a href="https://vuejs.org/">Vue</a>
        'd through a <a href="https://palletsprojects.com/p/flask/">Flask</a>
        by a <a href="https://www.docker.com/">Docker.</a>
      </span>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';
import loginModal from './loginModal.vue';
import changePasswordModal from './changePasswordModal.vue';
import scoreboard from './scoreboard.vue';
// import VueSimpleSuggest from 'vue-simple-suggest';

export default {
  name: 'main_page',
  components: {
    loginModal, changePasswordModal, scoreboard,
  },
  metaInfo: {
    title: 'Δες τι πήραν | Βρες τι πήραν',
    titleTemplate: '%s',
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
      this.condition = this.condition.charAt(0).toUpperCase() + this.condition.slice(1);
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
      if (((this.found / this.total) * 100).toFixed(2) === '0.00') {
        this.gameMessage = 'You can do better than this! Try again!';
        setTimeout(() => { this.gameMessage = ''; }, 3000);
      } else if (!this.scorePosted) {
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
        setTimeout(() => { this.gameMessage = ''; }, 3000);
      }
    },
    // general message manipulation method.
    showGameMessage(something) {
      const successMessages = ['Good guess!', "That's it!", 'Well done!', 'Great'];
      const failureMessages = ["Nope, that's not it.", 'Try again!', 'Nope'];
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
    getAutocomplete() {
      const term = this.condition;
      const path = `http://localhost:5000/autocomplete?term=${term}`;
      return axios.get(path).then((res) => res.data);
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
@import url(https://fonts.google.com/specimen/Jura?subset=greek#glyphs);
@import url(https://fonts.google.com/specimen/Lato#standard-styles);
  .fade-enter-active, .fade-leave-active{
    transition: opacity 1s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
    transform: translateY(30px);
  }
  #scores{
    border-radius:3px;
    font-size: 20px;
  }
  #results{
    margin:5px;
  }
  .table{
    border-radius: 10px;
    width:90%;
    margin: auto;
    text-align: center;
    border-style:dashed;
    border-width: 2px;
    border-collapse: collapse;
  }
  th{
    border-bottom-style: dashed;
    border-bottom-width: 1px;
  }
  .container{
    background-color: rgba(27, 62, 160, 0.144);
    border-radius: 25px;
    margin: auto;
    text-align: center;
    width: 80%;
    border-style:groove;
    border-width: 2px;
  }
  #guess{
    height:auto;
  }
  #gameStats{
    font-size:40px;
  }
  #gameButton{
    font-size: 30px;
  }
  #formButton{
    font-size: 20px;
  }
  #gameForm{
    width:50%;
    font-size: 20px;
    text-align: center;
  }
  .alert{
    align-self: center;
    text-align: center;
  }
  body{
    background-color: rgb(33, 37, 41);;
  }
  .outside{
    margin-top:40px;
    font-family: 'Jura';
    color:white;
  }
  button{
    font-family: 'Lato', sans-serif;
    background-color:rgb(42, 99, 255);
    color:white;
    border-color:rgb(42, 99, 255);
    padding:5px;
    border-radius: 5px;
    box-sizing: border-box;
    margin: 2px;
    margin-left:4px;
    margin-right:4px;
    align-content: center;
    font-weight: bold;
  }
  .italic{
    font-style:italic;
  }
  .Lato{
    font-family: 'Lato', sans-serif;
  }
  .alert{
    position: absolute;
    top:30%;
    left:2%;
    border-style:solid;
    background-color: rgb(42, 99, 255);
    border-radius: 5px;
    border-color: rgb(42, 99, 255);
    border-width:  2px;
  }
  .header{
    font-size: 18px;
    color:white;
    background:rgb(33, 37, 41);
    border-bottom: 1px solid #eeeeee;
    position:fixed;
    left:0;
    top:0;
    width:100%;
    height:auto;
  }
  tr{
    border-bottom: 1px dotted;
    font-size:23px;
  }
  label{
    font-size: 30px;
    font-weight: bold;
  }
  footer{
    border-top:1px solid white;
    text-align: center;
    left:0;
    width:100%;
    height:auto;
  }
  a{
    color: orange;
  }
</style>
