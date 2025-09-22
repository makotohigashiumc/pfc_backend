// AgendamentosMassoterapeuta.jsx
import React, { useState, useEffect } from "react";

function AgendamentosMassoterapeuta({ usuario }) {
  const [agendamentos, setAgendamentos] = useState([]); // Lista de agendamentos do massoterapeuta
  const [loading, setLoading] = useState(true);

  // Token (do massoterapeuta logado ou do localStorage)
  const token = usuario?.token || localStorage.getItem("token");

  // -------------------------------
  // Buscar agendamentos do massoterapeuta
  // -------------------------------
  useEffect(() => {
    if (!token) {
      console.error("Token não encontrado. Faça login primeiro.");
      return;
    }

    const fetchAgendamentos = async () => {
      try {
        const resp = await fetch("http://localhost:5000/api/massoterapeuta/agendamentos", {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });

        if (resp.ok) {
          const data = await resp.json();
          setAgendamentos(data);
        } else {
          console.error("Erro ao buscar agendamentos do massoterapeuta", resp.status);
          setAgendamentos([]);
        }
      } catch (err) {
        console.error("Erro na requisição de agendamentos", err);
        setAgendamentos([]);
      } finally {
        setLoading(false);
      }
    };

    fetchAgendamentos();
  }, [token]);

  // -------------------------------
  // Atualizar status do agendamento
  // -------------------------------
  const atualizarStatus = async (id, novoStatus) => {
    try {
      const resp = await fetch(`http://localhost:5000/api/massoterapeuta/agendamentos/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ status: novoStatus }),
      });

      if (resp.ok) {
        const msg = await resp.json();
        alert(msg.mensagem || "Status atualizado!");

        // Atualiza lista
        setAgendamentos((prev) =>
          prev.map((a) =>
            a.id === id ? { ...a, status: novoStatus } : a
          )
        );
      } else {
        const err = await resp.json();
        alert(err.erro || "Erro ao atualizar status.");
      }
    } catch (err) {
      console.error("Erro ao atualizar status", err);
      alert("Erro ao atualizar status.");
    }
  };

  // -------------------------------
  // Renderização
  // -------------------------------
  return (
    <div className="agendamentos-massoterapeuta-container">
      <h2>Agendamentos Recebidos</h2>

      {loading ? (
        <p>Carregando agendamentos...</p>
      ) : agendamentos.length === 0 ? (
        <p>Nenhum agendamento encontrado.</p>
      ) : (
        <ul>
          {agendamentos.map((a) => (
            <li key={a.id}>
              <strong>Cliente:</strong> {a.cliente_nome || "N/A"} <br />
              <strong>Data:</strong> {a.data_hora} <br />
              <strong>Status:</strong> {a.status} <br />
              <button onClick={() => atualizarStatus(a.id, "Confirmado")}>
                Confirmar
              </button>
              <button onClick={() => atualizarStatus(a.id, "Cancelado")}>
                Cancelar
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default AgendamentosMassoterapeuta;
