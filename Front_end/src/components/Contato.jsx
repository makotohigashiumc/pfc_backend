import React, { useState, useEffect } from "react";

function Contato() {
  return (
    <section className="form-container">
      <h2 style={{ color: "#0077b6", marginBottom: "1rem" }}>Fale Conosco</h2>
      <p style={{ marginBottom: "2rem" }}>
        Tem dúvidas, sugestões ou precisa de suporte? <br />
        Nossa equipe está pronta para te ajudar!
      </p>
      <ul style={{ listStyle: "none", padding: 0, fontSize: "1.1rem" }}>
        <li style={{ marginBottom: "1rem" }}>
          <span style={{ fontSize: "1.5rem", marginRight: "0.5rem", verticalAlign: "middle" }}>📧</span>
          <a href="mailto:contato@massoterapia.com" style={{ color: "#0077b6", textDecoration: "none", fontWeight: "bold" }}>
            contato@massoterapia.com
          </a>
        </li>
        <li style={{ marginBottom: "1rem" }}>
          <span style={{ fontSize: "1.5rem", marginRight: "0.5rem", verticalAlign: "middle" }}>📞</span>
          <a href="tel:+5511999999999" style={{ color: "#0077b6", textDecoration: "none", fontWeight: "bold" }}>
            (11) 99999-9999
          </a>
        </li>
        <li>
          <span style={{ fontSize: "1.5rem", marginRight: "0.5rem", verticalAlign: "middle" }}>📸</span>
          <a
            href="https://instagram.com/massoterapia"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "#0077b6", textDecoration: "none", fontWeight: "bold" }}
          >
            @massoterapia
          </a>
        </li>
      </ul>
    </section>
  );
}

export default Contato;
