import React, { useState, useEffect } from "react";
import ConfirmarEmail from "./ConfirmarEmail";
import LoginForm from "./LoginForm";
import RecuperarSenha from "./RecuperarSenha";
import RedefinirSenha from "./RedefinirSenha";
import CadastroForm from "./CadastroForm";
import PerfilCliente from "./Perfil/PerfilCliente";
import PerfilMassoterapeuta from "./Perfil/PerfilMassoterapeuta";
import AgendamentosCliente from "./Agendamentos/AgendamentosCliente";
import AgendamentosMassoterapeuta from "./Agendamentos/AgendamentosMassoterapeuta";
import Especialidades from "./Especialidades";
import Contato from "./Contato";
import "../App.css";

function Main({ usuario, login, logout }) {
  const [secaoAtual, setSecaoAtual] = useState("");
  const [mostrarCadastro, setMostrarCadastro] = useState(false);
  const [mostrarRecuperar, setMostrarRecuperar] = useState(false);

  // Escuta evento customizado para trocar de seção
  useEffect(() => {
    const handler = (e) => setSecaoAtual(e.detail);
    window.addEventListener("mostrarSecao", handler);
    return () => window.removeEventListener("mostrarSecao", handler);
  }, []);

  // Reset da seção após login
  useEffect(() => {
    if (usuario) {
      setSecaoAtual("");
    }
  }, [usuario]);

  const tipoUsuario = usuario?.tipo;

  // Detecta rota de confirmação de e-mail
  const isConfirmarEmail = window.location.pathname.startsWith("/confirmar-email/");
  // Detecta rota de redefinição de senha
  const urlParams = new URLSearchParams(window.location.search);
  const tokenRedefinir = urlParams.get("token");
  const isRedefinirSenha = window.location.pathname.startsWith("/redefinir-senha") && tokenRedefinir;

  return (
    <>
      <header>
        <h1
          style={{ cursor: "pointer" }}
          onClick={() => {
            if (!usuario) setSecaoAtual(""); // Página inicial pública
            else if (tipoUsuario === "cliente") setSecaoAtual("perfil"); // Cliente
            else if (tipoUsuario === "massoterapeuta") setSecaoAtual("agendamentos"); // Massoterapeuta
          }}
        >
          HM Massoterapia
        </h1>
        <nav>
          {!usuario && (
            <>
              <a onClick={() => { setSecaoAtual("login"); setMostrarCadastro(false); }}>Login</a>
              <a onClick={() => setSecaoAtual("especialidades")}>Especialidades</a>
              <a onClick={() => setSecaoAtual("contato")}>Contato</a>
            </>
          )}
          {usuario && tipoUsuario === "cliente" && (
            <>
              <a onClick={() => setSecaoAtual("perfil")}>Perfil</a>
              <a onClick={() => setSecaoAtual("agendamentos")}>Agendamentos</a>
              <a onClick={logout}>Sair</a>
            </>
          )}
          {usuario && tipoUsuario === "massoterapeuta" && (
            <>
              <a onClick={() => setSecaoAtual("perfil")}>Perfil</a>
              <a onClick={() => setSecaoAtual("agendamentos")}>Agendamentos</a>
              <a onClick={logout}>Sair</a>
            </>
          )}
        </nav>
      </header>

      <main>
        {isConfirmarEmail ? (
          <ConfirmarEmail voltarLogin={() => { setSecaoAtual("login"); setMostrarCadastro(false); window.history.replaceState({}, '', '/'); }} />
        ) : isRedefinirSenha ? (
          <RedefinirSenha token={tokenRedefinir} onRedefinido={() => {
            setSecaoAtual("login");
            setMostrarCadastro(false);
            window.history.replaceState({}, '', '/');
          }} />
        ) : mostrarRecuperar ? (
          <RecuperarSenha onVoltar={() => setMostrarRecuperar(false)} />
        ) : (
          <>
            {/* Login e Cadastro */}
            {secaoAtual === "login" && !mostrarCadastro && (
              <LoginForm login={login} abrirCadastro={() => setMostrarCadastro(true)} abrirRecuperarSenha={() => setMostrarRecuperar(true)} />
            )}
            {secaoAtual === "login" && mostrarCadastro && (
              <CadastroForm voltarLogin={() => setMostrarCadastro(false)} />
            )}

            {/* Perfil */}
            {secaoAtual === "perfil" && tipoUsuario === "cliente" && (
              <PerfilCliente usuario={usuario.usuario} token={usuario.token} />
            )}
            {secaoAtual === "perfil" && tipoUsuario === "massoterapeuta" && (
              <PerfilMassoterapeuta usuario={usuario.usuario} token={usuario.token} />
            )}

            {/* Agendamentos */}
            {secaoAtual === "agendamentos" && tipoUsuario === "cliente" && (
              <AgendamentosCliente usuario={usuario.usuario} token={usuario.token} />
            )}
            {secaoAtual === "agendamentos" && tipoUsuario === "massoterapeuta" && (
              <AgendamentosMassoterapeuta usuario={usuario.usuario} token={usuario.token} />
            )}

            {/* Seções públicas */}
            {secaoAtual === "especialidades" && <Especialidades />}
            {secaoAtual === "contato" && <Contato />}
          </>
        )}
      </main>
    </>
  );
}

export default Main;