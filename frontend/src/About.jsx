import React from "react";
import "./App.css";

export default function About({ onBack }) {
  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo" onClick={onBack} style={{ cursor: "pointer" }}>
            <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" width="28" height="28">
              <rect width="32" height="32" rx="8" className="logo-bg" fill="#3b82f6"/>
              <path d="M10 22V16M14 22V12M18 22V10M22 22V16" stroke="white" strokeWidth="1.8" strokeLinecap="round" />
            </svg>
            <span className="logo-text">AudioVerify</span>
          </div>
          <nav className="nav">
            <a href="#" className="nav-link" onClick={onBack}>Analyze</a>
            <a href="#" className="nav-link nav-link--active">About</a>
          </nav>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <p className="hero-badge">Our Mission</p>
          <h1 className="hero-title">About AudioVerify</h1>
          <p className="hero-sub">
            This project was built for the FMI Hackathon. Our goal is to fight 
            AI-generated misinformation by providing a tool that detects 
            synthetic audio with high accuracy.
          </p>
          
          <div style={{ marginTop: '40px' }}>
             <button className="browse-btn" onClick={onBack}>
               Back to Analyzer
             </button>
          </div>
        </section>
      </main>
    </div>
  );
}
