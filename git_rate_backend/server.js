var express = require('express');
var cors = require('cors')
var bodyParser = require('body-parser');
var app = express();
var fs = require('fs')
var http = require('http').createServer(app);
app.use(cors())
app.use(express.static('./Public'));
app.use(bodyParser.urlencoded({ extended: true }));;
http.listen(process.env.PORT || 5000);
var fetch = require('node-fetch');
var HttpsProxyAgent = require('https-proxy-agent');
var parse = require('parse-link-header');
var spawn = require("child_process").spawn
const client_id = 'fe1bcc900fac67e26d7c'
const client_secret = '0871e55b1a0c9c7d52b3c6c097a647fb28718b9c'
const per_page = 100
const proxy='http://iit2015089:9824110011@172.31.1.3:8080'

app.get('/user/ranking/:username', async function (req, res) {
    var rank_array
    var user_rank = 0
    var username = req.params.username
    var user = await getUser(username)
    console.log(user)
    var repos = await getAllRepos(username)
    var arr = await createArray(repos)
    var arr1 = JSON.stringify(arr)
    console.log(arr1)
    var pythonProcess = await spawn('python3', ["./model.py",arr]);
    await pythonProcess.stdout.on('data', function (data) {
        console.log(data.toString())
        rank_array = JSON.parse(data.toString())
        var len = rank_array.length
        for(let i =0;i<len;i++)
        {
           repos[i].ranking = rank_array[i]
           user_rank+=rank_array[i]
        }
        user.ranking = user_rank
        res.send({
            user:user,
        repos:repos})
    })
    

})


async function getUser(username) {
    try {
        let response = await fetch(`https://api.github.com/users/${username}?client_id=${client_id}&client_secret=${client_secret}`, { agent: new HttpsProxyAgent(proxy) })
        let userinfo = await response.json()
        let repoCount = await getReposCount(userinfo.repos_url)
        let eventsUrl = userinfo.events_url.split('{')[0]
        let commitsCount = await getCommitsCount(eventsUrl)
        userinfo.commits_count = commitsCount
        userinfo.repo_count = repoCount
        return userinfo

    }
    catch (e) {

    }
}

async function createArray(repos) {
    
}

async function getReposCount(repos_url){

}

async function getAllRepos(username) {
}

async function getCommitsCount(eventsUrl) {
}