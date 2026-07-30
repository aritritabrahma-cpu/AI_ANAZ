import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";

import LiveAPI from "./pages/LiveAPI";

import History from "./pages/History";

import Charts from "./pages/Charts";

import Alerts from "./pages/Alerts";

import "./App.css";

function App(){

    return(

        <BrowserRouter>

            <Sidebar/>

            <div className="main">

                <Routes>

                    <Route path="/" element={<Dashboard/>}/>

                    <Route path="/live" element={<LiveAPI/>}/>

                    <Route path="/history" element={<History/>}/>

                    <Route path="/charts" element={<Charts/>}/>

                    <Route path="/alerts" element={<Alerts/>}/>

                </Routes>

            </div>

        </BrowserRouter>

    );

}

export default App;