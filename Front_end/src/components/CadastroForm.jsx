// CadastroForm.jsx
// Formulário exclusivo para CLIENTES se cadastrarem no sistema

import React, { useState } from "react";

function CadastroForm({ voltarLogin }) {
  const [mostrarSenha, setMostrarSenha] = useState(false);
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
  // ...

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
        // Não volta para tela de login automaticamente
      } else {
        // Lê resposta de erro do backend
        let errMsg;
        try {
          const errJson = await resp.json();
          errMsg = errJson.erro || errJson.message || JSON.stringify(errJson);
        } catch {
          errMsg = await resp.text();
        }
        alert(errMsg);
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
      <form onSubmit={handleSubmit} className="cadastro-form">
        {/* ... */}
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

        <label style={{ position: 'relative', display: 'block' }}>
          Senha:
          <div style={{ position: 'relative' }}>
            <input
              type={mostrarSenha ? "text" : "password"}
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              placeholder="Digite sua senha"
              minLength={6}
              required
              style={{
                paddingRight: '38px',
                width: '100%',
                borderRadius: '8px',
                border: '1px solid #ccc',
                fontSize: '1rem',
                boxSizing: 'border-box',
                outline: 'none',
                transition: 'border-color 0.2s',
              }}
              onFocus={e => e.target.style.borderColor = '#1976d2'}
              onBlur={e => e.target.style.borderColor = '#ccc'}
            />
            <button
              type="button"
              onClick={() => setMostrarSenha((v) => !v)}
              style={{
                position: 'absolute',
                right: 8,
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                fontSize: 18,
                color: '#888',
                padding: 0
              }}
              tabIndex={-1}
              aria-label={mostrarSenha ? 'Esconder senha' : 'Mostrar senha'}
            >
              {mostrarSenha ? '🙈' : '👁️'}
            </button>
          </div>
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
          <div style={{ marginTop: "2rem", color: "#0077b6", fontWeight: "bold" }}>
            Após o cadastro, você receberá um e-mail para confirmar sua conta antes de acessar o sistema.
          </div>
      </form>
    </div>
  );
}

export default CadastroForm;
