// src/services/api.js

const API_BASE = "http://localhost:5000/api";

// Login do cliente
export async function loginCliente(email, senha) {
  const resp = await fetch(`${API_BASE}/clientes/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha }),
  });
  if (!resp.ok) throw new Error("Login falhou");
  return resp.json();
}

// Login do massoterapeuta
export async function loginMassoterapeuta(email, senha) {
  const resp = await fetch(`${API_BASE}/massoterapeutas/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha }),
  });
  if (!resp.ok) throw new Error("Login falhou");
  return resp.json();
}

// Cadastro de cliente
export async function cadastrarCliente(dados) {
  const resp = await fetch(`${API_BASE}/clientes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });
  if (!resp.ok) throw new Error("Cadastro falhou");
  return resp.json();
}

// Recuperação de senha
export async function recuperarSenha(email) {
  const resp = await fetch(`${API_BASE}/clientes/recuperar-senha`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
  if (!resp.ok) throw new Error("Erro ao solicitar recuperação de senha");
  return resp.json();
}

// Redefinição de senha
export async function redefinirSenha(token, nova_senha) {
  const resp = await fetch(`${API_BASE}/clientes/redefinir-senha`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token, nova_senha }),
  });
  if (!resp.ok) throw new Error("Erro ao redefinir senha");
  return resp.json();
}
