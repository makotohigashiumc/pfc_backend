import React from "react";

function Especialidades() {
  // Futuramente podemos receber as especialidades via props ou API
  const especialidades = [
    "Massagem Relaxante",
    "Massagem Terapêutica",
    "Drenagem Linfática",
    "Shiatsu",
  ];

  return (
    <section className="form-container">
      <h2>Especialidades</h2>
      <ul>
        {especialidades.map((esp, index) => (
          <li key={index}>{esp}</li>
        ))}
      </ul>
    </section>
  );
}

export default Especialidades;
