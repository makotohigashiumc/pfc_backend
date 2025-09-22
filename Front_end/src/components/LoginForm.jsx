import React, { useState } from "react";

function LoginForm({ login, abrirCadastro, abrirRecuperarSenha }) {
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [tipo, setTipo] = useState("cliente");
  const [loading, setLoading] = useState(false);
  // ...

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !senha) {
      alert("Preencha email e senha.");
      return;
    }

  // ...
  setLoading(true);

    const endpoint =
      tipo === "cliente"
        ? "/api/clientes/login"
        : "/api/massoterapeuta/login";

    try {
      const resp = await fetch("http://localhost:5000" + endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      });

      const data = await resp.json();

      if (resp.ok) {
        const token = data.token || data.usuario?.token;
        if (!token || token === "undefined") {
          alert("Token inválido recebido do backend.");
          return;
        }
        localStorage.setItem("token", token);
        alert("Login realizado com sucesso!");
        login({ tipo, usuario: data.usuario, token });
      } else {
  alert(data.erro || "Email ou senha inválidos.");
      }
    } catch (err) {
      console.error(err);
  alert("Erro ao tentar logar. Verifique sua conexão.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        {/* ... */}
        <h2>Login</h2>

        <label>
          Tipo de usuário:
          <select value={tipo} onChange={(e) => setTipo(e.target.value)} required>
            <option value="cliente">Cliente</option>
            <option value="massoterapeuta">Massoterapeuta</option>
          </select>
        </label>

        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
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
              placeholder="Senha"
              required
              style={{ paddingRight: '38px', width: '100%', borderRadius: '8px', border: '1px solid #ccc', fontSize: '1rem', boxSizing: 'border-box', outline: 'none', transition: 'border-color 0.2s' }}
              onFocus={e => e.target.style.borderColor = '#1976d2'}
              onBlur={e => e.target.style.borderColor = '#ccc'}
            />
            <button
              type="button"
              onClick={() => setMostrarSenha((v) => !v)}
              style={{ position: 'absolute', right: 8, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', fontSize: 18, color: '#888', padding: 0 }}
              tabIndex={-1}
              aria-label={mostrarSenha ? 'Esconder senha' : 'Mostrar senha'}
            >
              {mostrarSenha ? '🙈' : '👁️'}
            </button>
          </div>
        </label>
        <a
          href="#"
          className="forgot-password"
          onClick={e => { e.preventDefault(); abrirRecuperarSenha(); }}
        >
          Esqueceu a senha?
        </a>
        <button type="submit" disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </button>
        <div style={{ marginTop: "18px", textAlign: "center" }}>
          <span>Não tem uma conta?</span>
          <button
            type="button"
            className="criar-conta-btn"
            onClick={abrirCadastro}
            style={{ marginLeft: "8px" }}
          >
            Crie a sua conta
          </button>
        </div>
      </form>
    </div>
  );
}

export default LoginForm;