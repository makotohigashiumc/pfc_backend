// AgendamentosCliente.jsx
import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function AgendamentosCliente({ usuario, token }) {
  const authToken = token || usuario?.token || localStorage.getItem("token");
  const [dataHora, setDataHora] = useState(null);
  const [historico, setHistorico] = useState([]);
  const [massoterapeutas, setMassoterapeutas] = useState([]);
  const [massoterapeutaSelecionado, setMassoterapeutaSelecionado] = useState("");

  // -------------------------------
  // Buscar histórico de agendamentos do cliente
  // -------------------------------
  useEffect(() => {
    if (!authToken) {
      alert("Sessão expirada. Faça login novamente.");
      localStorage.removeItem("token");
      window.location.reload();
      return;
    }

    const fetchHistorico = async () => {
      try {
        const resp = await fetch("http://localhost:5000/api/clientes/agendamentos", {
          method: "GET",
          headers: { Authorization: `Bearer ${authToken}` },
        });

        if (resp.ok) {
          const data = await resp.json();
          setHistorico(data);
        } else {
          setHistorico([]);
        }
      } catch (err) {
        setHistorico([]);
      }
    };

    fetchHistorico();
  }, [authToken]);

  // -------------------------------
  // Buscar lista de massoterapeutas
  // -------------------------------
  useEffect(() => {
    const fetchMassoterapeutas = async () => {
      try {
        const resp = await fetch("http://localhost:5000/api/massoterapeuta/lista");
        if (resp.ok) {
          const data = await resp.json();
          setMassoterapeutas(data);
          if (data.length > 0) setMassoterapeutaSelecionado(data[0].id);
        }
      } catch (err) {}
    };

    fetchMassoterapeutas();
  }, []);

  async function limparHistorico() {
    if (!window.confirm("Tem certeza que deseja limpar todo o histórico de agendamentos?")) return;
    try {
      const resp = await fetch("http://localhost:5000/api/clientes/agendamentos/limpar", {
        method: "POST",
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (resp.ok) {
        alert("Histórico limpo com sucesso!");
        setHistorico([]);
      } else {
        alert("Erro ao limpar histórico.");
      }
    } catch (err) {
      alert("Erro ao limpar histórico.");
    }
  }

  // -------------------------------
  // Criar novo agendamento
  // -------------------------------
  const criarAgendamento = async () => {
    if (!authToken) return alert("Você precisa estar logado para agendar.");
    if (!dataHora) return alert("Escolha data e hora");
    if (!massoterapeutaSelecionado) return alert("Escolha um massoterapeuta");
    // Bloqueia agendamento para horários passados
    const agora = new Date();
    if (dataHora < agora) {
      alert("Não é possível agendar para horários passados.");
      return;
    }
  // Formata data para ISO local (YYYY-MM-DDTHH:mm)
  const pad = (n) => n.toString().padStart(2, '0');
  const dataFormatada = `${dataHora.getFullYear()}-${pad(dataHora.getMonth()+1)}-${pad(dataHora.getDate())}T${pad(dataHora.getHours())}:${pad(dataHora.getMinutes())}`;

    try {
      const resp = await fetch("http://localhost:5000/api/clientes/agendamentos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify({
          massoterapeuta_id: massoterapeutaSelecionado,
          data_hora: dataFormatada,
        }),
      });

      if (resp.ok) {
        alert("Agendamento criado!");
        setDataHora("");

        // Atualiza histórico
        const historicoResp = await fetch("http://localhost:5000/api/clientes/agendamentos", {
          method: "GET",
          headers: { Authorization: `Bearer ${authToken}` },
        });
        if (historicoResp.ok) {
          const data = await historicoResp.json();
          setHistorico(data);
        }
      } else {
        const err = await resp.json();
        alert(err.erro || "Erro ao criar agendamento.");
      }
    } catch (err) {
      alert("Erro ao criar agendamento.");
    }
  };

  async function cancelarAgendamento(id) {
    const authToken = token || usuario?.token || localStorage.getItem("token");
    if (!window.confirm("Tem certeza que deseja cancelar este agendamento?")) return;
    try {
      const resp = await fetch(`http://localhost:5000/api/clientes/agendamentos/${id}/cancelar`, {
        method: "POST",
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (resp.ok) {
        alert("Agendamento cancelado com sucesso!");
        // Atualiza histórico
        const historicoResp = await fetch("http://localhost:5000/api/clientes/agendamentos", {
          method: "GET",
          headers: { Authorization: `Bearer ${authToken}` },
        });
        if (historicoResp.ok) {
          const data = await historicoResp.json();
          setHistorico(data);
        }
      } else {
        alert("Erro ao cancelar agendamento.");
      }
    } catch (err) {
      alert("Erro ao cancelar agendamento.");
    }
  }

  async function excluirConta() {
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
        window.location.reload();
      } else {
        alert("Erro ao excluir conta.");
      }
    } catch (err) {
      alert("Erro ao excluir conta.");
    }
  }

  return (
    <div className="agendamentos-container">
      <h2>Agendar Consulta</h2>

      <label>
        Massoterapeuta:
        <select
          value={massoterapeutaSelecionado}
          onChange={(e) => setMassoterapeutaSelecionado(e.target.value)}
        >
          {massoterapeutas.map((m) => (
            <option key={m.id} value={m.id}>
              {m.nome}
            </option>
          ))}
        </select>
      </label>

      <label>
        Data e Hora:
        <DatePicker
          selected={dataHora}
          onChange={(date) => {
            if (!date) return setDataHora(null);
            // Só permite horários entre 8:30 e 18:30
            const hora = date.getHours();
            const minuto = date.getMinutes();
            const valido = (hora > 8 || (hora === 8 && minuto >= 30)) && (hora < 18 || (hora === 18 && minuto <= 30));
            if (!valido) {
              alert("Escolha um horário entre 8:30 e 18:30.");
              return;
            }
            setDataHora(date);
          }}
          showTimeSelect
          timeFormat="HH:mm"
          timeIntervals={30}
          dateFormat="dd/MM/yyyy HH:mm"
          placeholderText="Selecione data e hora"
          minDate={new Date()}
          locale="pt-BR"
          timeCaption="Horário"
          includeTimes={gerarHorariosPermitidos()}
          filterDate={(date) => {
            // Permite apenas segunda, terça, quarta e quinta-feira
            const day = date.getDay();
            return day >= 1 && day <= 4;
          }}
          dayClassName={(date) => {
            const day = date.getDay();
            if (day === 1) return "dia-semana segunda";
            if (day === 2) return "dia-semana terca";
            if (day === 3) return "dia-semana quarta";
            if (day === 4) return "dia-semana quinta";
            return "dia-semana bloqueado";
          }}
        />
      </label>

      <button onClick={criarAgendamento}>Agendar</button>

  <h3>Histórico de Agendamentos</h3>
  <button onClick={limparHistorico} style={{marginBottom: '10px'}}>Limpar Histórico</button>
      <ul>
        {historico.length === 0 && <li>Nenhum agendamento encontrado</li>}
        {historico.map((a) => (
          <li key={a.id}>
            {formatarDataHora(a.data_hora)} - {traduzirStatus(a.status)} - Massoterapeuta: {a.massoterapeuta_nome || "Não informado"}
            {a.status === 'marcado' && (
              <button onClick={() => cancelarAgendamento(a.id)} style={{marginLeft: '12px'}}>Cancelar</button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
export default AgendamentosCliente;

// Função para formatar data/hora para o padrão brasileiro
function formatarDataHora(dataHoraStr) {
  if (!dataHoraStr) return "";
  // Aceita formatos: YYYY-MM-DDTHH:mm, YYYY-MM-DD HH:mm:ss, YYYY-MM-DD HH:mm
  let d;
  let str = dataHoraStr.replace('T', ' ');
  let [datePart, timePart] = str.split(' ');
  if (datePart && timePart) {
    const [year, month, day] = datePart.split('-');
    const [hour, minute] = timePart.split(':');
    d = new Date(Number(year), Number(month)-1, Number(day), Number(hour), Number(minute));
  } else {
    d = new Date(dataHoraStr);
  }
  if (isNaN(d.getTime())) return "Data inválida";
  return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth()+1).toString().padStart(2, '0')}/${d.getFullYear()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
}

// Função para traduzir status para português
function traduzirStatus(status) {
  switch (status) {
    case 'pendente': return 'Pendente';
    case 'confirmado': return 'Confirmado';
    case 'cancelado': return 'Cancelado';
    case 'marcado': return 'Marcado';
    default: return status ? status.charAt(0).toUpperCase() + status.slice(1) : "";
  }
}

function gerarHorariosPermitidos() {
  const horarios = [];
  const agora = new Date();
  const base = new Date();
  base.setHours(8, 30, 0, 0);
  for (let h = 8; h <= 18; h++) {
    for (let m of [30, 0]) {
      if (h === 8 && m === 0) continue; // só 8:30
      if (h === 18 && m === 30) break; // até 18:30
      const horario = new Date(base);
      horario.setHours(h, m, 0, 0);
      // Só adiciona horários futuros no dia atual
      if (
        horario.getDate() > agora.getDate() ||
        horario.getMonth() > agora.getMonth() ||
        horario.getFullYear() > agora.getFullYear() ||
        (horario.getDate() === agora.getDate() && horario.getMonth() === agora.getMonth() && horario.getFullYear() === agora.getFullYear() && horario > agora)
      ) {
        horarios.push(new Date(horario));
      }
      if (h === 18 && m === 0) break;
    }
  }
  return horarios;
}