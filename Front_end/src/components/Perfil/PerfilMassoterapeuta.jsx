// PerfilMassoterapeuta.jsx
// Componente para o massoterapeuta editar/visualizar suas informações pessoais

import React, { useState } from "react";

function PerfilMassoterapeuta({ usuario, token }) {
  const [editando, setEditando] = useState(false);
  const [nome, setNome] = useState(usuario.nome);
  const [telefone, setTelefone] = useState(usuario.telefone);
  const [email, setEmail] = useState(usuario.email);
  const [especialidade, setEspecialidade] = useState(usuario.especialidade || "");
  const [registro, setRegistro] = useState(usuario.registro_profissional || "");
  // ...

  const salvar = async () => {
  // ...
    try {
      const resp = await fetch("http://localhost:5000/api/massoterapeuta/me", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ nome, telefone, email, especialidade, registro_profissional: registro }),
      });

      if (resp.ok) {
        alert("Informações atualizadas com sucesso!");
        setEditando(false);
      } else {
        const err = await resp.json();
        alert(err.erro || "Erro ao atualizar informações.");
      }
    } catch (e) {
      console.error(e);
      alert("Erro ao atualizar informações.");
    }
  };

  return (
    <div className="perfil-container">
      <h2>Perfil do Massoterapeuta</h2>
      {/* ... */}
      {editando ? (
        <div>
          <label>
            Nome:{" "}
            <input value={nome} onChange={(e) => setNome(e.target.value)} />
          </label>
          <label>
            Telefone:{" "}
            <input
              value={telefone}
              onChange={(e) => setTelefone(e.target.value)}
            />
          </label>
          <label>
            Email:{" "}
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            Especialidade:{" "}
            <input
              value={especialidade}
              onChange={(e) => setEspecialidade(e.target.value)}
            />
          </label>
          <label>
            Registro Profissional:{" "}
            <input
              value={registro}
              onChange={(e) => setRegistro(e.target.value)}
            />
          </label>
          <button onClick={salvar}>Salvar</button>
          <button onClick={() => setEditando(false)}>Cancelar</button>
        </div>
      ) : (
        <div>
          <p>Nome: {nome}</p>
          <p>Telefone: {telefone}</p>
          <p>Email: {email}</p>
          <p>Especialidade: {especialidade}</p>
          <p>Registro Profissional: {registro}</p>
          <button onClick={() => setEditando(true)}>Editar informações</button>
        </div>
      )}
    </div>
  );
}

export default PerfilMassoterapeuta;
