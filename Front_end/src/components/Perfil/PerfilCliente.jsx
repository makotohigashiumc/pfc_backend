// PerfilCliente.jsx
// Componente para o cliente editar/visualizar suas informações pessoais

import React, { useState } from "react";

function PerfilCliente({ usuario, token }) {
  const [editando, setEditando] = useState(false);
  const [nome, setNome] = useState(usuario.nome);
  const [telefone, setTelefone] = useState(usuario.telefone);
  // ...

  const salvar = async () => {
  // ...
    try {
      const resp = await fetch("http://localhost:5000/api/clientes", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ nome, telefone, email: usuario.email }),
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

  async function excluirConta() {
  // ...
    const authToken = token || usuario?.token || localStorage.getItem("token");
  if (!window.confirm("Tem certeza que deseja excluir sua conta? Esta ação é irreversível.")) return;
    try {
      const resp = await fetch("http://localhost:5000/api/clientes", {
        method: "DELETE",
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (resp.ok) {
        alert("Conta excluída com sucesso!");
        localStorage.removeItem("token");
        setTimeout(() => window.location.reload(), 1200);
      } else {
        alert("Erro ao excluir conta.");
      }
    } catch (err) {
      setMensagem("Erro ao excluir conta.");
      setMensagemTipo("erro");
    }
  }

  return (
    <div className="perfil-container">
      {/* ... */}
      {editando ? (
        <div>
          <label>
            Nome: {" "}
            <input value={nome} onChange={(e) => setNome(e.target.value)} />
          </label>
          <label>
            Telefone: {" "}
            <input
              value={telefone}
              onChange={(e) => setTelefone(e.target.value)}
            />
          </label>
          <p>Email: {usuario.email}</p>
          <button onClick={salvar}>Salvar</button>
          <button onClick={() => setEditando(false)}>Cancelar</button>
        </div>
      ) : (
        <div>
          <p>Nome: {nome}</p>
          <p>Telefone: {telefone}</p>
          <p>Email: {usuario.email}</p>
          <button onClick={() => setEditando(true)}>Editar informações</button>
        </div>
      )}
      <button onClick={excluirConta} style={{background:'#d32f2f', color:'white', marginTop:'18px'}}>Excluir Conta</button>
    </div>
  );
}

export default PerfilCliente;
