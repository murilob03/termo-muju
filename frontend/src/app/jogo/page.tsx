import { Suspense } from "react";
import TermoGame from "./TermoGame";

export default function Page() {
  return (
    <Suspense fallback={<div>Carregando jogo...</div>}>
      <TermoGame />
    </Suspense>
  );
}
