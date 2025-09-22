// ContaCliente.jsx
// Página de conta do CLIENTE (visualização e dados básicos)

import React, { useEffect, useState } from "react";

function ContaCliente() {
  const [cliente, setCliente] = useState(null);

  useEffect(() => {
    // Busca os dados do cliente logado
    const fetchCliente = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          console.error("Token não encontrado. Faça login.");
          return;
        }

        const resp = await fetch("http://localhost:5000/api/clientes/me", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (resp.ok) {
          const data = await resp.json();
          setCliente(data);
        } else {
          console.error("Erro ao buscar dados do cliente");
        }
      } catch (err) {
        console.error("Erro na requisição:", err);
      }
    };

    fetchCliente();
  }, []);

  if (!cliente) return <p>Carregando informações...</p>;

  return (
    <div className="conta-cliente">
      <h2>Minha Conta (Cliente)</h2>
      <p><strong>Nome:</strong> {cliente.nome}</p>
      <p><strong>Email:</strong> {cliente.email}</p>
      <p><strong>Telefone:</strong> {cliente.telefone}</p>
      {/* Adicione outros campos se necessário */}

      <button onClick={() => alert("Funcionalidade de edição em breve!")}>
        Editar Perfil
      </button>
    </div>
  );
}

export default ContaCliente;