import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import NavBar from './demo_pages/NavigationBar';
import Overview from './demo_pages/Overview';
import Segmentation from './demo_pages/Segmentation';
import Instruction from './demo_pages/Instruction';

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
  <>
    <div className='App'>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/segmentation" element={<Segmentation />} />
          <Route path="/instruction" element={<Instruction />} />
        </Routes>
      </BrowserRouter>
    </div>
  </>
  );
}

export default App;
