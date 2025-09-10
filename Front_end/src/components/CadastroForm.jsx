// CadastroForm.jsx
// Formulário exclusivo para CLIENTES se cadastrarem no sistema

import React, { useState } from "react";

function CadastroForm({ voltarLogin }) {
  // -------------------------------
  // Estados para os campos do cliente
  // -------------------------------
  const [nome, setNome] = useState("");
  const [telefone, setTelefone] = useState("");
  const [sexo, setSexo] = useState("");
  const [dataNascimento, setDataNascimento] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [loading, setLoading] = useState(false); // evita duplo clique

  // -------------------------------
  // Função para submeter cadastro
  // -------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validação simples antes de enviar
    if (!["Masculino", "Feminino", "Outro"].includes(sexo)) {
      alert("Selecione um sexo válido: Masculino, Feminino ou Outro.");
      return;
    }

    setLoading(true);

    try {
      const resp = await fetch("http://localhost:5000/api/clientes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nome,
          telefone,
          sexo,
          data_nascimento: dataNascimento,
          email,
          senha,
        }),
      });

      if (resp.ok) {
        // Limpa campos após cadastro
        setNome("");
        setTelefone("");
        setSexo("");
        setDataNascimento("");
        setEmail("");
        setSenha("");

        alert("Cadastro realizado com sucesso! Agora faça login.");
        voltarLogin(); // volta para tela de login
      } else {
        // Lê resposta de erro do backend
        let errMsg;
        try {
          const errJson = await resp.json();
          errMsg = errJson.erro || errJson.message || JSON.stringify(errJson);
        } catch {
          errMsg = await resp.text();
        }
        alert("Erro ao cadastrar: " + errMsg);
      }
    } catch (err) {
      console.error("Erro no cadastro:", err);
      alert("Erro ao tentar cadastrar. Verifique sua conexão.");
    } finally {
      setLoading(false);
    }
  };

  // -------------------------------
  // Renderização do formulário
  // -------------------------------
  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <h2>Cadastro de Cliente</h2>

        <label>
          Nome:
          <input
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            placeholder="Nome completo"
            required
          />
        </label>

        <label>
          Telefone:
          <input
            type="tel"
            value={telefone}
            onChange={(e) => setTelefone(e.target.value)}
            placeholder="(xx) xxxxx-xxxx"
            required
          />
        </label>

        <label>
          Sexo:
          <select value={sexo} onChange={(e) => setSexo(e.target.value)} required>
            <option value="">Selecione o sexo</option>
            <option value="Masculino">Masculino</option>
            <option value="Feminino">Feminino</option>
            <option value="Outro">Outro</option>
          </select>
        </label>

        <label>
          Data de Nascimento:
          <input
            type="date"
            value={dataNascimento}
            onChange={(e) => setDataNascimento(e.target.value)}
            required
          />
        </label>

        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="seuemail@exemplo.com"
            required
          />
        </label>

        <label>
          Senha:
          <input
            type="password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            placeholder="Digite sua senha"
            minLength={6}
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Cadastrando..." : "Cadastrar"}
        </button>

        <p>
          Já tem conta?{" "}
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              voltarLogin();
            }}
          >
            Login
          </a>
        </p>
      </form>
    </div>
  );
}

export default CadastroForm;
