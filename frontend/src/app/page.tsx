"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Home() {
  const [nome, setNome] = useState("");
  const router = useRouter();

  const entrar = () => {
    if (nome.trim().length > 0) {
      router.push(`/jogo?nome=${encodeURIComponent(nome)}`);
    }
  };

  return (
    <div className="min-h-screen bg-[#1e1e2f] flex flex-col items-center justify-center p-4 text-white font-roboto">
      <h1 className="text-4xl font-bold mb-6">Bem-vindo ao Termo</h1>
      <input
        type="text"
        placeholder="Digite seu nome"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        className="mb-4 p-2 rounded bg-tranparent text-white border-2 "
      />
      <button
        onClick={entrar}
        className="bg-purple-500 text-white px-4 py-2 rounded"
        disabled={!nome.trim()}
      >
        Jogar
      </button>
    </div>
  );
}
