import React,{Redirect,Component} from 'react';
import {BrowserRouter,Route,Link} from 'react-router-dom';
export default class Home extends Component{
    constructor(props)
    {
        super(props);

        this.handlesubmit=this.handlesubmit.bind(this);
        this.handlesubmit2=this.handlesubmit2.bind(this);
    }
 
    handlesubmit(e)
    {
        e.preventDefault();
        this.props.history.push(`/user/${this.refs.userInput.value}`)
    }
    handlesubmit2(e)
    {
        e.preventDefault();
        this.props.history.push(`/organisation/${this.refs.orgInput.value}`)
    }
    render()
    {
        return(
            <div className="login-container">
            <div className="login-grid1"></div>
            <div className="login-grid2"></div>
            <div className="login-grid3"></div>
            <div className="login-grid4"></div>
            <div className="login-grid5">
                <form className="loginform" onSubmit={this.handlesubmit}>
                <div className = "loginchild1">
                    <input ref="userInput" className="search-page_input" type="text" placeholder="enter github username" />
                </div>
                <div className = "loginchild2">
                    <button className="search-page_button">Search</button>
                </div>
                </form>
            </div>
            </div>
        );
    }
}