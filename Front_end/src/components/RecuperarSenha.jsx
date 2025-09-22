import React, { useState } from "react";
import { recuperarSenha } from "../services/Api";

function RecuperarSenha({ onVoltar }) {
  const [email, setEmail] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem("");
    setErro("");
    setLoading(true);
    try {
      const resp = await recuperarSenha(email);
      setMensagem(resp.mensagem || "Verifique seu email para redefinir a senha.");
    } catch (err) {
      setErro(err.response?.data?.erro || "Erro ao enviar email de recuperação.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <h2>Recuperar senha</h2>
        <label htmlFor="email">Email cadastrado</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        {mensagem && <div className="sucesso">{mensagem}</div>}
        {erro && <div className="erro-login">{erro}</div>}
        <button type="submit" disabled={loading} className="enviar-recuperacao">
          {loading ? "Enviando..." : "Enviar link de recuperação"}
        </button>
        <button type="button" onClick={onVoltar} style={{ marginLeft: 12 }}>
          Voltar
        </button>
      </form>
    </div>
  );
}

export default RecuperarSenha;
