import React from "react";

function Especialidades() {
  // Futuramente podemos receber as especialidades via props ou API
  const especialidades = [
    "Quiropraxía",
    "Ventosaterapia",
    "Acupuntura",
    "Shiatsu",
    "Moxaterapia",
  ];

  return (
    <section className="form-container">
      <h2>Conheça nossas especialidades</h2>
      <ul>
        {especialidades.map((esp, index) => (
          <li key={index}>{esp}</li>
        ))}
      </ul>
    </section>
  );
}

export default Especialidades;
