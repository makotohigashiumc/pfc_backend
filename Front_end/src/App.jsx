import React, { useState, useEffect } from "react";
import Main from "./components/Main";
import Footer from "./components/Footer";
import "./App.css";

function App() {
  const [usuario, setUsuario] = useState(null);

  // Ao recarregar a página, tenta recuperar usuário do localStorage
  useEffect(() => {
    const token = localStorage.getItem("token");
    const usuarioSalvo = localStorage.getItem("usuario");
    if (token && usuarioSalvo) {
      setUsuario(JSON.parse(usuarioSalvo));
    }
  }, []);

  // login recebe objeto { tipo, usuario, token }
  const login = ({ tipo, usuario: dadosUsuario, token }) => {
    const usuarioCompleto = { tipo, usuario: dadosUsuario, token };
    setUsuario(usuarioCompleto);
    localStorage.setItem("token", token);
    localStorage.setItem("usuario", JSON.stringify(usuarioCompleto));
  };

  const logout = () => {
    setUsuario(null);
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
  };

  return (
    <>
      <Main usuario={usuario} login={login} logout={logout} />
      <Footer />
    </>
  );
}

export default App;