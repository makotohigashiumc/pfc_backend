
import React, { useState } from "react";
import { redefinirSenha } from "../services/Api";

function RedefinirSenha({ token, onRedefinido }) {
  const [novaSenha, setNovaSenha] = useState("");
  const [confirmar, setConfirmar] = useState("");
  const [mostrarNova, setMostrarNova] = useState(false);
  const [mostrarConfirmar, setMostrarConfirmar] = useState(false);
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem("");
    setErro("");
    if (novaSenha !== confirmar) {
      setErro("As senhas não coincidem.");
      return;
    }
    setLoading(true);
    try {
      const resp = await redefinirSenha(token, novaSenha);
      setMensagem(resp.mensagem || "Senha redefinida com sucesso!");
      setTimeout(() => {
        if (onRedefinido) onRedefinido();
      }, 1200);
    } catch (err) {
      setErro(err.response?.data?.erro || "Erro ao redefinir senha.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <h2>Redefinir senha</h2>

        <label htmlFor="novaSenha">
          Nova senha:
          <div style={{ position: 'relative' }}>
            <input
              id="novaSenha"
              type={mostrarNova ? "text" : "password"}
              value={novaSenha}
              onChange={e => setNovaSenha(e.target.value)}
              placeholder="Nova senha"
              required
              style={{ paddingRight: '38px', width: '100%', borderRadius: '8px', border: '1px solid #ccc', fontSize: '1rem', boxSizing: 'border-box', outline: 'none', transition: 'border-color 0.2s' }}
              onFocus={e => e.target.style.borderColor = '#1976d2'}
              onBlur={e => e.target.style.borderColor = '#ccc'}
            />
            <button
              type="button"
              onClick={() => setMostrarNova((v) => !v)}
              style={{ position: 'absolute', right: 8, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', fontSize: 18, color: '#888', padding: 0 }}
              tabIndex={-1}
              aria-label={mostrarNova ? 'Esconder senha' : 'Mostrar senha'}
            >
              {mostrarNova ? '🙈' : '👁️'}
            </button>
          </div>
        </label>

        <label htmlFor="confirmar">
          Confirmar nova senha:
          <div style={{ position: 'relative' }}>
            <input
              id="confirmar"
              type={mostrarConfirmar ? "text" : "password"}
              value={confirmar}
              onChange={e => setConfirmar(e.target.value)}
              placeholder="Confirmar nova senha"
              required
              style={{ paddingRight: '38px', width: '100%', borderRadius: '8px', border: '1px solid #ccc', fontSize: '1rem', boxSizing: 'border-box', outline: 'none', transition: 'border-color 0.2s' }}
              onFocus={e => e.target.style.borderColor = '#1976d2'}
              onBlur={e => e.target.style.borderColor = '#ccc'}
            />
            <button
              type="button"
              onClick={() => setMostrarConfirmar((v) => !v)}
              style={{ position: 'absolute', right: 8, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', fontSize: 18, color: '#888', padding: 0 }}
              tabIndex={-1}
              aria-label={mostrarConfirmar ? 'Esconder senha' : 'Mostrar senha'}
            >
              {mostrarConfirmar ? '🙈' : '👁️'}
            </button>
          </div>
        </label>

        {mensagem && <div className="sucesso">{mensagem}</div>}
        {erro && <div className="erro-login">{erro}</div>}

        <button type="submit" disabled={loading}>
          {loading ? "Redefinindo..." : "Redefinir senha"}
        </button>
      </form>
    </div>
  );
}

export default RedefinirSenha;
