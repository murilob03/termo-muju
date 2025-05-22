"use client";

import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export default function TermoGame() {
  const searchParams = useSearchParams();
  const nome = searchParams.get("nome") || "";

  const [letras, setLetras] = useState(["", "", "", "", ""]);
  const [tentativas, setTentativas] = useState<any[]>([]);
  const [mensagem, setMensagem] = useState("");
  const [venceu, setVenceu] = useState(false);
  const inputsRef = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    setTentativas([]);
    setMensagem("");
    setVenceu(false);
  }, []);

  const handleChange = (index: number, value: string) => {
    const novaLetra = value.slice(-1).toLowerCase();
    const novasLetras = [...letras];
    novasLetras[index] = novaLetra;
    setLetras(novasLetras);

    if (novaLetra && index < 4) {
      inputsRef.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      enviarPalpite();
      return; // evita que outras ações sejam feitas
    }
    if (e.key === "Backspace" && !letras[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
    if (e.key === "ArrowLeft" && index > 0) {
      inputsRef.current[index - 1]?.focus();
      e.preventDefault();
      return;
    }
    if (e.key === "ArrowRight" && index < letras.length - 1) {
      inputsRef.current[index + 1]?.focus();
      e.preventDefault();
      return;
    }
  };

  const enviarPalpite = async () => {
    const palavra = letras.join("");

    if (palavra.length < 5) {
      setMensagem("Complete todas as letras.");
      return;
    }

    const res = await fetch(`${API_URL}/guess`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, palavra }),
    });

    const data = await res.json();
    console.log("Resposta da API:", data);

    if (!res.ok) {
      setMensagem(data.error || "Erro desconhecido.");
      return;
    }

    setTentativas((prev) => [...prev, data.resultado]);
    setMensagem("");
    setLetras(["", "", "", "", ""]);
    inputsRef.current[0]?.focus();

    if (data.venceu) {
      setVenceu(true);
    }
  };

  const renderLetra = (letra: any, idx: number) => {
    let bg = "bg-gray-300";
    if (letra.cor === "G") bg = "bg-green-500";
    else if (letra.cor === "Y") bg = "bg-yellow-400";
    else if (letra.cor === "R") bg = "bg-red-500";

    return (
      <span
        key={idx}
        className={`w-10 h-10 text-xl font-bold m-1 text-white flex items-center justify-center ${bg}`}
      >
        {(letra.letra || "").toUpperCase()}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-#1e1e2f flex flex-col items-center justify-center p-4 text-white">
      <h1 className="text-4xl font-bold mb-6">Termo</h1>

      {tentativas.map((linha, i) => (
        <div key={i} className="flex mb-2">
          {linha.map((letra: any, idx: number) => renderLetra(letra, idx))}
        </div>
      ))}

      {!venceu && (
        <div className="flex flex-col items-center gap-4 mt-4">
          <div className="flex gap-2">
            {letras.map((letra, i) => (
              <input
                key={i}
                ref={(el) => (inputsRef.current[i] = el)}
                type="text"
                value={letra}
                onChange={(e) => handleChange(i, e.target.value)}
                onKeyDown={(e) => handleKeyDown(i, e)}
                maxLength={1}
                className="w-10 h-10 text-center text-2xl border-b-2 border-white bg-#1e1e2f focus:outline-none focus:border-blue-400"
              />
            ))}
          </div>
          <button
            onClick={enviarPalpite}
            className="bg-purple-500 text-white px-4 py-2 rounded"
            disabled={letras.join("").length !== 5 || !nome}
          >
            Enviar
          </button>
        </div>
      )}

      {mensagem && <p className="text-red-500 mt-2">{mensagem}</p>}

      {venceu && (
        <div className="mt-4">
          <p className="text-green-400 font-bold text-xl">
            Parabéns, você acertou!
          </p>
        </div>
      )}
    </div>
  );
}
