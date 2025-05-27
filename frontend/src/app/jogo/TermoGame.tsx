"use client";

import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export default function TermoGame() {
  const searchParams = useSearchParams();
  const nome = searchParams.get("nome") || "";

  const [letras, setLetras] = useState(["", "", "", "", ""]);
interface LetterResult {
    letra: string;
    cor: "G" | "Y" | "R";
}

const [tentativas, setTentativas] = useState<LetterResult[][]>([]);
  const [mensagem, setMensagem] = useState("");
  const [venceu, setVenceu] = useState(false);
  const [inputSelecionado, setInputSelecionado] = useState(0);
  const [estadoTeclado, setEstadoTeclado] = useState<
    Record<string, "G" | "Y" | "R" | undefined>
  >({});
  const inputsRef = useRef<(HTMLInputElement | null)[]>([]);

  // Limpa tentativas e mensagens quando o nome mudar ou componente montar
  useEffect(() => {
    setTentativas([]);
    setMensagem("");
    setVenceu(false);
  }, [nome]);

  // Limpa mensagem só quando usuário começa a digitar uma nova palavra
  useEffect(() => {
    if (mensagem) setMensagem("");
  }, [letras, mensagem]);

  const handleChange = (index: number, value: string) => {
    const novaLetra = value.slice(-1).toUpperCase();
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
      return;
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

    try {
      const res = await fetch(`${API_URL}/guess`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, palavra }),
      });

      const data = await res.json();
      console.log("Resposta da API:", data);

      if (res.ok) {
        setTentativas((prev) => [...prev, data.resultado]);

        setEstadoTeclado((prev) => {
          const novoEstado = { ...prev };
          const prioridade = { R: 1, Y: 2, G: 3 };

          data.resultado.forEach((item: any) => {
            const l = item.letra.toLowerCase();
            const novaCor = item.cor;
            // Explicitly cast novaCor and novoEstado[l] to the appropriate type key
            if (
              !novoEstado[l] ||
              prioridade[novaCor as "R" | "Y" | "G"] > prioridade[novoEstado[l]! as "R" | "Y" | "G"]
            ) {
              novoEstado[l] = novaCor;
            }
          });

          return novoEstado;
        });

        setMensagem("");
        setLetras(["", "", "", "", ""]);
        inputsRef.current[0]?.focus();

        if (data.venceu) {
          setVenceu(true);
        }
      } else {
        setMensagem(data.error);
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      setMensagem("Erro na comunicação com o servidor.");
    }
  };

  const renderLetra = (letra: any, idx: number) => {
    let bg = "bg-gray-300";
    if (letra.cor === "G") bg = "bg-[#2E7D32]";
    else if (letra.cor === "Y") bg = "bg-[#F9A825]";
    else if (letra.cor === "R") bg = "bg-red-700";

    return (
      <span
        key={idx}
        className={`w-10 h-10 text-xl font-bold m-1 text-white flex rounded-sm items-center justify-center ${bg}`}
      >
        {(letra.letra || "").toUpperCase()}
      </span>
    );
  };

  const tecladoQWERTY = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
    ["z", "x", "c", "v", "b", "n", "m"],
  ];

  const inserirLetra = (letra: string) => {
    const novasLetras = [...letras];
    novasLetras[inputSelecionado] = letra;
    setLetras(novasLetras);

    if (inputSelecionado < 4) {
      inputsRef.current[inputSelecionado + 1]?.focus();
    }
  };

  return (
    <div className="min-h-screen bg-[#1e1e2f] flex flex-col items-center justify-center p-4 text-white font-roboto">
      <h1 className="text-4xl font-bold mb-6">TERMO</h1>

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
                ref={(el) => { inputsRef.current[i] = el; }}
                type="text"
                value={letra}
                onChange={(e) => handleChange(i, e.target.value)}
                onKeyDown={(e) => handleKeyDown(i, e)}
                maxLength={1}
                onFocus={() => setInputSelecionado(i)}
                className="w-10 h-10 text-center text-2xl border-b-2 border-white bg-[#1e1e2f] focus:outline-none focus:border-blue-400"
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

          <div className="mt-6 flex flex-col gap-2">
            {tecladoQWERTY.map((linha, linhaIndex) => (
              <div key={linhaIndex} className="flex justify-center gap-2">
                {linha.map((letra) => {
                  const letraMinuscula = letra.toLowerCase();
                  const cor = estadoTeclado[letraMinuscula];

                  let corBg = "bg-gray-700";
                  if (cor === "G") corBg = "bg-[#2E7D32]";
                  else if (cor === "Y") corBg = "bg-[#F9A825] text-black";
                  else if (cor === "R") corBg = "bg-gray-700 opacity-40";

                  return (
                    <button
                      key={letra}
                      onClick={() => inserirLetra(letraMinuscula)}
                      className={`rounded-md px-3 py-2 font-bold ${corBg}`}
                    >
                      {letra.toUpperCase()}
                    </button>
                  );
                })}
              </div>
            ))}
          </div>
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
