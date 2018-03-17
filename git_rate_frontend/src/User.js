import React from 'react';
import { Link } from 'react-router-dom';

export default class User extends React.Component {
  constructor() {
    super();
    this.state = {};
    this.getStarAverage = this.getStarAverage.bind(this)
  }

  async getUser() {
    let response = await fetch(`http://localhost:5000/user/ranking/${this.props.match.params.username}`)
    let resp_json = await response.json()
    let userinfo = resp_json.user
    let repos = resp_json.repos
    this.props.getDatafromUser(repos)
    let star_avg = await this.getStarAverage(repos);
    this.setState({
      user: userinfo,
      repos: repos,
      star_avg:star_avg
    })
  }

async getStarAverage(repos)
{
  var count=0;
  for(let i=0;i<repos.length;i++)
  {
    count+=repos[i].stargazers_count
  }
  var avg = count/repos.length;
  return avg
}

  componentDidMount() {
    this.getUser()
  }
  renderStat(stat) {
    return (
      <li key={stat.name} className="user-info__stat">
        <Link to={stat.url}>
          <p className="user-info__stat-value">{stat.value}</p>
          <p className="user-info__stat-name">{stat.name}</p>
        </Link>
      </li>
    );
  }


  render() {
    if (!this.state.user) {
      return (<div className="user-page">LOADING...</div>)
    }
    console.log(this.props.getDatafromUser)
    const user = this.state.user
    const repos = this.state.repos
    const avg = this.state.star_avg
    console.log(avg)
    const stats = [
      {
        name: 'Public Repos',
        value: user.repo_count,
        url: `/user/${this.props.match.params.username}/repos`
      },
      {
        name: 'Followers',
        value: user.followers,
        url: `/user/${this.props.match.params.username}/followers`
      },
      {
        name: 'Following',
        value: user.following,
        url: `/user/${this.props.match.params.username}/following`
      },
      {
        name: 'Recent OpenSource Commits',
        value: user.commits_count,
        url: `/user/${this.props.match.params.username}/forks`
      },
      {
        name: 'Ranking',
        value: user.ranking,
        url: `/user/${this.props.match.params.username}/forks`
      },
      {
        name: 'Language_Ranking',
        value: user.ranking,
        url: `/user/${this.props.match.params.username}/languagesort`
      }
    ];
    let foll_tip
    let star_tip
    let rep_ratio = user.repo_count / user.public_repos
    let rep_tip
    if(stats[1].value<100)
    {
      foll_tip = (
        <li className="card-info-back">More activity needed in the git community</li>
      )
    }
    else{
      foll_tip = (
        <li className="card-info-back">Sufficient socialisation</li>
      )
    }
    if(avg < 8) {
      star_tip = (
        <li  className="card-info-back"> Increase understandability of repos</li>
      )
    }
    else{
      star_tip = (
        <li className="card-info-back">Stars to Repos ratio seems good</li>
      )
    }
    if(rep_ratio<0.5)
    {
      rep_tip = (
        <li className="card-info-back">Need to create more personal repos</li>
      )
    }
    else
    {
      rep_tip = (
        <li className="card-info-back">Sufficient number of personal repos</li>
      )
    }
    return (
      <div className="grid-container">
        <div className="grid-item-1" style={{ color: 'white' }} />
        <div className="grid-item-2" style={{ color: 'white' }}>
          <div className="header">
            <div>
              Overview
            </div>
            <hr size={1} />
          </div>
        </div>
        <div className="grid-item-3" style={{ color: 'white' }} />
        <div className="grid-item-4">
          <div className="side">
            <div className="list-group">
              <a href="#">Overview</a>
            </div>
            <Link to={stats[0].url}>
              <div className="list-group">
                <a href="#">Repo wise stats</a>
              </div>
            </Link>
            <Link to={stats[5].url}>
              <div className="list-group">
                <a href="#">Language wise stats</a>
              </div>
            </Link>
            <hr />
          </div>
        </div>
        <div className="grid-item-5" style={{ color: 'white' }}>
            <div id="chartContainer3">
                <img id="chartimage" src={user.avatar_url} alt={`${user.login} avatar`} />
            </div>
            <div id="chartContainer3">
                <div className="flip-card3">
                    <div className="card-front">
                        <div className="card-info-front">ANALYSIS</div>
                    </div>
                    <div className="card-back">
                        <ul>
                            {foll_tip}
                            {star_tip}
                            {rep_tip}
                        </ul>
                    </div>
                </div>
            </div>
            <div id="rankContainer3" style={{ backgroundColor: 'rgba(255,99,132,0.6)' }}>
                 <div id="rankvalue">
                    RATING : {user.ranking.toString().substr(0,7)}
                 </div>
            </div>
        </div>
        <div className="grid-item-6" />
        <div className="grid-item-7" />
        <div className="grid-item-8">
          <div className="divider" style={{ color: 'white' }}>
            <div className="left"><hr /></div>
            <div className="text">QUICK STATS</div>
            <div className="right"><hr /></div>
          </div>
          <div className="stats">
            <div className="quick-stats" style={{ backgroundColor: '#00d18c' }}>
              <div className="text-quick-stats">
                <h4>REPOS</h4>
                <h4>{stats[0].value}</h4>
              </div>
            </div>
            <div className="quick-stats" style={{ backgroundColor: '#f72b4d' }}>
              <div className="text-quick-stats">
                <h4>FOLLOWERS</h4>
                <h4>{stats[1].value}</h4>
              </div>
            </div>
            <div className="quick-stats" style={{ backgroundColor: '#a974ff' }}>
              <div className="text-quick-stats">
                <h4>FOLLOWING</h4>
                <h4>{stats[2].value}</h4>
              </div>
            </div>
            <div className="quick-stats" style={{ backgroundColor: '#e3de00' }}>
              <div className="text-quick-stats">
                <h5>OPEN SOURCE COMMITS</h5>
                <h4>{stats[3].value}</h4>
              </div>
            </div>
          </div>
        </div>
        <div className="grid-item-9" />
      </div>
    );
  }
};
