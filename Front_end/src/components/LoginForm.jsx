import React, { useState } from "react";

function LoginForm({ login, abrirCadastro }) {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [tipo, setTipo] = useState("cliente");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !senha) {
      alert("Preencha email e senha.");
      return;
    }

    setLoading(true);

    const endpoint =
      tipo === "cliente"
        ? "/api/clientes/login"
        : "/api/massoterapeutas/login";

    try {
      const resp = await fetch("http://localhost:5000" + endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      });

      const data = await resp.json();

      if (resp.ok) {
        // Corrigido: pega o token do campo correto
        const token = data.token || data.usuario?.token;
        if (!token || token === "undefined") {
          alert("Token inválido recebido do backend.");
          return;
        }
        localStorage.setItem("token", token);
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

        <label>
          Senha:
          <input
            type="password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            placeholder="Senha"
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </button>

        <p>
          Não tem conta?{" "}
          <button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              abrirCadastro();
            }}
            className="link-button"
          >
            Crie sua conta
          </button>
        </p>
      </form>
    </div>
  );
}

export default LoginForm; // ...existing code...